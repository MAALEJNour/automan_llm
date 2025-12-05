from string import Template

coordinator_prompt = """
### Goal
You receive a numbered list of robot actions.
Each action line describes a manipulation or locomotion behavior involving one or more objects.

Your task is to understand the meaning of each action and translate it into a short JSON message that describes:
1. The objects involved.
2. A brief, natural description of what the robot is doing.

At the end, output one JSON array containing all converted messages in the same order as the input actions.

---

### Expected Output
Your final answer must be pure JSON, structured like this:

[
  {
    "objects": ["object 1", "object 2"],
    "interaction": "short human-readable description of what happens"
  },
  ...
]

Strict rules:
- Output only valid JSON — no text, no markdown, no code.
- Each JSON object corresponds to exactly one input action.
- If an action does not involve any object, set "objects": [].
- Stop after producing the list — do not comment or summarize.

---

### How to think about each action
When reading a line like:
> grasp_two_hands_one_obj(box A)

Ask yourself:
- What are the objects? → ["box A"]
- What is the interaction? → "grasp box A with both hands"

Then express it in the required JSON format:
{
  "objects": ["box A"],
  "interaction": "grasp box A with both hands"
}

Do this reasoning process for each action in order.
"""
contact_prompt = """

- Task: You will be given a list of objects and a short text description of human interactions with these objects. Your task is to analyze all the interaction relations among human body parts and object parts and output the results as a graph in the JSON format.

- Input format: The input is provided in the JSON format as follows

{
    "objects": [
        "object 1",
        "object 2"
    ],
    "interaction": "a short interaction description"
}

If multiple inputs are provided, they will be in an array:
[
    { "objects": [...], "interaction": "..." },
    { "objects": [...], "interaction": "..." },
    ...
]

- Output format: Provide the output strictly in JSON format, without any additional explanation or commentary, structured as follows:
[
  {
      "object part nodes": [
          "object 1, object part 1",
          "object 1, object part 2"
      ],

      "body part nodes": [
          "person 1, human body part 1",
          "person 1, human body part 2"
      ],

      "interaction edges": [
          {
              "nodes": [
                  "object a, object part b",
                  "person c, human body part d"
              ],
          },
          {
              "nodes": [
                  "object x, object part y",
                  "person z, human body part w"
              ],
          },
          {
              "nodes": [
                  "object f, object part q",
                  "object r, object part k"
              ],
          }
      ],
  },
  ...
]

After this list, write exactly:
**ALL INTERACTIONS PROCESSED**

---

- Rules for analysis:

(1) There are two types of nodes in the output interaction graph: "object part nodes" representing object parts and "body part nodes" representing human body parts.
(2) The "object part nodes" field represent a part-level segmentation of each input object. Segmentations should roughly cover the entire object without becoming excessively detailed. Use descriptive, specific part names rather than generic terms, for example, avoid "surface", "edge", "body", "base", "area", "cover", "support", "connector", "frame", and the like. Avoid numbering object parts.
Example: For a "bike", use the following parts: "handlebar", "pedal", "seat", "frame tubes", "wheels". For a "skateboard", use the following parts: "longboard deck", "wheels". For a "cordless vacuum cleaner", use the following parts: "ergonomic hand grip", "wand", "floor roller". For a "ladder", use the following parts: "side rail tubes", "rungs". For a "boxing bag", use the following parts: "punching bag". For a "box", use the following "top side", "left side", "right side", "bottom side". For a "door", use the following parts: "handle", "door frame".
(3) The "body part nodes" field must be the following: "left hand", "right hand", "left foot", "right foot". Distinguish between left/right human body parts.
(4) The "interaction edges" represent direct physical contact relationships between two end nodes. An edge connects an object part node to either a human body part node or another object part node. Do not connect part nodes within the same object. Example: when ironing on an ironing board, the soleplate part of an iron should be connected to the top flat panel part of the ironing board.
(5) Explicitly mentioned body parts in the input "interaction" field must be included.
Example: For a description "a person is lifting a single dumbbell with one hand", include either "left hand" or "right hand" in the analysis. If no specific body part
is mentioned, use the most common ergonomic interactions in the physical contact analysis.
(6) Focus on primary actions influencing object use or movement in the physical contact
analysis. Example: For "a person walking and carrying a briefcase in one hand", the
primary action for analysis is "carrying".
(7) Ensure the identified object parts belong to their respective objects in the node and
edge outputs of the interaction graph.
(8) Ensure plausible distribution and avoid conflicts or duplication of human body
parts during the interaction analysis.
(9) Exclude environmental elements, like floor, ground, or wall, from the physical contact
analysis.

- Examples:
(1) If the input is
{
    "objects": [
        "umbrella",
        "suitcase"
    ],
    "interaction": "a person is dragging a suitcase with one hand and holding an
    open umbrella with the other hand while walking"
}
then the output is
{
    "object part nodes": 
    [
        "umbrella, canopy",
        "umbrella, shaft",
        "suitcase, main compartment",
        "suitcase, handle",
        "suitcase, wheels"
    ],
    "body part nodes": [
        "person 1, left hand",
        "person 1, right hand",
        "person 1, left foot",
        "person 1, right foot"
    ],
    "interaction edges": [
        {
            "nodes": [
                "umbrella, shaft",
                "person 1, left hand"
            ],
        },
        {
            "nodes": [
                "suitcase, handle",
                "person 1, right hand"
            ]
        }
    ]
}

(2) If the input is
{
    "objects": [
        "box"
    ],
    "interaction": "a person is lifting a box"
}
then the output is
{
    "object part nodes": [
        "box, left side",
        "box, right side",
        "box, front side",
        "box, back side",
        "box, top side",
        "box, bottom side"
    ],
    "body part nodes": [
        "person 1, left hand",
        "person 1, right hand",
        "person 1, left foot",
        "person 1, right foot"
    ],
    "interaction edges": [
        {
            "nodes": [
                "box, left side",
                "person 1, left hand"
            ]
        },
        {
            "nodes": [
                "box, right side",
                "person 1, right hand"
            ]
        }
    ]
}

(3) If the input is
{
    "objects": [
        "guitar"
    ],
    "interaction": "a person is holding a guitar while standing"
}
then the output is
{
    "object part nodes": [
        "guitar, neck",
        "guitar, main compartment" 
    ],
    "body part nodes": [
        "person 1, left hand",
        "person 1, right hand",
        "person 1, left foot",
        "person 1, right foot"
    ],
    "interaction edges": [
        {
            "nodes": [
                "guitar, neck",
                "person 1, left_hand"
            ]
        }
    ]
}
"""



