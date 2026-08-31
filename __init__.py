import os


class VHS_CleanupSilentVideo:
    """
    Deletes the silent video file that VHS_VideoCombine (ComfyUI-VideoHelperSuite)
    additionally writes whenever an audio track is muxed in.

    VHS_VideoCombine always renders a video without audio first and, if audio
    is connected, muxes a second file with an "-audio" suffix on top of it.
    The silent intermediate file is never removed by VHS itself.

    Connect the "Filenames" output of Video Combine to this node's input.
    A silent video is only deleted if a matching "-audio" file with the same
    base name exists in the same run - so plain videos rendered without any
    audio input (e.g. Wan 2.2 without an audio source) are left untouched.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "filenames": ("VHS_FILENAMES",),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    CATEGORY = "Video Helper Suite 🎥🅥🅗🅢/cleanup"
    FUNCTION = "cleanup"

    def cleanup(self, filenames):
        # filenames = (save_output_bool, [list_of_paths])
        save_output, files = filenames
        video_exts = (".mp4", ".webm", ".mov", ".mkv", ".gif", ".webp")

        # Collect (directory, base_name_without_"-audio", ext) for every
        # "-audio" file present. A silent file is only redundant if a
        # matching audio counterpart actually exists.
        audio_stems = set()
        for path in files:
            directory, filename = os.path.split(path)
            name, ext = os.path.splitext(filename)
            if ext.lower() in video_exts and name.endswith("-audio"):
                stem = name[: -len("-audio")]
                audio_stems.add((directory, stem, ext.lower()))

        for path in files:
            directory, filename = os.path.split(path)
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext not in video_exts or name.endswith("-audio"):
                continue
            # Only delete if a matching "-audio" file exists in this run.
            if (directory, name, ext) not in audio_stems:
                continue
            try:
                os.remove(path)
                print(f"VHS_CleanupSilentVideo: deleted -> {path}")
            except OSError as e:
                print(f"VHS_CleanupSilentVideo: could not delete {path}: {e}")

        return {}


NODE_CLASS_MAPPINGS = {
    "VHS_CleanupSilentVideo": VHS_CleanupSilentVideo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VHS_CleanupSilentVideo": "Cleanup Silent Video (VHS)",
}
