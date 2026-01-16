# this baseline is used to evaluate other agents prompts compared to the baseline
# For all scenarios: baseline is the deepseek model: DeepSeek-V3.2-Exp

baseline_contact_scenario_1 = """[
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side",
      "table A, tabletop",
      "table A, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side",
      "table C, tabletop",
      "table C, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box A, bottom side",
          "table C, tabletop"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side",
      "table B, tabletop",
      "table B, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side",
      "table C, tabletop",
      "table C, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box B, bottom side",
          "table C, tabletop"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side",
      "table C, tabletop",
      "table C, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box C, bottom side",
          "table C, tabletop"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  }
]
"""
baseline_contact_scenario_2= """[
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side",
      "shelf A, shelf surface",
      "shelf A, shelf brackets"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box A, bottom side",
          "shelf A, shelf surface"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  }
]

"""
baseline_contact_scenario_3="""[
  {
    "object part nodes": [
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels",
      "table A, tabletop",
      "table A, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "trolley A, handle",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "trolley A, handle",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side",
      "table A, tabletop",
      "table A, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side",
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box A, bottom side",
          "trolley A, platform"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side",
      "table A, tabletop",
      "table A, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side",
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box B, bottom side",
          "trolley A, platform"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  },
  {
    "object part nodes": [
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels",
      "table B, tabletop",
      "table B, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "trolley A, handle",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "trolley A, handle",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side",
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box A, top side",
      "box A, bottom side",
      "box A, left side",
      "box A, right side",
      "box A, front side",
      "box A, back side",
      "table B, tabletop",
      "table B, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box A, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box A, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box A, bottom side",
          "table B, tabletop"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side",
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box B, top side",
      "box B, bottom side",
      "box B, left side",
      "box B, right side",
      "box B, front side",
      "box B, back side",
      "table B, tabletop",
      "table B, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box B, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box B, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box B, bottom side",
          "table B, tabletop"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  },
  {
    "object part nodes": [
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels",
      "table A, tabletop",
      "table A, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "trolley A, handle",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "trolley A, handle",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side",
      "table A, tabletop",
      "table A, legs"
    ],
    "body part nodes": [    
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side",
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box C, bottom side",
          "trolley A, platform"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  },
  {
    "object part nodes": [
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels",
      "table B, tabletop",
      "table B, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "trolley A, handle",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "trolley A, handle",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side",
      "trolley A, handle",
      "trolley A, platform",
      "trolley A, wheels"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      }
    ]
  },
  {
    "object part nodes": [
      "box C, top side",
      "box C, bottom side",
      "box C, left side",
      "box C, right side",
      "box C, front side",
      "box C, back side",
      "table B, tabletop",
      "table B, legs"
    ],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": [
      {
        "nodes": [
          "box C, left side",
          "person 1, left hand"
        ]
      },
      {
        "nodes": [
          "box C, right side",
          "person 1, right hand"
        ]
      },
      {
        "nodes": [
          "box C, bottom side",
          "table B, tabletop"
        ]
      }
    ]
  },
  {
    "object part nodes": [],
    "body part nodes": [
      "person 1, left hand",
      "person 1, right hand",
      "person 1, left foot",
      "person 1, right foot"
    ],
    "inter  edges": []
  }
]
"""




baseline_scenario3_plan = """
1. push_obj_near(trolley A, table A)
2. grasp_two_hands_one_obj(box A)
3. lift_two_hands_obj_from_loc(box A, table A)
4. place_two_hands_one_obj_on_loc(box A, trolley A)
5. free_two_hands()
6. grasp_two_hands_one_obj(box B)
7. lift_two_hands_obj_from_loc(box B, table A)
8. place_two_hands_one_obj_on_loc(box B, trolley A)
9. free_two_hands()
10. push_obj_near(trolley A, table B)
11. grasp_two_hands_one_obj(box A)
12. lift_two_hands_obj_from_loc(box A, trolley A)
13. place_two_hands_one_obj_on_loc(box A, table B)
14. free_two_hands()
15. grasp_two_hands_one_obj(box B)
16. lift_two_hands_obj_from_loc(box B, trolley A)
17. place_two_hands_one_obj_on_loc(box B, table B)
18. free_two_hands()
19. push_obj_near(trolley A, table A)
20. grasp_two_hands_one_obj(box C)
21. lift_two_hands_obj_from_loc(box C, table A)
22. place_two_hands_one_obj_on_loc(box C, trolley A)
23. free_two_hands()
24. push_obj_near(trolley A, table B)
25. grasp_two_hands_one_obj(box C)
26. lift_two_hands_obj_from_loc(box C, trolley A)
27. place_two_hands_one_obj_on_loc(box C, table B)
28. free_two_hands()
"""
baseline_scenario_1_plan = """
1. grasp_two_hands_one_obj(box A)
2. lift_two_hands_obj_from_loc(box A, table A)
3. place_two_hands_one_obj_on_loc(box A, table C)
4. free_two_hands()
5. grasp_two_hands_one_obj(box B)
6. lift_two_hands_obj_from_loc(box B, table B)
7. place_two_hands_one_obj_on_loc(box B, table C)
8. free_two_hands()
9. grasp_two_hands_one_obj(box C)
10. lift_two_hands_obj_from_loc(box C, floor)
11. place_two_hands_one_obj_on_loc(box C, table C)
12. free_two_hands()
"""