SCENARIO_1 = """Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene description and a task, you must output a sequence of actions from the provided list of available actions to achieve the task. Use only the actions specified—do not invent new ones. The number of actions in the sequence can vary based on the task requirements.

Scene:

The object available in the scene are the following:

A table A on the floor of size 3 m x 3 m
A table B on the floor of size 2 m x 5 m
A table C on the floor of size 3 m x 4 m
A box A on table A of size 0.2 m x 0.2 m
A box B on table B of size 0.4 m x 0.5 m
A box C on the floor of size 0.5 m x 0.4 m

Task:

Place all the boxes on table C

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. This action has to be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, object2): Lift object1 from object2 using two hands. This action has to be called before using place_two_hands_one_obj_on_loc. object2 can also be the floor.

place_two_hands_one_obj_on_loc(object1, object2): Place object1 on object2 using two hands. object2 can also be the floor.

stand(object): Stand on the specified object if the height difference between you and the object is less than 0.6m. Use this for locomotion or height adjustment when needed.

Output:

Return only a numbered list of actions with their parameters, based on the scene and task. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list.
"""
SCENARIO_2 = """Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene description and a task, you must output a sequence of actions from the provided list of available actions to achieve the task. Use only the actions specified—do not invent new ones. The number of actions in the sequence can vary based on the task requirements.

Scene:


The objects available in the scene are the following:

A shelf A placed on the floor with a height of 1.5 m
A box A placed on the floor
A box B placed on the floor in front of the shelf with a height of 0.5 m

Robot initial condition:

The robot is standing on the floor with a base height of 0.7 m.

Task:

Place the box A on the shelf.

Limitations:

 An object can only be placed on another object if and only if the height difference between the robot base and the object is below or equal to 0.3 m.

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. This action has to be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, object2): Lift object1 from object2 using two hands. This action has to be called before using place_two_hands_one_obj_on_loc. object2 can also be the floor.

place_two_hands_one_obj_on_loc(object1, object2): Place object1 on object2 using two hands. object2 can also be the floor.

stand(object): Stand on the specified object if the height difference between the robot base and the object is less than 0.6 m. object can also be the floor. If the robot stands on the object, then the robot base height gets increased by the object height.

Output:

Return only a numbered list of actions with their parameters, based on the scene and task. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list.
"""

