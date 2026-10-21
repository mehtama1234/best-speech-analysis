# Data and large-artifact policy

This repository keeps source code, notes, and durable speech-analysis metadata in Git.

Large durable artifacts under `research/` use Git LFS. After cloning, run:

```bash
git lfs install
git lfs pull
```

The `data/audio/` and `data/video/` directories contain raw media and are not part of the durable Git backup policy. Reproducible caches, temporary downloads, and generated outputs should remain untracked.
