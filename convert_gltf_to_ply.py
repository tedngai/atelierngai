#!/usr/bin/env python3
"""
Convert a GLTF point cloud (scene.gltf + scene.bin) to a downsampled PLY file.

Reads all VEC3 positions and VEC4 colors from the GLTF binary buffer,
applies node transforms (rotation, scale, translation), randomly samples
down to a target point count, and writes a binary PLY file.

Usage:
    python convert_gltf_to_ply.py [--input scene.gltf] [--output scene.ply] [--target 700000]
"""

import json
import struct
import argparse
import numpy as np
from pathlib import Path


def quat_to_matrix(q):
    """Convert quaternion [x, y, z, w] to 3x3 rotation matrix."""
    x, y, z, w = q
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ]
    )


def decompose_matrix4(m):
    """Extract 3x3 rotation+scale and translation from a 4x4 column-major matrix.

    GLTF stores matrices in column-major order:
    m = [m0, m1, m2, m3, m4, m5, ...] ->
        col0 = [m0, m1, m2, m3]
        col1 = [m4, m5, m6, m7]
        ...
    """
    # Reshape to 4x4 column-major
    mat = np.array(m).reshape(4, 4, order="F")
    # Upper-left 3x3 = rotation * scale
    rot_scale = mat[:3, :3]
    # Translation is last column's first 3 rows... wait, column-major
    # In GLTF, the translation is in mat[3, :3] (4th row, first 3 cols) in row-major
    # But since we reshaped column-major: mat[row, col]
    # translation = column 3, rows 0-2
    translation = mat[:3, 3]
    return rot_scale, translation


def build_world_transform(nodes):
    """Build the combined transform from the first 3 nodes (root chain).

    Node 0: rotation quaternion [-0.707, 0, 0, 0.707] (90° around X)
    Node 1: uniform scale 0.745 (via 4x4 matrix)
    Node 2: translation [6.37, 8.70, 5.01] (via 4x4 matrix)
    """
    transform = np.eye(3)
    translation = np.zeros(3)

    for node in nodes:
        if "matrix" in node:
            mat = np.array(node["matrix"]).reshape(4, 4, order="F")
            rs = mat[:3, :3]
            t = mat[:3, 3]
            transform = rs @ transform
            translation = rs @ translation + t
        elif "rotation" in node:
            r = quat_to_matrix(node["rotation"])
            transform = r @ transform
            # No translation in rotation-only nodes
        elif "translation" in node:
            t = np.array(node["translation"][:3])
            translation = translation + t
        elif "scale" in node:
            s = np.diag(node["scale"][:3])
            transform = s @ transform

    return transform, translation


def read_accessor_positions(bin_data, accessor, buffer_view):
    """Read VEC3 float positions from a binary buffer."""
    stride = buffer_view["byteStride"]
    bv_offset = buffer_view["byteOffset"]
    acc_offset = accessor.get("byteOffset", 0)
    count = accessor["count"]
    start = bv_offset + acc_offset

    positions = np.zeros((count, 3), dtype=np.float32)
    for i in range(count):
        offset = start + i * stride
        positions[i] = struct.unpack_from("fff", bin_data, offset)
    return positions


def read_accessor_colors(bin_data, accessor, buffer_view):
    """Read VEC4 float colors from a binary buffer."""
    stride = buffer_view["byteStride"]
    bv_offset = buffer_view["byteOffset"]
    acc_offset = accessor.get("byteOffset", 0)
    count = accessor["count"]
    start = bv_offset + acc_offset

    colors = np.zeros((count, 4), dtype=np.float32)
    for i in range(count):
        offset = start + i * stride
        colors[i] = struct.unpack_from("ffff", bin_data, offset)
    return colors