SCENARIO_3= """Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene description and a task, you must output a sequence of actions from the provided list of available actions to achieve the task. Use only the actions specified—do not invent new ones. The number of actions in the sequence can vary based on the task requirements.

Scene:

The objects available in the scene are the following:

A table A placed on the floor
A table B placed on the floor
A box A placed on table A
A box B placed on table A
A box C placed on table A
A trolley A placed on the floor, not near table A or table B

Robot initial condition:

The robot is standing on the floor with a base height of 0.7 m.

Task:

Place all the boxes to table B.

Limitations:

The trolley can only carry 2 boxes at the time.

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. This action has to be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, object2): Lift object1 from object2 using two hands. This action has to be called before using place_two_hands_one_obj_on_loc. object2 can also be the floor.

place_two_hands_one_obj_on_loc(object1, object2): Place object1 on object2 using two hands. object2 can also be the floor.

stand(object): Stand on the specified object if the height difference between the robot base and the object is less than 0.6 m. object can also be the floor. If the robot stands on the object, then the robot base height gets increased by the object height.

push_obj_near(object1, object2): Push object1 near object2.

Output:

Return only a numbered list of actions with their parameters, based on the scene and task. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list.

"""



one_shot_plan_sc2 = """
Example Task:
Move box D from table D to the floor.

Known data:
- Robot base height = 0.7 m
- Table D height = 1.5 m
- Helper object: box C height = 0.5 m
- Allowed placing difference ≤ 0.3 m
- Standing condition: the robot can stand on an object only if |base height − object height| < 0.6 m.
  When standing, the robot base height increases by the object's height.

Reasoning:
Step 1 — Check if the robot can grasp box D directly from the floor:
- Table D height = 1.5 m, base height = 0.7 m → |0.7 − 1.5| = 0.8 m → exceeds limit → cannot reach.

Step 2 — Check if standing on box C helps:
- |0.7 − 0.5| = 0.2 m < 0.6 m → standing allowed.
- New base height = 0.7 + 0.5 = 1.2 m.
- Height difference to table D = |1.2 − 1.5| = 0.3 m ≤ 0.3 m → grasp feasible.

Step 3 — Check where to place the box:
- Target = floor (0.0 m)
- With base 0.7 m, |0.7 − 0.0| = 0.7 m → downward placing feasible (within robot reach).

Therefore:
- The robot should first stand on box C to reach the table height.
- Then grasp and lift box D from the table.
- Then return to the floor to place it safely.

(Example-only) Step-by-step reasoning:
1) Stand on box C to raise base from 0.7 m to 1.2 m (within allowed 0.6 m diff).
2) Grasp box D; at 1.2 m base vs 1.5 m table → feasible.
3) Lift box D from table D to prepare for transport.
4) Step down to the floor before placing.
5) Place box D on the floor (height difference acceptable for downward motion).
6) Free hands to finish the task.

Deduced Action Plan from the reasoning above (model output should look like this):
1. stand(box C)
2. grasp_two_hands_one_obj(box D)
3. lift_two_hands_obj_from_loc(box D, table D)
4. stand(floor)
5. place_two_hands_one_obj_on_loc(box D, floor)
6. free_two_hands()
"""

