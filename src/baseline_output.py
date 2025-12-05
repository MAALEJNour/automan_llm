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