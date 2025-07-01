import json
import os

STATE_FILE = "cyclic_prompt_indices.json"

class CyclicCharacterAndBackgroundPrompt:
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True  # Always re-executes
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character_prompts": ("STRING", {
                    "multiline": True,
                    "default": '"A knight", "A samurai", "A wizard"]'
                }),
                "background_prompts": ("STRING", {
                    "multiline": True,
                    "default": '"in a forest", "on a mountain", "in a dungeon"]'
                }),
                "additional_prompts": ("STRING", {
                    "multiline": True,
                    "default": '"cinematic lighting", "highly detailed", "photorealistic"]'
                }),
                "trigger": ("INT", {"default": 0})  # dummy input to force evaluation
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_prompt",)
    FUNCTION = "get_next_prompts"
    CATEGORY = "utils"
    OUTPUT_NODE = True  # optional: treat as important downstream    
    def get_next_prompts(self, character_prompts, background_prompts, additional_prompts, trigger):
        try:
            char_list = json.loads(character_prompts)
            bg_list = json.loads(background_prompts)
            add_list = json.loads(additional_prompts)

            if not isinstance(char_list, list) or not all(isinstance(p, str) for p in char_list):
                raise ValueError("Character prompt must be a JSON array of strings")
            if not isinstance(bg_list, list) or not all(isinstance(p, str) for p in bg_list):
                raise ValueError("Background prompt must be a JSON array of strings")
            if not isinstance(add_list, list) or not all(isinstance(p, str) for p in add_list):
                raise ValueError("Additional prompt must be a JSON array of strings")

        except Exception:
            raise ValueError("Invalid JSON input")        
        # Load saved indices
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                char_idx = state.get("char_idx", 0)
                bg_idx = state.get("bg_idx", 0)
                add_idx = state.get("add_idx", 0)
        else:
            char_idx = bg_idx = add_idx = 0
        
        char_prompt = char_list[char_idx % len(char_list)] if char_list else ""
        bg_prompt = bg_list[bg_idx % len(bg_list)] if bg_list else ""
        add_prompt = add_list[add_idx % len(add_list)] if add_list else ""

        # Update and save indices
        with open(STATE_FILE, "w") as f:
            json.dump({
                "char_idx": (char_idx + 1) % len(char_list) if char_list else 0,
                "bg_idx": (bg_idx + 1) % len(bg_list) if bg_list else 0,
                "add_idx": (add_idx + 1) % len(add_list) if add_list else 0,
            }, f)

        merged = f"{char_prompt}. In the background: {bg_prompt}."
        if add_prompt:
            merged += f"{add_prompt}"
            
        print(f"Generated prompt: {merged}")
        return (merged,)

NODE_CLASS_MAPPINGS = {
    "CyclicCharacterAndBackgroundPrompt": CyclicCharacterAndBackgroundPrompt
}
