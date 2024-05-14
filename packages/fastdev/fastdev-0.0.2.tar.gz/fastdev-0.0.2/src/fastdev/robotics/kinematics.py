import os

try:
    import pytorch_kinematics as pk
except ImportError:
    raise ImportError(
        "Please install pytorch_kinematics to use this feature. \nYou can install it by running `pip install pytorch-kinematics`."
    )


def build_kinematics_layer():
    pass
