# VHS Cleanup Silent Video

A tiny ComfyUI custom node that deletes the silent video file left behind by
[ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)'s
**Video Combine** node.

## The problem

When you feed audio into **Video Combine**, VHS writes **three** files:

- a `.png` (first frame, used for metadata)
- a silent video (no audio)
- the same video muxed with audio, suffixed `-audio`

The silent video is only an internal intermediate step (VHS renders it first,
then muxes audio into a second file), but VHS never cleans it up. If you only
care about the version with audio, you end up with a redundant duplicate
video for every generation.

There's currently no built-in toggle for this in VideoHelperSuite - see
[Kosinkadink/ComfyUI-VideoHelperSuite#130](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/issues/130)
and [#260](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/issues/260).

## What this node does

`VHS_CleanupSilentVideo` connects to the **Filenames** output of Video
Combine. After Video Combine has finished writing both files, it deletes any
video file that does **not** have an `-audio` suffix, but **only if** a
matching `-audio` file with the same base name exists in the same run.

That safety check matters: if you render a video with no audio track at all
(e.g. plain Wan 2.2 output), there is no `-audio` counterpart, so the node
leaves the single silent video alone instead of deleting your only output.

The `.png` metadata file is not touched.

## Installation

1. Clone this repo into your `ComfyUI/custom_nodes/` folder:
   ```
   cd ComfyUI/custom_nodes
   git clone https://github.com/VRAM-Hoarder/vhs-cleanup-silent-video.git
   ```
2. Restart ComfyUI.

## Usage

In your workflow, connect the **Filenames** output of **Video Combine**
(VHS_VideoCombine) to the **filenames** input of **Cleanup Silent Video
(VHS)**.

```
[Video Combine] --Filenames--> [Cleanup Silent Video (VHS)]
```

That's it - no other settings. The node has no outputs; it's a pure
side-effect / cleanup step.

## Notes

- Works with batched runs via `VHS_BatchManager`: while a batch is still in
  progress, Video Combine returns an empty filename list, so the cleanup
  simply does nothing until the final, completed batch is processed.
- This is an independent, unofficial helper node and is not affiliated with
  or endorsed by the ComfyUI-VideoHelperSuite project.

## License

MIT, see [LICENSE](LICENSE).
