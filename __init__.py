from .prepare_control_video import PrepareControlVideo
from .latest_video_from_folder import LatestVideoFromFolder
from .cyclic_prompt_from_list import CyclicCharacterAndBackgroundPrompt


NODE_CLASS_MAPPINGS = {
    "PrepareControlVideo": PrepareControlVideo,
    "LatestVideoFromFolder": LatestVideoFromFolder,
    "CyclicCharacterAndBackgroundPrompt": CyclicCharacterAndBackgroundPrompt,
    }