baseline_scenario_2_plan = """
1. grasp_two_hands_one_obj(box A)
2. lift_two_hands_obj_from_loc(box A, floor)
3. stand(box B)
4. place_two_hands_one_obj_on_loc(box A, shelf A)
5. free_two_hands()
"""

baseline_scenario_4_plan = """
1. open_door(DW)
2. grasp_two_hands_one_obj(mug1)
3. lift_two_hands_obj_from_loc(mug1, B_side)
4. place_two_hands_one_obj_on_loc(mug1, DW)
5. free_two_hands()
6. grasp_two_hands_one_obj(plate1)
7. lift_two_hands_obj_from_loc(plate1, L_coffee)
8. place_two_hands_one_obj_on_loc(plate1, DW)
9. free_two_hands()
10. grasp_two_hands_one_obj(bowl1)
11. lift_two_hands_obj_from_loc(bowl1, B_bed)
12. place_two_hands_one_obj_on_loc(bowl1, DW)
13. free_two_hands()
14. close_door(DW)
15. grasp_two_hands_one_obj(toy_car)
16. lift_two_hands_obj_from_loc(toy_car, K_counter)
17. place_two_hands_one_obj_on_loc(toy_car, L_toys)
18. free_two_hands()
19. grasp_two_hands_one_obj(plush_bear)
20. lift_two_hands_obj_from_loc(plush_bear, BA_sink)
21. place_two_hands_one_obj_on_loc(plush_bear, L_toys)
22. free_two_hands()
23. grasp_two_hands_one_obj(tshirt1)
24. lift_two_hands_obj_from_loc(tshirt1, L_coffee)
25. place_two_hands_one_obj_on_loc(tshirt1, B_laundry)
26. free_two_hands()
27. grasp_two_hands_one_obj(sock1)
28. lift_two_hands_obj_from_loc(sock1, L_tv)
29. place_two_hands_one_obj_on_loc(sock1, B_laundry)
30. free_two_hands()
31. grasp_two_hands_one_obj(shoe_pair1)
32. lift_two_hands_obj_from_loc(shoe_pair1, L_coffee)
33. place_two_hands_one_obj_on_loc(shoe_pair1, L_shoes)
34. free_two_hands()
35. grasp_two_hands_one_obj(scissors1)
36. lift_two_hands_obj_from_loc(scissors1, L_coffee)
37. place_two_hands_one_obj_on_loc(scissors1, K_counter)
38. free_two_hands()
39. grasp_two_hands_one_obj(remote1)
40. lift_two_hands_obj_from_loc(remote1, K_counter)
41. place_two_hands_one_obj_on_loc(remote1, L_tv)
42. free_two_hands()
43. open_door(BA_med)
44. grasp_two_hands_one_obj(pill_bottle)
45. lift_two_hands_obj_from_loc(pill_bottle, L_coffee)
46. place_two_hands_one_obj_on_loc(pill_bottle, BA_med)
47. free_two_hands()
48. close_door(BA_med)
49. grasp_two_hands_one_obj(can_empty)
50. lift_two_hands_obj_from_loc(can_empty, B_side)
51. place_two_hands_one_obj_on_loc(can_empty, K_trash)
52. free_two_hands()
53. grasp_two_hands_one_obj(tissue_used)
54. lift_two_hands_obj_from_loc(tissue_used, L_coffee)
55. place_two_hands_one_obj_on_loc(tissue_used, K_trash)
56. free_two_hands()
"""

