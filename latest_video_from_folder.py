import os
from pathlib import Path

class LatestVideoFromFolder:
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True  # Force refresh on every run

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {
                    "multiline": False,
                    "default": "./output/videos"
                }),
                "trigger": ("INT", {"default": 0})  # Dummy input to break cache
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("latest_video_path",)
    FUNCTION = "get_latest_video"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def get_latest_video(self, folder_path, trigger):
        folder = Path(folder_path)
        if not folder.is_dir():
            raise ValueError("Provided path is not a valid directory")

        video_files = list(folder.glob("*.mp4"))
        if not video_files:
            raise FileNotFoundError("No .mp4 files found in the folder")

        latest_file = max(video_files, key=lambda f: f.stat().st_mtime)
        print(f"Latest video file: {latest_file}")
        return (str(latest_file),)

NODE_CLASS_MAPPINGS = {
    "LatestVideoFromFolder": LatestVideoFromFolder
}