def main():
    parser = argparse.ArgumentParser(
        description="Convert GLTF point cloud to downsampled PLY"
    )
    parser.add_argument("--input", default="3d/scene.gltf", help="Path to .gltf file")
    parser.add_argument(
        "--output",
        default="assets/pointcloud/scene.ply",
        help="Path to output .ply file",
    )
    parser.add_argument("--target", type=int, default=700000, help="Target point count")
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    bin_path = input_path.parent / "scene.bin"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading {input_path}...")
    with open(input_path) as f:
        gltf = json.load(f)

    print(f"Reading {bin_path} ({bin_path.stat().st_size / 1e6:.1f} MB)...")
    with open(bin_path, "rb") as f:
        bin_data = f.read()

    buffer_views = gltf["bufferViews"]
    accessors = gltf["accessors"]
    nodes = gltf["nodes"]
    meshes = gltf["meshes"]

    # Build world transform from root node chain
    transform, translation = build_world_transform(nodes[:3])
    print(f"Transform matrix:\n{transform}")
    print(f"Translation: {translation}")

    # Process all meshes — collect positions and colors
    total_points = sum(
        meshes[i]["primitives"][0]["attributes"]["POSITION"] for i in range(len(meshes))
    )
    # Just count via accessors
    total_points = sum(
        accessors[meshes[i]["primitives"][0]["attributes"]["POSITION"]]["count"]
        for i in range(len(meshes))
    )
    print(f"Total points across {len(meshes)} meshes: {total_points:,}")

    # Read all points into arrays
    print("Extracting positions and colors...")
    all_positions = []
    all_colors = []

    for i, mesh in enumerate(meshes):
        attrs = mesh["primitives"][0]["attributes"]
        pos_acc = accessors[attrs["POSITION"]]
        col_acc = accessors[attrs["COLOR_0"]]

        pos_bv = buffer_views[pos_acc["bufferView"]]
        col_bv = buffer_views[col_acc["bufferView"]]

        positions = read_accessor_positions(bin_data, pos_acc, pos_bv)
        colors = read_accessor_colors(bin_data, col_acc, col_bv)

        all_positions.append(positions)
        all_colors.append(colors)

        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(meshes)} meshes...")

    all_positions = np.concatenate(all_positions, axis=0)
    all_colors = np.concatenate(all_colors, axis=0)
    print(
        f"Combined: {all_positions.shape[0]:,} positions, {all_colors.shape[0]:,} colors"
    )

    # Apply transforms to positions
    print("Applying transforms...")
    all_positions = (transform @ all_positions.T).T + translation

    # Normalize colors: GLTF colors may be 0-1 float, convert to 0-255 uint8
    # Keep RGB only (drop alpha)
    rgb = all_colors[:, :3]
    if rgb.max() <= 1.0:
        rgb = (rgb * 255).astype(np.uint8)
    else:
        rgb = rgb.astype(np.uint8)

    # Downsample
    rng = np.random.default_rng(args.seed)
    n = all_positions.shape[0]
    target = min(args.target, n)

    if target < n:
        print(f"Downsampling {n:,} → {target:,} points (random uniform)...")
        indices = rng.choice(n, size=target, replace=False)
        indices.sort()  # Sort for slightly better memory access patterns
        positions = all_positions[indices]
        colors = rgb[indices]
    else:
        positions = all_positions
        colors = rgb
        print(f"No downsampling needed ({n:,} <= {target:,})")

    del all_positions, all_colors, rgb  # Free memory

    # Center the point cloud
    centroid = positions.mean(axis=0)
    positions -= centroid
    print(f"Centered at origin (was at {centroid})")

    # Compute bounds
    mins = positions.min(axis=0)
    maxs = positions.max(axis=0)
    print(
        f"Bounds: x=[{mins[0]:.2f}, {maxs[0]:.2f}] y=[{mins[1]:.2f}, {maxs[1]:.2f}] z=[{mins[2]:.2f}, {maxs[2]:.2f}]"
    )

    # Write binary PLY
    print(f"Writing {output_path}...")
    num_points = positions.shape[0]

    with open(output_path, "wb") as f:
        # Header
        header = (
            f"ply\n"
            f"format binary_little_endian 1.0\n"
            f"element vertex {num_points}\n"
            f"property float x\n"
            f"property float y\n"
            f"property float z\n"
            f"property uchar red\n"
            f"property uchar green\n"
            f"property uchar blue\n"
            f"end_header\n"
        )
        f.write(header.encode("ascii"))

        # Interleave position + color and write
        # Pack as: float x, float y, float z, uchar r, uchar g, uchar b
        for i in range(num_points):
            f.write(
                struct.pack(
                    "fffBBB",
                    positions[i, 0],
                    positions[i, 1],
                    positions[i, 2],
                    colors[i, 0],
                    colors[i, 1],
                    colors[i, 2],
                )
            )

    print(f"Done! {num_points:,} points written to {output_path}")
    print(f"File size: {output_path.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