SCENARIO_4 = """Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene and a task list, you must output a sequence of actions from the provided list only—do not invent new actions. Use as many steps as needed.

Scene:

- Surfaces & furniture:
  - table A (floor-standing)
  - table B (floor-standing)
  - counter C (floor-standing)
  - side table D (single-item buffer only)
  - bed E (has head area 'bed_head')

- Containers / appliances:
  - dishwasher DW (door closed, empty; rack capacity: 6 dish items)
  - laundry basket LB (capacity: 12 clothing items)

- Objects to organize:
  - dirty dishes: dish_1, dish_2 on table A; dish_3 on table B; dish_4 on counter C
  - dirty clothes: cloth_1, cloth_2 on chair near bed; cloth_3 on floor near table B
  - bedding: crumpled duvet U on bed E; pillows P1, P2 on chair

- Heavy objects:
  - heavy box H ≈ 20 kg in the room center
  - heavy cylinder R ≈ 15 kg near counter C

Robot initial condition:

- The robot is standing on the floor with a base height of 0.7 m.
- Dishwasher DW door is CLOSED.

Task (do all, in a reasonable order):

1) Dishes: Load all dirty dishes (dish_1..dish_4) into DW, then start DW.
2) Clothes: Put all dirty clothes (cloth_1..cloth_3) into LB.
3) Heavy objects: Move H to corner X and R to corner Y.
4) Bed: Make the bed — spread U flat on bed E, place P1 and P2 at 'bed_head'.

Limitations & constraints:

- Do not place items on the floor as an intermediate surface for dishes/clothes/bedding. (Floor interaction is permitted when moving heavy objects.)
- Side table D is a single-slot buffer: at most one item at a time.
- The robot may hold only one small item at a time in hands.
- To open/close DW, keep a 0.6 m front sweep zone clear (use D as temporary buffer if needed).
- Dishwasher DW: to load, door must be OPEN; to start, door must be CLOSED and ≥ 1 item loaded; rack capacity 6.
- Laundry LB: can receive clothes anytime; no door operation required.
- Lifting constraint: Lifting is allowed only for objects ≤ 10 kg.
- stand() allowed only if |Δheight| ≤ 0.6 m (for reach).
- Avoid stacking items on tables/counter; place directly on intended surfaces/containers only.

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. Must be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. Must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, source_surface): Lift object1 from source_surface using two hands. Must be called before using place_two_hands_one_obj_on_loc. source_surface can also be the floor (only if lifting is allowed).

place_two_hands_one_obj_on_loc(object1, target_surface_or_container): Place object1 on target_surface_or_container using two hands. Target can also be the floor (only for heavy-object relocation tasks).

stand(object): Stand on the specified object if the height difference between you and the object is ≤ 0.6 m. Use this for locomotion or height adjustment when needed.

open_door(appliance): Open the appliance door (e.g., open_door(DW)); requires sweep zone clear.

close_door(appliance): Close the appliance door (e.g., close_door(DW)).

start_appliance(appliance, mode): Start the appliance with a mode (e.g., start_appliance(DW, normal)); door must be closed; capacity respected.

push_obj_to_loc(object, floor_location): Push an object along the floor to a given location.

roll_obj_to_loc(object, floor_location): Roll an object along the floor to a given location.

spread_fabric_on_loc(object_fabric, surface): Spread/arrange a deformable fabric (e.g., duvet/sheet/blanket) evenly across a planar surface (e.g., bed). Use two-hand sweeping; remove wrinkles; ensure full coverage.

Output:

Return only a numbered list of actions with their parameters, based on the scene and tasks. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list.
"""
SCENARIO_2_test = """
This is an example and you need to solve another task try to follow the reasoning provided to demonstrate what you should do and get a general overview.

### BEGIN EXAMPLE (illustrative only – DO NOT COPY NAMES/NUMBERS)

Example Setup (heights in meters):
- Destination surface: rack Z on the floor, height = 1.4
- Object to place: crate X on the floor
- helper: plinth Y on the floor, height = 0.5

Robot initial base height: H_base = 0.8

Rules (for this example):
- place_two_hands_one_obj_on_loc(A, B) allowed only if |H_base − height(B)| ≤ 0.3
- stand(B) allowed only if |H_base − height(B)| < 0.6
- After stand(B): H_base := H_base + height(B)
- Action grammar per object: grasp → lift(from support) → place(on support) → free

Goal:
- Put crate X on rack Z.

Reasoning (explicit checks):
1) Direct placement test (from floor):
   gap = |0.8 − 1.4| = 0.6  > 0.3  → cannot place X on Z directly.

2) Consider standing on plinth Y:
   stand test: |0.8 − 0.5| = 0.3 < 0.6 → allowed.
   After stand(Y): H_base = 0.8 + 0.5 = 1.3

3) Re-test placement feasibility:
   |1.3 − 1.4| = 0.1 ≤ 0.3 → placing X on Z is now feasible.

Final Action Plan (numbered list only):
1. stand(plinth Y)
2. grasp_two_hands_one_obj(crate X)
3. lift_two_hands_obj_from_loc(crate X, floor)
4. place_two_hands_one_obj_on_loc(crate X, rack Z)
5. free_two_hands()

### END EXAMPLE (illustrative only – DO NOT COPY NAMES/NUMBERS)

# RESET for the REAL TASK (below this line):
# - Ignore the example’s names and numbers.
# - Recompute all heights from the actual scene.
# - Use ONLY the capacity/limits stated in the task.
# - Emit the final numbered action list for the task.
### END EXAMPLE (illustrative only – DO NOT COPY NUMBERS)

Now this is the task you need to do: 
Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene description and a task, you must output a sequence of actions from the provided list of available actions to achieve the task. Use only the actions specified—do not invent new ones. The number of actions in the sequence can vary based on the task requirements.

Scene:

The objects available in the scene are the following:

A shelf A placed on the floor with a height of 1.5 m
A box A placed on the floor
A box B placed on the floor in front of the shelf with a height of 0.5 m

Robot initial condition:

The robot is standing on the floor with a base height of 0.7 m.
Robot_height = 0.7m

Goal:

Place the box A on the shelf.

Limitations:

An object can only be placed on another object if and only if the height difference between the robot base and the object is: height_difference= | Robot_height - object's height| <= 0.3 m (height_difference == 0.3 is allowed).

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. This action has to be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, object2): Lift object1 from object2 using two hands. This action has to be called before using place_two_hands_one_obj_on_loc. object2 can also be the floor.

place_two_hands_one_obj_on_loc(object1, object2): Place object1 on object2 using two hands. object2 can also be the floor.

stand(object): Stand on the specified object if the height difference between the robot base and the object is less than 0.6 m. object can also be the floor. If the robot stands on the object, then the robot base height gets increased by the object height.

Output:

Return only a numbered list of actions with their parameters, based on the scene and task. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list. 
Also give your reasoning for each step and don't add a step before verifying it's feasibility given the limitations.
After giving the your reasoning produce the final plan.
Note: The reasoning and the final plan must be perfectly aligned. Every feasible action found in reasoning appears in the final plan.
Do not add any action that is not in the list of available actions.
"""

