import os
from typing import Literal

from fastdev.constants import FDEV_GH_CACHE_ROOT, URDF_GH_REPO

URDF_PATHS = Literal[
    "hands/allegro_hand/allegro_hand_left.urdf",
    "hands/allegro_hand/allegro_hand_right.urdf",
    "hands/shadow_hand/shadow_hand_left.urdf",
    "hands/shadow_hand/shadow_hand_right.urdf",
]


def get_local_urdf_path(urdf_path: URDF_PATHS) -> str:
    urdf_repo_dir = os.path.join(FDEV_GH_CACHE_ROOT, "dex-urdf")
    if not os.path.exists(urdf_repo_dir):
        from git import Repo  # lazy import here

        print(f"URDF repo not found, cloning from {URDF_GH_REPO} to {urdf_repo_dir}...")
        os.makedirs(os.path.dirname(urdf_repo_dir), exist_ok=True)
        Repo.clone_from(URDF_GH_REPO, urdf_repo_dir, depth=1)
        print("URDF repo cloned")

    full_urdf_path = os.path.join(urdf_repo_dir, "robots", urdf_path)
    if not os.path.exists(full_urdf_path):
        raise FileNotFoundError(f"{urdf_path} not found in {urdf_repo_dir}, please check the path.")

    return full_urdf_path
