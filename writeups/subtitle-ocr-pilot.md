# Recovering visible subtitles without calling them spoken words

Region-first OCR matches the displayed English subtitle text on all three
previously inspected frames. The initial whole-frame approach failed on each:
it omitted text, confused scene content with text, or lost punctuation. Both
outputs are preserved in the [OCR report](../research/subtitle-ocr-pilot.json).

Restricting the image region before recognition made the difference. Filtering
word boxes afterward was insufficient because the scene had already affected
segmentation. The revised path uses the subtitle rectangle, enlarges it twofold
in memory and recognizes it as one text block. Original images are untouched.
Boxes are mapped back to source coordinates; engine confidence is uncalibrated.

## Evidence boundaries

The assistant compared outputs at 60.026633, 100.033267 and 378.010967 seconds
with frames directly inspected earlier. The [review record](../research/subtitle-ocr-review.json)
binds that judgment to exact report bytes. There is no independent reviewer or
held-out accuracy result: the rectangle was selected after seeing these frames.
It may fail when subtitles move, wrap, disappear or overlap graphics.

An OCR record describes editorial text visible at a frame time, not display
duration, exact spoken words, speech rate or audio alignment. The audience-shot
example retains its visual attribution warning. No reconstructed transcript
replaces the quarantined language candidate or changes corpus statistics.

## Local runtime

No system package was installed. Four Ubuntu packages were downloaded and
unpacked inside ignored `data/cache/ocr-runtime/`: Tesseract 4.1.1, its library,
Leptonica and English language data. The report hashes packages, executable,
local libraries and trained data and records the OpenCV version. This is a
pilot runtime, not a production dependency/security recommendation.

To reproduce in this Ubuntu environment, from the repository root:

```bash
mkdir -p data/cache/ocr-runtime/debs data/cache/ocr-runtime/root
cd data/cache/ocr-runtime/debs
apt-get download tesseract-ocr libtesseract4 liblept5 tesseract-ocr-eng
cd ../../../..
for package in data/cache/ocr-runtime/debs/*.deb; do
  dpkg-deb -x "$package" data/cache/ocr-runtime/root
done
python3 scripts/ocr_language_verification_frames.py
```

Compare downloaded package versions/hashes with the report; repositories may
change. OpenCV is the existing Python dependency. Library search settings apply
only to the OCR subprocess. Ignored runtime/media files may be absent on a clone.

Next: freeze preprocessing and test previously uninspected timestamps, including
no-subtitle frames. Measure omissions, insertions and layout failures before
continuous extraction. Three selected successes are not a corpus accuracy estimate.