SCENARIO_1_test = """
This is an example and you need to solve another task try to follow the reasoning provided to demonstrate what you should do and get a general overview.

### BEGIN EXAMPLE (illustrative only – DO NOT COPY NUMBERS,NAMES)
Example Task:
Place all containers from platform R on the floor.
Important disclaimer about this example:
- The initial conditions below are ONLY for illustrating correct reasoning.
- They do NOT carry over to, constrain, or override the initial conditions of any other task or scenario prompt.

Initial Conditions (example-only):
- All containers (crate X, crate Y) are initially placed on platform R.

Objects in the environment:
- Robot base height = 0.7 m
- Platform R height = 1.0 m
- Floor height = 0.0 m
- Standing condition: the robot can stand on an object only if |base height − object height| < 0.6 m

Reasoning (Step-by-step):

1) The goal is to relocate every container from platform R **directly to the floor**.

3) Each container can be moved independently following the standard grasp → lift → place → free sequence.

4) Because all containers start from the same location (platform R) and end on the floor,
   the same sequence can be repeated for each container.

5) Free hands to safely reset before manipulating the next object.

Final Action Plan:
1. grasp_two_hands_one_obj(crate X)
2. lift_two_hands_obj_from_loc(crate X, platform R)
3. place_two_hands_one_obj_on_loc(crate X, floor)
4. free_two_hands()
5. grasp_two_hands_one_obj(crate Y)
6. lift_two_hands_obj_from_loc(crate Y, platform R)
7. place_two_hands_one_obj_on_loc(crate Y, floor)
8. free_two_hands()

Notes:
- This example is only to help you understand the correct reasoning and output format.
- No stacking or intermediate placements are needed.
- All containers end up directly on the floor surface.
- No stand() actions are required since all height differences are feasible.
### END EXAMPLE (illustrative only – DO NOT COPY NUMBERS,NAMES)

Now this is the task you need to do: 
Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene description and a task, you must output a sequence of actions from the provided list of available actions to achieve the task. Use only the actions specified—do not invent new ones. The number of actions in the sequence can vary based on the task requirements.

Scene:

The object available in the scene are the following:

A table A on the floor of size length × width =  3 m x 3 m  
A table B on the floor of size length × width =  2 m x 5 m  
A table C on the floor of size length × width =  3 m x 4 m  
A box A on table A of size 0.2 m x 0.2 m   
A box B on table B of size 0.4 m x 0.5 m 
A box C on the floor of size 0.5 m x 0.4 m

Task:

Place all the boxes on table C

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. This action has to be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, object2): Lift object1 from object2 using two hands. This action has to be called before using place_two_hands_one_obj_on_loc. object2 can also be the floor.

place_two_hands_one_obj_on_loc(object1, object2): Place object1 on object2 using two hands. object2 can also be the floor.

stand(object): Stand on the specified object if the height difference between you and the object is less than 0.6m. Use this for locomotion or height adjustment when needed.

Output:

Return only a numbered list of actions with their parameters, based on the scene and task. Do not include any additional explanations, text, or formatting beyond the list.
Also give your reasoning for each step and don't add a step before verifying it's feasibility given the limitations.
After giving your reasoning produce the final plan based on it.
"""



