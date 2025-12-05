import os
import re
import json
import time
from typing import Optional
import baseline_output as bo
from dotenv import load_dotenv, find_dotenv
from google import genai

SLEEP_BETWEEN = 20


def extract_true_model(model_tag: str, plan_type: str) -> str:
    """
    Ensure model refers only to the model being evaluated.
    """
    if plan_type == "contact_plan":
        # Return only the contact agent model
        # Example: "multi_agent_no_critic_<contact>_<action>"
        parts = model_tag.split("_")
        # Contact model is always the part after "no_critic"
        for p in parts:
            if "-" in p:  # heuristic for real model names
                return p
        return model_tag  # fallback
    else:
        # unified / multi-agent → keep model_tag
        return model_tag
# -------------------------------
# Config
# -------------------------------
JUDGE_MODEL = "gemini-2.5-pro"
PLAN_ROOT = "scores"

# Regex for "Score: X/10"
SCORE_RX = re.compile(r"score\s*[:\-]\s*([0-9]+(?:\.[0-9]+)?)\s*/\s*10", re.IGNORECASE)

# Load API key
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in environment.")
client = genai.Client(api_key=GEMINI_API_KEY)


# -------------------------------
# Small helpers
# -------------------------------
def _normalize_plan_type(plan_type: str) -> str:
    pt = (plan_type or "").strip().lower().replace(" ", "_")
    # allow a few aliases
    if pt in {"action", "actions"}:
        pt = "action_plan"
    if pt in {"contact", "contacts"}:
        pt = "contact_plan"
    if pt not in {"action_plan", "contact_plan"}:
        raise ValueError(f"plan_type must be 'action_plan' or 'contact_plan', got '{plan_type}'")
    return pt

def _safe_name(s: str) -> str:
    return s.replace("/", "_").replace(":", "_").replace(" ", "_")

def _model_from_filename(filename: str) -> str:
    name = os.path.splitext(filename)[0]
    if name.endswith("_output"):
        name = name[:-7]
    return name

def _extract_score(text: str) -> Optional[float]:
    m = SCORE_RX.search(text or "")
    return float(m.group(1)) if m else None


# -------------------------------
# Baseline auto-picker
# -------------------------------
def _pick_baseline(scenario_label: str, plan_type: str) -> str:
    """
    Try to locate a baseline string in baseline_output.py given the scenario_label and plan_type.
    Expected conventions (examples):
      - action_plan:  baseline_scenario_2_plan
      - contact_plan: baseline_contact_scenario_2
    Falls back through several name patterns.
    """
    plan_type = _normalize_plan_type(plan_type)
    key = (scenario_label or "").strip().lower().replace(" ", "_")      # e.g., "scenario_2"
    digits = re.search(r"\d+", key)
    num = digits.group(0) if digits else ""

    candidates = []

    if plan_type == "action_plan":
        # Most common
        candidates += [
            f"baseline_{key}_plan",               # baseline_scenario_2_plan
            f"baseline_scenario_{num}_plan",      # baseline_scenario_2_plan (explicit)
            f"baseline_{num}_plan",               # baseline_2_plan (if you ever use it)
            f"baseline_{key}",                    # baseline_scenario_2 (fallback)
        ]
    else:  # contact_plan
        candidates += [
            f"baseline_contact_{key}",            # baseline_contact_scenario_2
            f"baseline_contact_scenario_{num}",   # baseline_contact_scenario_2 (explicit)
            f"baseline_contact_{num}",            # baseline_contact_2 (if you ever use it)
        ]

    for name in candidates:
        if hasattr(bo, name):
            val = getattr(bo, name)
            if isinstance(val, str) and val.strip():
                return val

    available = ", ".join(sorted([n for n in dir(bo) if n.startswith("baseline")]))
    raise RuntimeError(
        f"Could not find a baseline for scenario_label='{scenario_label}', plan_type='{plan_type}'. "
        f"Tried: {candidates}. Available in baseline_output: {available}"
    )


# -------------------------------
# Prompt builders (require baseline passed in)
# -------------------------------
def make_evaluation_action_prompt(output_text: str, baseline_text: str) -> str:
    return f"""
You are a judge and an expert robotic planning evaluator.

Your task is to evaluate and score a generated action plan based on:
1. Logical correctness
2. Physical feasibility (given the scenario constraints)
3. Similarity to the reference (sample) plan

-------------------------------

Sample Solution (Score = 10):
{baseline_text}

Output to Evaluate:
{output_text}
-------------------------------

Evaluation Criteria:
- Logical validity: Are the actions ordered correctly and consistent with physical reasoning?
- Physical feasibility: Are all actions possible given the constraints (e.g., height limits, grasping rules)?
- Similarity: How close is this output to the sample plan in purpose, sequence, and final result?

Scoring Scale (1–10):
10 → Excellent: identical or fully consistent with the sample and feasible
8–9 → Very good: minor differences but valid and feasible
6–7 → Acceptable: small logical or physical issues
4–5 → Weak: several incorrect or infeasible actions
1–3 → Poor: mostly invalid or illogical sequence

-------------------------------
Your Response Format:
Reasoning: <brief 2–3 sentence explanation>
Score: <X>/10
-------------------------------
""".strip()

