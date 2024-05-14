import os

# cache
FDEV_CACHE_ROOT = os.path.abspath(os.path.join(os.path.expanduser("~/.cache/fastdev")))

# dataset
FDEV_DATASET_ROOT = os.path.abspath(os.path.join(os.path.expanduser("~"), "data"))
FDEV_PROCESSED_ROOT = os.path.join(FDEV_DATASET_ROOT, "processed")

# huggingface
FDEV_HF_CACHE_ROOT = os.path.join(FDEV_CACHE_ROOT, "hf")  # ~/.cache/fastdev/hf
FDEV_HF_REPO_ID = "jianglongye/fastdev"  # https://huggingface.co/jianglongye/fastdev

# github
FDEV_GH_CACHE_ROOT = os.path.join(FDEV_CACHE_ROOT, "gh")  # ~/.cache/fastdev/gh
URDF_GH_REPO = "https://github.com/dexsuite/dex-urdf.git"