SCENARIO_3_test = """
This is an example and you need to solve another task try to follow the reasoning provided to demonstrate what you should do and get a general overview.

### BEGIN EXAMPLE (illustrative only – DO NOT COPY NUMBERS)
Example (illustrative only):
Task: Move boxes A, B, C, and D from floor near table B to table C using trolley X (capacity 4).

Important disclaimer about this example:
- The initial conditions below are ONLY for illustrating correct reasoning.
- They do NOT carry over to, constrain, or override the initial conditions of any other task or scenario prompt.

Initial Conditions (example-only):
- box D, box E, box F, and box G are on the floor near table B.
- trolley X is on the floor, not near table B and not near table C.
- Trolley capacity = 4.

Reasoning (step-by-step):

1) Goal interpretation (end-state facts):
   - box D on table C
   - box E on table C
   - box F on table C
   - box G on table C
   - No stacking between the boxes.

2) Minimal-trip transport planning:
   - Four boxes, trolley capacity 4 → all can be moved in a single trip.

3) Proximity planning (preconditions for manipulation):
   - The trolley starts not near table B. To load at table B, first ensure:
     push_obj_near(trolley A, table B)
   - After loading all boxes, to unload at table C, ensure:
     push_obj_near(trolley A, table C)

4) Action grammar per object (safety and consistency):
   For each object manipulation:
   grasp_two_hands_one_obj → lift_two_hands_obj_from_loc → place_two_hands_one_obj_on_loc → free_two_hands

5) Sanity and feasibility checks:
   - Capacity never exceeds 4.
   - No stacking of boxes on each other.
   - Exactly two pushes (one to source, one to destination) — minimal.
   - No unnecessary standing or temporary placements.

Final Action Plan:
1. push_obj_near(trolley X, table B)

# Load 4 boxes onto the trolley (near table B)
2. grasp_two_hands_one_obj(box D)
3. lift_two_hands_obj_from_loc(box D, floor)
4. place_two_hands_one_obj_on_loc(box D, trolley X)
5. free_two_hands()

6. grasp_two_hands_one_obj(box E)
7. lift_two_hands_obj_from_loc(box E, floor)
8. place_two_hands_one_obj_on_loc(box E, trolley X)
9. free_two_hands()

10. grasp_two_hands_one_obj(box F)
11. lift_two_hands_obj_from_loc(box F, floor)
12. place_two_hands_one_obj_on_loc(box F, trolley X)
13. free_two_hands()

14. grasp_two_hands_one_obj(box G)
15. lift_two_hands_obj_from_loc(box G, floor)
16. place_two_hands_one_obj_on_loc(box G, trolley X)
17. free_two_hands()

# Move trolley to destination (near table C)
18. push_obj_near(trolley X, table C)

# Unload 4 boxes onto table C
19. grasp_two_hands_one_obj(box D)
20. lift_two_hands_obj_from_loc(box D, trolley X)
21. place_two_hands_one_obj_on_loc(box D, table C)
22. free_two_hands()

23. grasp_two_hands_one_obj(box E)
24. lift_two_hands_obj_from_loc(box E, trolley X)
25. place_two_hands_one_obj_on_loc(box E, table C)
26. free_two_hands()

27. grasp_two_hands_one_obj(box F)
28. lift_two_hands_obj_from_loc(box F, trolley X)
29. place_two_hands_one_obj_on_loc(box F, table C)
30. free_two_hands()

31. grasp_two_hands_one_obj(box G)
32. lift_two_hands_obj_from_loc(box G, trolley X)
33. place_two_hands_one_obj_on_loc(box G, table C)
34. free_two_hands()

Explanation summary:
- First push aligns the trolley with the loading area (table B). Second push aligns it with the unloading area (table C).
- Per-object grammar is respected for every manipulation.
- Capacity respected; exactly one trip with four boxes.
- No illegal stacking or unnecessary steps.
### END EXAMPLE (illustrative only – DO NOT COPY NUMBERS)

Now this is the task you need to do: 
Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene description and a task, you must output a sequence of actions from the provided list of available actions to achieve the task. Use only the actions specified—do not invent new ones. The number of actions in the sequence can vary based on the task requirements.

Scene:

The objects available in the scene are the following:

A table A placed on the floor
A table B placed on the floor
A box A placed on table A
A box B placed on table A
A box C placed on table A
A trolley A placed on the floor, not near table A or table B

Robot initial condition:

The robot is standing on the floor with a base height of 0.7 m.

Task:

Place all the boxes to table B.
Goal: Put TARGET_BOXES = {box A, box B, box C} on table B.
Limitations:

The trolley can only carry 2 boxes at the time.

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. This action has to be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, object2): Lift object1 from object2 using two hands. This action has to be called before using place_two_hands_one_obj_on_loc. object2 can also be the floor.

place_two_hands_one_obj_on_loc(object1, object2): Place object1 on object2 using two hands. object2 can also be the floor.

stand(object): Stand on the specified object if the height difference between the robot base and the object is less than 0.6 m. object can also be the floor. If the robot stands on the object, then the robot base height gets increased by the object height.

push_obj_near(object1, object2): Push object1 near object2.

Output:

Return only a numbered list of actions with their parameters, based on the scene and task. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list.
Try to make few trips as possible. Also give your reasoning for each step and don't add a step before verifying it's feasibility given the limitations.
After giving your reasoning produce the final plan based on it.
Important: Think about transporting all boxes using minimal trips.
Before producing any plan, compute:
  N = number of boxes to move
  K = trolley capacity stated in THIS task
"""


