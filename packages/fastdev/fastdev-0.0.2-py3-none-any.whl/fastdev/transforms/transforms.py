from typing import Optional, Tuple, Union, overload

import torch


def transform(pts: torch.Tensor, tf_mat: torch.Tensor) -> torch.Tensor:
    """
    Apply a transformation matrix on a set of 3D points.

    Args:
        pts: 3D points, could be [..., N, 3]
        tf_mat: Transformation matrix, could be [..., 4, 4]

        The dimension number of pts and tf_mat should be the same.

    Returns:
        Transformed pts.
    """
    if pts.ndim != tf_mat.ndim:
        raise ValueError("The dimension number of pts and tf_mat should be the same.")

    homo_pts = to_homo(pts)
    # `homo_pts @ tf_mat.T` or `(tf_mat @ homo_pts.T).T`
    new_pts = torch.matmul(homo_pts, torch.transpose(tf_mat, -2, -1))
    return new_pts[..., :3]


def rotate(pts: torch.Tensor, rot_mat: torch.Tensor) -> torch.Tensor:
    """
    Apply a rotation matrix on a set of 3D points.

    Args:
        pts: 3D points, could be [..., N, 3]
        rot_mat: Rotation matrix, could be [..., 3, 3]

        The dimension number of pts and rot_mat should be the same.

    Returns:
        Rotated pts.
    """
    if pts.ndim != rot_mat.ndim:
        raise ValueError(
            f"The dimension number of pts and rot_mat should be the same, but got {pts.ndim=} and {rot_mat.ndim=}"
        )

    # `pts @ rot_mat.T` or `(rot_mat @ pts.T).T`
    new_pts = torch.matmul(pts, torch.transpose(rot_mat, -2, -1))
    return new_pts


@overload
def project(pts: torch.Tensor, intr_mat: torch.Tensor, return_depth: bool = False) -> torch.Tensor: ...


@overload
def project(
    pts: torch.Tensor, intr_mat: torch.Tensor, return_depth: bool = True
) -> Tuple[torch.Tensor, torch.Tensor]: ...


def project(
    pts: torch.Tensor, intr_mat: torch.Tensor, return_depth: bool = False
) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
    """
    Project 3D points in the camera space to the image plane.

    Args:
        pts: 3D points, could be Nx3 or BxNx3.
        intr_mat: Intrinsic matrix, could be 3x3 or Bx3x3.

    Returns:
        pixels: the order is uv other than xy.
        depth (if return_depth): depth in the camera space.
    """
    pts = torch.clone(pts)
    new_pts = pts / pts[..., 2:3]
    new_pts = torch.matmul(new_pts, torch.transpose(intr_mat, -2, -1))

    if not return_depth:
        return new_pts[..., :2]
    else:
        return new_pts[..., :2], pts[..., 2]


def unproject(pixels, depth, intr_mat):
    """
    Unproject pixels in the image plane to 3D points in the camera space.

    Args:
        pixels: Pixels in the image plane, could be Nx2 or BxNx2. The order is uv rather than xy.
        depth: Depth in the camera space, could be N, Nx1, BxN or BxNx1.
        intr_mat: Intrinsic matrix, could be 3x3 or Bx3x3.
    Returns:
        pts: 3D points, Nx3 or BxNx3.
    """
    if depth.ndim < pixels.ndim:
        depth = depth[..., None]  # N -> Nx1, BxN -> BxNx1
    principal_point = torch.unsqueeze(intr_mat[..., :2, 2], dim=-2)  # 1x2, Bx1x2
    focal_length = torch.cat([intr_mat[..., 0:1, 0:1], intr_mat[..., 1:2, 1:2]], dim=-1)  # 1x2, Bx1x2
    xys = (pixels - principal_point) * depth / focal_length
    pts = torch.cat([xys, depth], dim=-1)
    return pts


# Ref: https://math.stackexchange.com/a/1315407/757569
def inverse(rot_or_tf_mat: torch.Tensor) -> torch.Tensor:
    if rot_or_tf_mat.shape[-1] == 3:  # rotation matrix
        new_mat = torch.transpose(rot_or_tf_mat, -2, -1)
    else:  # transformation matrix
        new_rot_mat = torch.transpose(rot_or_tf_mat[..., :3, :3], -2, -1)
        ori_tl = torch.unsqueeze(rot_or_tf_mat[..., :3, 3], dim=-2)  # 1x3, Bx1x3
        new_tl = torch.squeeze(-rotate(ori_tl, new_rot_mat), dim=-2)  # 3, Bx3
        new_mat = rot_tl_to_tf_mat(new_rot_mat, new_tl)
    return new_mat


# Ref: https://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/geometry/row-major-vs-column-major-vector # noqa
def swap_major(rot_or_tf_mat: torch.Tensor) -> torch.Tensor:
    return torch.transpose(rot_or_tf_mat, -2, -1)


def rot_tl_to_tf_mat(rot_mat: torch.Tensor, tl: Optional[torch.Tensor] = None) -> torch.Tensor:
    """
    Build transformation matrix with rotation matrix and translation vector.

    Args:
        rot_mat: rotation matrix, could be ...x3x3.
        tl: translation vector, could be ...x3. If None, translation will be 0.
    Returns:
        tf_mat, transformation matrix.
    """

    tf_mat = torch.eye(4, device=rot_mat.device, dtype=rot_mat.dtype).repeat(rot_mat.shape[:-2] + (1, 1))
    tf_mat[..., :3, :3] = rot_mat
    if tl is not None:
        tf_mat[..., :3, 3] = tl
    return tf_mat


def to_homo(pts_3d: torch.Tensor) -> torch.Tensor:
    """
    Convert Cartesian 3D points to Homogeneous 4D points.

    Args:
      pts_3d: 3D points in Cartesian coord, could be ...x3.
    Returns:
      ...x4 points in the Homogeneous coord.
    """
    return torch.cat([pts_3d, torch.ones_like(pts_3d[..., :1])], dim=-1)


def expand_tf_mat(tf_mat: torch.Tensor) -> torch.Tensor:
    """
    Expand transformation matrix to [..., 4, 4].

    Args:
        tf_mat: transformation matrix, could be ...x3x4 or ...x4x4.

    Returns:
        tf_mat, expanded transformation matrix.
    """
    if tf_mat.shape[-2:] == (3, 4):
        tf_mat = torch.cat(
            [
                tf_mat,
                torch.tensor([0.0, 0.0, 0.0, 1.0], dtype=tf_mat.dtype, device=tf_mat.device).repeat(
                    tf_mat.shape[:-2] + (1, 1)
                ),
            ],
            dim=-2,
        )
    return tf_mat
