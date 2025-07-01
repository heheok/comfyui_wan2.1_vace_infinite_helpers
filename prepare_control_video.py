import torch

class PrepareControlVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_frames": ("IMAGE",),  # list or batch
                "tail_count": ("INT", {"default": 15, "min": 1, "max": 256}),
                "pad_count": ("INT", {"default": 46, "min": 0, "max": 256}),
                "width": ("INT", {"default": 640, "min": 1}),
                "height": ("INT", {"default": 640, "min": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE",)
    RETURN_NAMES = ("control_video", "preview_video",)
    FUNCTION = "run"
    CATEGORY = "video_utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False, False)

    def run(self, video_frames, tail_count, pad_count, width, height):
        # Convert batched tensor to list if needed
        if isinstance(video_frames, torch.Tensor) and video_frames.dim() == 4:
            frame_list = list(video_frames)
        elif isinstance(video_frames, list):
            frame_list = video_frames
        else:
            raise ValueError("Invalid input: video_frames must be list or 4D tensor")

        # Sanitize shapes: expect CHW
        for i, f in enumerate(frame_list):
            if f.dim() == 3 and f.shape[0] != 3:
                # Probably HWC, fix it
                frame_list[i] = f.permute(2, 0, 1)

        # Slice last N frames
        tail = frame_list[-tail_count:] if tail_count <= len(frame_list) else frame_list[:]

        # Generate grey frame [3, H, W] RGB(128,128,128) normalized to 0–1
        grey_frame = torch.full((3, height, width), 0.5, dtype=tail[0].dtype, device=tail[0].device)
        grey_frames = [grey_frame.clone() for _ in range(pad_count)]

        # Combine
        all_frames = tail + grey_frames
        batched_chw = torch.stack(all_frames, dim=0)           # [N, 3, H, W] → for control_video
        batched_hw3 = batched_chw.permute(0, 2, 3, 1)          # [N, H, W, 3] → for preview/save

        return (batched_chw, batched_hw3)

NODE_CLASS_MAPPINGS = {
    "PrepareControlVideo": PrepareControlVideo
}