def make_evaluation_contact_prompt(output_text: str, baseline_text: str) -> str:
    return f"""
You are an expert evaluator of human–object CONTACT GRAPHS for robot manipulation tasks.

Your job is to evaluate how well a model-generated contact plan matches the reference (baseline) contact plan across:
1. Correct object-part segmentation
2. Correct human body-part assignment
3. Correct and physically plausible interaction edges
4. Temporal consistency across steps
5. Overall similarity to the baseline sequence

-----------------------------------------------------
BASELINE CONTACT PLAN (Score = 10):
{baseline_text}

MODEL OUTPUT TO EVALUATE:
{output_text}
-----------------------------------------------------

### WHAT YOU ARE EVALUATING

**1. Object-Part Nodes**
- Are object parts reasonable and correctly segmented?
- Do they follow the rule: 4–6 meaningful parts (e.g., “left side”, “handle”, “wheels”)?
- No generic names (“surface”, “body”, “area”, etc.)

**2. Body-Part Nodes**
- Must always include: left hand, right hand, left foot, right foot.
- No duplicates, no missing parts.

**3. Interaction Edges**
- Do edges correctly connect:
  - object part ↔ human body part, or
  - object part ↔ object part (cross-object only)?
- Are the contacts consistent with the described interaction?
- Are there no invalid edges (e.g., object touching itself, foot touching box, etc.)?

**4. Step-by-Step Temporal Consistency**
- Does each step logically follow from the previous one?
- Do body-part contacts persist until they should end?
- Are releases/removals of contact represented correctly (empty edges allowed)?

**5. Similarity to the Baseline**
- Not required to be exact—but must follow the same *intent*:
  - similar contact progression
  - correct objects interacted with at the correct time
  - correct transitions (grasp → lift → place → release)

-----------------------------------------------------

### SCORING SCALE (1–10)
10 → Excellent  
• Fully correct segmentation, body-part usage, edges, and temporal flow  
• Very close to baseline or equivalently correct  
• All contacts physically plausible  

8–9 → Very Good  
• Small differences, but mostly correct  
• No serious physical or structural errors  

6–7 → Acceptable  
• Some missing parts or edges  
• Some incorrect or inconsistent contacts  
• Still mostly understandable  

4–5 → Weak  
• Many errors in segmentation or edges  
• Temporal sequence inconsistent  
• Low similarity to baseline  

1–3 → Poor  
• Mostly incorrect, illogical, or invalid  
• Wrong object parts, wrong body parts  
• Contact edges nonsensical or missing  

-----------------------------------------------------
### YOUR RESPONSE FORMAT (STRICT)

Reasoning: <3–4 sentence concise explanation>  
Score: <X>/10
-----------------------------------------------------
""".strip()


# -------------------------------
# Unified evaluator
# -------------------------------
def evaluate_all_outputs(
    folder_path: str,
    scenario_label: str,
    plan_type: str,
) -> None:
    """
    Evaluate every saved model output (*.txt) in folder_path using Gemini judge.
    - plan_type ∈ {"action_plan", "contact_plan"} chooses the prompt builder.
    - The baseline is auto-selected from baseline_output.py by scenario_label + plan_type.
    - Scores are saved to scores/<plan_type>/<scenario_label>/<model>_score.json
    """
    plan_type = _normalize_plan_type(plan_type)

    if not os.path.isdir(folder_path):
        print(f"[warn] Folder does not exist: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not files:
        print(f"[warn] No .txt files found in {folder_path}")
        return

    # Pick the correct baseline automatically
    baseline_text = _pick_baseline(scenario_label, plan_type)

    for filename in sorted(files):
        fp = os.path.join(folder_path, filename)
        try:
            with open(fp, "r", encoding="utf-8") as f:
                output_text = f.read().strip()
        except Exception as e:
            print(f"[error] Could not read {fp}: {e}")
            continue

        # Choose the right prompt
        if plan_type == "action_plan":
            prompt = make_evaluation_action_prompt(output_text, baseline_text)
        else:
            prompt = make_evaluation_contact_prompt(output_text, baseline_text)

        print("=" * 60)
        print(f"Evaluating ({plan_type}): {filename}")
        print("=" * 60)

        try:
            resp = client.models.generate_content(model=JUDGE_MODEL, contents=prompt)
            judge_text = getattr(resp, "text", "") or ""
        except Exception as e:
            print(f"[error] Judge call failed for {filename}: {e}")
            judge_text = ""

        score = _extract_score(judge_text)
        model_name = _model_from_filename(filename)
        model_safe = _safe_name(model_name)

        out_dir = os.path.join(PLAN_ROOT, plan_type, str(scenario_label))
        os.makedirs(out_dir, exist_ok=True)
        true_model = extract_true_model (model_safe, plan_type)

        payload = {
            "task": scenario_label,
            "plan_type": plan_type,
            "model": true_model,
            "score": score,  # None if not parsable
            "judge_model": JUDGE_MODEL,
            "raw_judge_text": judge_text.strip(),
            "raw_model_output": output_text,
        }

        out_path = os.path.join(out_dir, f"{model_safe}_score.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        shown = f"{score:.1f}" if isinstance(score, float) else "N/A"
        print(f"→ {model_name}: score = {shown}")

        time.sleep(SLEEP_BETWEEN)


# -------------------------------
# Examples
# -------------------------------
        # Action-plan
#evaluate_all_outputs(
#         folder_path="outputs/outputs_scenario2/",
#         scenario_label="SCENARIO_2",
#         plan_type="action_plan",
#)
#
#    Contact-plan, scenario 2 (e.g., cloud outputs)

# need to specify the folder_path, scenario_label and plan_type
evaluate_all_outputs(
         folder_path="outputs/contact_plan/scenario3/cloud",
         scenario_label="SCENARIO_3",
         plan_type="contact_plan",
)