UNIFIED_PROMPT= Template(r"""
You are a single agent that must perform an end-to-end pipeline divided into three tasks:

TASK 1 — ACTION PLAN (use SCENARIO)
TASK 2 — ACTION→MESSAGE MAPPING (convert action lines to JSON messages)
TASK 3 — CONTACT ANALYSIS (turn each message into a part-level contact graph)

OUTPUT CONTRACT (very important):
- Emit your results in THREE sections, in this exact order.
- Do NOT print anything outside these sections.

1) ===ACTION_PLAN===
   (Only the numbered list per SCENARIO Output — no extra text)
   ===END_ACTION_PLAN===

2) ===COORDINATOR_OUTPUT===
   (Pure JSON array only, as required by TASK 2)
   ===END_COORDINATOR_OUTPUT===

3) ===CONTACT_OUTPUT===
   (A JSON list of graphs in the same order as messages in TASK 2.
    After the list, write exactly: ALL INTERACTIONS PROCESSED)
   ===END_CONTACT_OUTPUT===

You MUST:
- In TASK 2, use the exact action lines you produced in TASK 1 as input.
- In TASK 3, use the exact JSON array you produced in TASK 2 as input.
- Preserve ordering between all tasks.

----------------------------------------------------------------
TASK 1 PROMPT ($scenario_label) 
----------------------------------------------------------------

SCENARIO= $scenario_text


----------------------------------------------------------------
TASK 2 PROMPT (Action → Message mapping)
----------------------------------------------------------------

coordinator_prompt = $coordinator_prompt


----------------------------------------------------------------
TASK 3 PROMPT (Contact analysis)
----------------------------------------------------------------

contact_prompt = $contact_prompt

----------------------------------------------------------------
PIPELINE EXECUTION REMINDER (do not print this section)
----------------------------------------------------------------
- Produce the three sections in order.
- TASK 1 uses SCENARIO_1 to create the numbered Action Plan.
- TASK 2 converts the Action Plan lines into the JSON array; place that array between the COORDINATOR_OUTPUT tags.
- TASK 3 converts that array into a list of JSON contact graphs; place those between CONTACT_OUTPUT tags, then write exactly:
  ALL INTERACTIONS PROCESSED
- Do not include any commentary or markdown outside the specified section tags.
""")

def build_unified_prompt(scenario_var_name: str) -> str:
    """
    Substitute ONLY the scenario text. Leave {COORDINATOR_PROMPT} and {contact_prompt}
    as literal placeholders in the output.
    """
    try:
        ns =  globals()
        scenario_text = ns[scenario_var_name]
        coord_text = ns["coordinator_prompt"]
        contact_text = ns["contact_prompt"]
    except KeyError as e:
        raise KeyError(f"Missing scenario in namespace: {scenario_var_name}") from e
    return UNIFIED_PROMPT.substitute(
        scenario_label=scenario_var_name,
        scenario_text=scenario_text,
        coordinator_prompt = coord_text,
        contact_prompt = contact_text,
    )