baseline_scenario_5_plan = """
1. grasp_two_hands_one_obj(CUP_B)
2. lift_two_hands_obj_from_loc(CUP_B, counter)
3. wash_item_in_sink(CUP_B, S, DS)
4. dry_item_on_rack(CUP_B, DR)
5. grasp_two_hands_one_obj(CUP_B)
6. lift_two_hands_obj_from_loc(CUP_B, DR)
7. place_two_hands_one_obj_on_loc(CUP_B, counter)
8. free_two_hands()
9. press_button(CM, "ON")
10. grasp_two_hands_one_obj(CUP_A)
11. lift_two_hands_obj_from_loc(CUP_A, counter)
12. place_two_hands_one_obj_on_loc(CUP_A, CM)
13. free_two_hands()
14. dispense_coffee(CM, CUP_A)
15. grasp_two_hands_one_obj(CUP_A)
16. lift_two_hands_obj_from_loc(CUP_A, CM)
17. place_two_hands_one_obj_on_loc(CUP_A, counter)
18. free_two_hands()
19. grasp_two_hands_one_obj(CUP_B)
20. lift_two_hands_obj_from_loc(CUP_B, counter)
21. place_two_hands_one_obj_on_loc(CUP_B, CM)
22. free_two_hands()
23. dispense_coffee(CM, CUP_B)
24. grasp_two_hands_one_obj(CUP_B)
25. lift_two_hands_obj_from_loc(CUP_B, CM)
26. place_two_hands_one_obj_on_loc(CUP_B, counter)
27. free_two_hands()
28. open_container(SJ)
29. scoop_from_to(SJ, CUP_B, sugar)
30. close_container(SJ)
31. open_container(F)
32. grasp_two_hands_one_obj(MC)
33. lift_two_hands_obj_from_loc(MC, F)
34. close_container(F)
35. pour_from_to(MC, CUP_B)
36. open_container(F)
37. place_two_hands_one_obj_on_loc(MC, F)
38. free_two_hands()
39. close_container(F)
40. press_button(CM, "OFF")
"""
baseline_coordinator_scenario_1 = """[
  {"objects": ["box A"], "interaction": "grasp box A with both hands"},
  {"objects": ["box A", "table A"], "interaction": "lift box A from table A using both hands"},
  {"objects": ["box A", "table C"], "interaction": "place box A on table C using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["box B"], "interaction": "grasp box B with both hands"},
  {"objects": ["box B", "table B"], "interaction": "lift box B from table B using both hands"},
  {"objects": ["box B", "table C"], "interaction": "place box B on table C using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["box C"], "interaction": "grasp box C with both hands"},
  {"objects": ["box C", "floor"], "interaction": "lift box C from floor using both hands"},
  {"objects": ["box C", "table C"], "interaction": "place box C on table C using both hands"},
  {"objects": [], "interaction": "free both hands"}
]"""
baseline_coordinator_scenario_2 = """[
  {"objects": ["box A"], "interaction": "grasp box A with both hands"},
  {"objects": ["box A", "floor"], "interaction": "lift box A from floor using both hands"},
  {"objects": ["box B"], "interaction": "stand on box B"},
  {"objects": ["box A", "shelf A"], "interaction": "place box A on shelf A using both hands"},
  {"objects": [], "interaction": "free both hands"}
]"""
baseline_coordinator_scenario_3 = """[
  {
    "objects": ["trolley A", "table A"],
    "interaction": "push trolley A near table A"
  },
  {
    "objects": ["box A"],
    "interaction": "grasp box A with both hands"
  },
  {
    "objects": ["box A", "table A"],
    "interaction": "lift box A from table A using both hands"
  },
  {
    "objects": ["box A", "trolley A"],
    "interaction": "place box A on trolley A using both hands"
  },
  {
    "objects": [],
    "interaction": "free both hands"
  },
  {
    "objects": ["box B"],
    "interaction": "grasp box B with both hands"
  },
  {
    "objects": ["box B", "table A"],
    "interaction": "lift box B from table A using both hands"
  },
  {
    "objects": ["box B", "trolley A"],
    "interaction": "place box B on trolley A using both hands"
  },
  {
    "objects": [],
    "interaction": "free both hands"
  },
  {
    "objects": ["trolley A", "table B"],
    "interaction": "push trolley A near table B"
  },
  {
    "objects": ["box A"],
    "interaction": "grasp box A with both hands"
  },
  {
    "objects": ["box A", "trolley A"],
    "interaction": "lift box A from trolley A using both hands"
  },
  {
    "objects": ["box A", "table B"],
    "interaction": "place box A on table B using both hands"
  },
  {
    "objects": [],
    "interaction": "free both hands"
  },
  {
    "objects": ["box B"],
    "interaction": "grasp box B with both hands"
  },
  {
    "objects": ["box B", "trolley A"],
    "interaction": "lift box B from trolley A using both hands"
  },
  {
    "objects": ["box B", "table B"],
    "interaction": "place box B on table B using both hands"
  },
  {
    "objects": [],
    "interaction": "free both hands"
  },
  {
    "objects": ["trolley A", "table A"],
    "interaction": "push trolley A near table A"
  },
  {
    "objects": ["box C"],
    "interaction": "grasp box C with both hands"
  },
  {
    "objects": ["box C", "table A"],
    "interaction": "lift box C from table A using both hands"
  },
  {
    "objects": ["box C", "trolley A"],
    "interaction": "place box C on trolley A using both hands"
  },
  {
    "objects": [],
    "interaction": "free both hands"
  },
  {
    "objects": ["trolley A", "table B"],
    "interaction": "push trolley A near table B"
  },
  {
    "objects": ["box C"],
    "interaction": "grasp box C with both hands"
  },
  {
    "objects": ["box C", "trolley A"],
    "interaction": "lift box C from trolley A using both hands"
  },
  {
    "objects": ["box C", "table B"],
    "interaction": "place box C on table B using both hands"
  },
  {
    "objects": [],
    "interaction": "free both hands"
  }
]"""
baseline_coordinator_scenario_4 = """[
  {"objects": ["DW"], "interaction": "open DW door"},
  {"objects": ["mug1"], "interaction": "grasp mug1 with both hands"},
  {"objects": ["mug1", "B_side"], "interaction": "lift mug1 from B_side using both hands"},
  {"objects": ["mug1", "DW"], "interaction": "place mug1 in DW using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["plate1"], "interaction": "grasp plate1 with both hands"},
  {"objects": ["plate1", "L_coffee"], "interaction": "lift plate1 from L_coffee using both hands"},
  {"objects": ["plate1", "DW"], "interaction": "place plate1 in DW using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["bowl1"], "interaction": "grasp bowl1 with both hands"},
  {"objects": ["bowl1", "B_bed"], "interaction": "lift bowl1 from B_bed using both hands"},
  {"objects": ["bowl1", "DW"], "interaction": "place bowl1 in DW using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["DW"], "interaction": "close DW door"},
  {"objects": ["toy_car"], "interaction": "grasp toy_car with both hands"},
  {"objects": ["toy_car", "K_counter"], "interaction": "lift toy_car from K_counter using both hands"},
  {"objects": ["toy_car", "L_toys"], "interaction": "place toy_car in L_toys using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["plush_bear"], "interaction": "grasp plush_bear with both hands"},
  {"objects": ["plush_bear", "BA_sink"], "interaction": "lift plush_bear from BA_sink using both hands"},
  {"objects": ["plush_bear", "L_toys"], "interaction": "place plush_bear in L_toys using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["tshirt1"], "interaction": "grasp tshirt1 with both hands"},
  {"objects": ["tshirt1", "L_coffee"], "interaction": "lift tshirt1 from L_coffee using both hands"},
  {"objects": ["tshirt1", "B_laundry"], "interaction": "place tshirt1 in B_laundry using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["sock1"], "interaction": "grasp sock1 with both hands"},
  {"objects": ["sock1", "L_tv"], "interaction": "lift sock1 from L_tv using both hands"},
  {"objects": ["sock1", "B_laundry"], "interaction": "place sock1 in B_laundry using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["shoe_pair1"], "interaction": "grasp shoe_pair1 with both hands"},
  {"objects": ["shoe_pair1", "L_coffee"], "interaction": "lift shoe_pair1 from L_coffee using both hands"},
  {"objects": ["shoe_pair1", "L_shoes"], "interaction": "place shoe_pair1 on L_shoes using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["scissors1"], "interaction": "grasp scissors1 with both hands"},
  {"objects": ["scissors1", "L_coffee"], "interaction": "lift scissors1 from L_coffee using both hands"},
  {"objects": ["scissors1", "K_counter"], "interaction": "place scissors1 on K_counter using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["remote1"], "interaction": "grasp remote1 with both hands"},
  {"objects": ["remote1", "K_counter"], "interaction": "lift remote1 from K_counter using both hands"},
  {"objects": ["remote1", "L_tv"], "interaction": "place remote1 on L_tv using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["BA_med"], "interaction": "open BA_med door"},
  {"objects": ["pill_bottle"], "interaction": "grasp pill_bottle with both hands"},
  {"objects": ["pill_bottle", "L_coffee"], "interaction": "lift pill_bottle from L_coffee using both hands"},
  {"objects": ["pill_bottle", "BA_med"], "interaction": "place pill_bottle in BA_med using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["BA_med"], "interaction": "close BA_med door"},
  {"objects": ["can_empty"], "interaction": "grasp can_empty with both hands"},
  {"objects": ["can_empty", "B_side"], "interaction": "lift can_empty from B_side using both hands"},
  {"objects": ["can_empty", "K_trash"], "interaction": "place can_empty in K_trash using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["tissue_used"], "interaction": "grasp tissue_used with both hands"},
  {"objects": ["tissue_used", "L_coffee"], "interaction": "lift tissue_used from L_coffee using both hands"},
  {"objects": ["tissue_used", "K_trash"], "interaction": "place tissue_used in K_trash using both hands"},
  {"objects": [], "interaction": "free both hands"}
]"""
baseline_coordinator_scenario_5 = """[
  {"objects": ["CUP_B"], "interaction": "grasp CUP_B with both hands"},
  {"objects": ["CUP_B", "counter"], "interaction": "lift CUP_B from counter using both hands"},
  {"objects": ["CUP_B", "S", "DS"], "interaction": "wash CUP_B in sink S with soap DS"},
  {"objects": ["CUP_B", "DR"], "interaction": "dry CUP_B on rack DR"},
  {"objects": ["CUP_B"], "interaction": "grasp CUP_B with both hands"},
  {"objects": ["CUP_B", "DR"], "interaction": "lift CUP_B from DR using both hands"},
  {"objects": ["CUP_B", "counter"], "interaction": "place CUP_B on counter using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["CM"], "interaction": "press ON button on CM"},
  {"objects": ["CUP_A"], "interaction": "grasp CUP_A with both hands"},
  {"objects": ["CUP_A", "counter"], "interaction": "lift CUP_A from counter using both hands"},
  {"objects": ["CUP_A", "CM"], "interaction": "place CUP_A on CM using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["CM", "CUP_A"], "interaction": "dispense coffee from CM into CUP_A"},
  {"objects": ["CUP_A"], "interaction": "grasp CUP_A with both hands"},
  {"objects": ["CUP_A", "CM"], "interaction": "lift CUP_A from CM using both hands"},
  {"objects": ["CUP_A", "counter"], "interaction": "place CUP_A on counter using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["CUP_B"], "interaction": "grasp CUP_B with both hands"},
  {"objects": ["CUP_B", "counter"], "interaction": "lift CUP_B from counter using both hands"},
  {"objects": ["CUP_B", "CM"], "interaction": "place CUP_B on CM using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["CM", "CUP_B"], "interaction": "dispense coffee from CM into CUP_B"},
  {"objects": ["CUP_B"], "interaction": "grasp CUP_B with both hands"},
  {"objects": ["CUP_B", "CM"], "interaction": "lift CUP_B from CM using both hands"},
  {"objects": ["CUP_B", "counter"], "interaction": "place CUP_B on counter using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["SJ"], "interaction": "open container SJ"},
  {"objects": ["SJ", "CUP_B"], "interaction": "scoop sugar from SJ into CUP_B"},
  {"objects": ["SJ"], "interaction": "close container SJ"},
  {"objects": ["F"], "interaction": "open container F"},
  {"objects": ["MC"], "interaction": "grasp MC with both hands"},
  {"objects": ["MC", "F"], "interaction": "lift MC from F using both hands"},
  {"objects": ["F"], "interaction": "close container F"},
  {"objects": ["MC", "CUP_B"], "interaction": "pour from MC into CUP_B"},
  {"objects": ["F"], "interaction": "open container F"},
  {"objects": ["MC", "F"], "interaction": "place MC in F using both hands"},
  {"objects": [], "interaction": "free both hands"},
  {"objects": ["F"], "interaction": "close container F"},
  {"objects": ["CM"], "interaction": "press OFF button on CM"}
]"""