# lif_stitching

**Stitch Leica `.lif` tile scans (Z/T/C‑aware) into analysis‑ready mosaics.**

## What & why
Use this to restitch Leica LAS X `.lif` tile scans with your own Z‑projection and per‑channel handling, producing clean mosaics for downstream quantification. You can also export the vendor mosaic for quick QA/visual comparison.

## Assumptions about `.lif`
- Series **0** → all **tiles** (address with `m`).
- Series **1** → **vendor** pre‑stitched mosaic (optional).
- Frames are indexed `(z, t, c, m)`; most datasets have `t = 0`.

## Quick start
1) Put one or more `.lif` files into `./src/`  
2) Run:
```bash
python main.py
```
3) See outputs in `./out/<lif_name>/`:
- `mosaics/<channel>_mosaic.tif` (stitched per channel)
- `tiles/<channel>_tile-<m>.tif` (projected tiles used for stitching)
- `debug/*.png` (optional match/layout visuals)
- `vendor/vendor_mosaic.tif` (if present in series 1)

## Configure
- **Z strategy**: choose brightest‑Z (`brightestZ.py`) or max‑projection (`mergeZstack.py`).
- **Stitching**: tweak OpenCV settings in `stitching.py`.
- **Channels & names**: set indices and friendly names in your driver code.
- **Series**: adjust in `lif_processer.py` if your `.lif` ordering differs.

## Requirements
Python 3.9+. Suggested packages:
```bash
pip install numpy opencv-python tifffile imagecodecs readlif
# If readlif doesn’t work: pip install pylifreader
```

## Tips
- Ensure sufficient tile overlap and texture for robust stitching.
- Z‑project before stitching to reduce memory and improve alignment.

## License
MIT (see `LICENSE`).