SCENARIO_CLEANING_HOME= """Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Given a scene description and a task, you must output a sequence of actions from the provided list of available actions to achieve the task. Use only the actions specified—do not invent new ones. The number of actions in the sequence can vary based on the task requirements.

Scene (rooms & surfaces/containers):
- Kitchen: sink K_sink, dishwasher DW (door CLOSED), dish_rack K_rack, counter K_counter, trash_bin K_trash
- Living room: TV_stand L_tv, bookshelf L_books, coffee_table L_coffee, toy_bin L_toys, shoe_rack L_shoes
- Bedroom: bed B_bed, bedside_table B_side, closet B_closet, laundry_basket B_laundry
- Bathroom: sink BA_sink, medicine_cabinet BA_med, towel_bar BA_towel
- Entryway: mail_tray E_mail, shoe_rack E_shoes
- Side table D_side (maximum capacity: one item)

Initial clutter:
- Dishes: mug1 on B_side, plate1 on L_coffee and bowl1 on B_bed
- Toys: toy_car on K_counter and plush_bear on BA_sink
- Clothes: tshirt1 on L_coffee and sock1 on L_tv
- Shoes: shoe_pair1 on L_coffee
- Tools/misc: scissors1 on L_coffee, remote1 on K_counter and pill_bottle on L_coffee
- Trash: can_empty on B_side, tissue_used on L_coffee

Robot initial condition:
- The robot is standing on the floor with a base height of 0.7 m.
- Dishwasher DW door is CLOSED.

Goal:
- Restore the home to a tidy, typical state by relocating each object to a reasonable storage/placement location available in the scene.
- Choose destinations using ordinary household conventions.
- Be consistent: similar items should end up in the same type of place you decide (your choice), and do not invent containers or locations not listed above.
- Do not leave objects on the floor or on clearly inappropriate surfaces when finished.

Constraints:
- Carry/handle one small item at a time.
- Do not place items on the floor as an intermediate surface.
- D_side can hold at most one item at a time (temporary buffer).
- Opening/closing DW requires a clear 0.6 m front sweep zone (use D_side if needed).
- To place inside DW or on K_rack, DW door must be OPEN,
- To close DW, hands must be free.
- stand(object) allowed only if |Δheight| ≤ 0.6 m (reach adjustment).
- Avoid unsafe placements (e.g., sharp tools in non-kitchen living areas).


Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. Must precede lift_two_hands_obj_from_loc.

lift_two_hands_obj_from_loc(object, source_surface): Lift object from its current surface/container.

place_two_hands_one_obj_on_loc(object, target_surface_or_container): Place object on/into target listed in the scene.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

stand(object): Stand on an object/surface if the height difference is ≤ 0.6 m to adjust reach.

open_door(appliance): Open an appliance door. 

close_door(appliance): Close an appliance door.


Output:
Return only a numbered list of actions with their parameters, based on the scene and task. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list.
"""


SCENARIO_MAKING_COFFEE = """Setup

You are an AI assistant specialized in planning action sequences for humanoid robots performing loco-manipulation tasks. Use only the actions listed—do not invent new ones. The number of steps may vary.

Scene:

- Countertop: coffee_machine CM (mug platform, OFF), sugar_jar SJ (closed)
- Sink S with dish_soap DS, drying_rack DR
- Fridge F 
- Cup A on counter (CUP_A is CLEAN)
- Cup B on counter (CUP_B is DIRTY)
- milk_carton MC (closed and stored INSIDE fridge F which is also closed)

Robot initial condition:

- Robot stands on the floor, hands-free.


Task:

Prepare two coffees:
1) One black coffee in CUP_A (no sugar, no milk).
2) One coffee with sugar and milk in CUP_B.

Limitations:

- Do not place items on the floor as an intermediate surface.
- Handle one small item at a time.
- stand(object) allowed only if |Δheight| ≤ 0.6 m.
- Liquids must be poured only into a clean cup.
- To access an item inside a closed container, you must open that container first and close it when finished.

Available Actions:

grasp_two_hands_one_obj(object): Grasp the specified object using two hands. This action has to be called before using lift_two_hands_obj_from_loc.

free_two_hands(): Free both hands after placing an object, releasing any held object. This action must be called after using place_two_hands_one_obj_on_loc.

lift_two_hands_obj_from_loc(object1, object2): Lift object1 from object2 using two hands. This action has to be called before using place_two_hands_one_obj_on_loc. object2 can also be the floor.

place_two_hands_one_obj_on_loc(object1, object2): Place object1 on object2 using two hands. object2 can also be the floor.

stand(object): Stand on the specified object if the height difference between you and the object is less than 0.6m. Use this for locomotion or height adjustment when needed.

open_container(container): Open a container (e.g., SJ).

close_container(container): Close a container that was opened.

wash_item_in_sink(item, sink, soap): Wash an item in the sink with soap (renders the item clean).

dry_item_on_rack(item, rack): Place washed item on a rack briefly to drain (makes it ready to use).

dispense_coffee(machine, target): Dispense hot coffee from CM into target.

scoop_from_to(source_container, target, item_name): Transfer a small amount (e.g., sugar) from a container to a target.

pour_from_to(source_container, target): Pour liquid from a container to a target.

press_button(device, button_name): Press a device button (e.g., START, OFF).

Output:

Return only a numbered list of actions with their parameters, based on the scene and task. Use fewer or more actions as necessary. Do not include any additional explanations, text, or formatting beyond the list.
"""



