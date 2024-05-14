import json

from pydantic import Field

from creator.base.base_request import BaseRequest

default_workflow_json = {
    "3": {
        "inputs": {
            "seed": 985289875893903,
            "steps": 20,
            "cfg": 7.5,
            "sampler_name": "dpmpp_2m_sde",
            "scheduler": "karras",
            "denoise": 1,
            "model": [
                "4",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "latent_image": [
                "5",
                0
            ]
        },
        "class_type": "KSampler",
        "_meta": {
            "title": "KSampler"
        }
    },
    "4": {
        "inputs": {
            "ckpt_name": "Juggernaut-XI-Prototype.safetensors"
        },
        "class_type": "CheckpointLoaderSimple",
        "_meta": {
            "title": "Load Checkpoint"
        }
    },
    "5": {
        "inputs": {
            "width": 1024,
            "height": 768,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage",
        "_meta": {
            "title": "Empty Latent Image"
        }
    },
    "6": {
        "inputs": {
            "text": "a photograph of a smiling green alien holding a sign which says \"Run Diffusion\", ultra realistic, street, city, sci-fi, ultra realistic, cute, friendly",
            "clip": [
                "4",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "7": {
        "inputs": {
            "text": "blurry, low quality",
            "clip": [
                "4",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "8": {
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        },
        "class_type": "VAEDecode",
        "_meta": {
            "title": "VAE Decode"
        }
    },
    "9": {
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        },
        "class_type": "SaveImage",
        "_meta": {
            "title": "Save Image"
        }
    }
}

default_workflow_json_2 = {
  "4": {
    "inputs": {
      "ckpt_name": "Juggernaut-XI-Prototype.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "21": {
    "inputs": {
      "width": 2432,
      "height": 1664,
      "batch_size": 2
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Image Size\n"
    }
  },
  "67": {
    "inputs": {
      "samples": [
        "132",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "69": {
    "inputs": {
      "images": [
        "67",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Output"
    }
  },
  "99": {
    "inputs": {
      "seed": 1042340763738557
    },
    "class_type": "CR Seed",
    "_meta": {
      "title": "🌱 CR Seed"
    }
  },
  "100": {
    "inputs": {
      "text": [
        "114:0",
        0
      ],
      "seed": 1116260329,
      "log_prompt": "No"
    },
    "class_type": "PromptExpansion",
    "_meta": {
      "title": "Prompt Expansion"
    }
  },
  "101": {
    "inputs": {
      "text": [
        "100",
        0
      ]
    },
    "class_type": "ShowText|pysssss",
    "_meta": {
      "title": "Final Positive Prompt"
    }
  },
  "102": {
    "inputs": {
      "text": [
        "114:1",
        0
      ]
    },
    "class_type": "ShowText|pysssss",
    "_meta": {
      "title": "Final Negative Prompt"
    }
  },
  "120": {
    "inputs": {
      "b1": 1.01,
      "b2": 1.02,
      "s1": 0.99,
      "s2": 0.9500000000000001,
      "model": [
        "4",
        0
      ]
    },
    "class_type": "FreeU_V2",
    "_meta": {
      "title": "FreeU_V2"
    }
  },
  "132": {
    "inputs": {
      "add_noise": True,
      "noise_seed": [
        "99",
        0
      ],
      "steps": 20,
      "cfg": 5,
      "sampler_name": "dpmpp_2m",
      "scheduler": "AYS SDXL",
      "start_at_step": 0,
      "end_at_step": 10000,
      "noise_mode": "GPU(=A1111)",
      "return_with_leftover_noise": False,
      "batch_seed_mode": "incremental",
      "variation_seed": 0,
      "variation_strength": 0,
      "model": [
        "134",
        0
      ],
      "positive": [
        "98:0",
        0
      ],
      "negative": [
        "98:1",
        0
      ],
      "latent_image": [
        "21",
        0
      ]
    },
    "class_type": "KSamplerAdvanced //Inspire",
    "_meta": {
      "title": "KSamplerAdvanced (inspire)"
    }
  },
  "134": {
    "inputs": {
      "ds_depth_1": 3,
      "ds_depth_2": 3,
      "ds_timestep_1": 900,
      "ds_timestep_2": 650,
      "resize_scale_1": 2,
      "resize_scale_2": 2,
      "model": [
        "120",
        0
      ]
    },
    "class_type": "Hires",
    "_meta": {
      "title": "Apply Kohya's HiresFix"
    }
  },
  "119:0": {
    "inputs": {
      "text_positive": "",
      "text_negative": "",
      "style": "Fooocus Photograph",
      "log_prompt": True,
      "style_positive": True,
      "style_negative": True
    },
    "class_type": "SDXLPromptStyler",
    "_meta": {
      "title": "SDXL Prompt Styler"
    }
  },
  "119:1": {
    "inputs": {
      "text_positive": "",
      "text_negative": "",
      "style": "Fooocus Enhance",
      "log_prompt": True,
      "style_positive": True,
      "style_negative": True
    },
    "class_type": "SDXLPromptStyler",
    "_meta": {
      "title": "SDXL Prompt Styler"
    }
  },
  "119:2": {
    "inputs": {
      "text_positive": "",
      "text_negative": "",
      "style": "Fooocus Negative",
      "log_prompt": True,
      "style_positive": True,
      "style_negative": True
    },
    "class_type": "SDXLPromptStyler",
    "_meta": {
      "title": "SDXL Prompt Styler"
    }
  },
  "133:0": {
    "inputs": {
      "text1": "a close-up shot of a soldier running on the battlefield, world war 2, gritty, dust, explosions",
      "text2": [
        "119:0",
        0
      ],
      "separator": ", "
    },
    "class_type": "CR Text Concatenate",
    "_meta": {
      "title": "Concat Positive"
    }
  },
  "133:1": {
    "inputs": {
      "text1": "blurry eyes, zombie eyes, bad face, too many fingers",
      "text2": [
        "119:0",
        1
      ],
      "separator": ", "
    },
    "class_type": "CR Text Concatenate",
    "_meta": {
      "title": "Concat Negative"
    }
  },
  "133:2": {
    "inputs": {
      "text1": [
        "119:1",
        0
      ],
      "text2": [
        "119:2",
        0
      ],
      "separator": ", "
    },
    "class_type": "CR Text Concatenate",
    "_meta": {
      "title": "Concat Positive"
    }
  },
  "133:3": {
    "inputs": {
      "text1": [
        "119:1",
        1
      ],
      "text2": [
        "119:2",
        1
      ],
      "separator": ", "
    },
    "class_type": "CR Text Concatenate",
    "_meta": {
      "title": "Concat Negative"
    }
  },
  "114:0": {
    "inputs": {
      "text1": [
        "133:0",
        0
      ],
      "text2": [
        "133:2",
        0
      ],
      "separator": ", "
    },
    "class_type": "CR Text Concatenate",
    "_meta": {
      "title": "Concat Positive"
    }
  },
  "114:1": {
    "inputs": {
      "text1": [
        "133:1",
        0
      ],
      "text2": [
        "133:3",
        0
      ],
      "separator": ", "
    },
    "class_type": "CR Text Concatenate",
    "_meta": {
      "title": "Concat Negative"
    }
  },
  "98:0": {
    "inputs": {
      "text": [
        "101",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "Encode Positive"
    }
  },
  "98:1": {
    "inputs": {
      "text": [
        "102",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "Encode Negative"
    }
  }
}


class CmfyWorkflow(BaseRequest):
    workflow_json: str = Field("", examples=[json.dumps(default_workflow_json)])


class CmfyWorkflowFcus(BaseRequest):
    workflow_json: str = Field("", examples=[json.dumps(default_workflow_json_2)])
