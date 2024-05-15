"""Convert BEVFormer results to nuScenes format."""

import json
import pickle
from tqdm import tqdm

import numpy as np

from nuscenes import NuScenes as NuScenesDevkit
from nuscenes.utils.splits import create_splits_scenes
from nuscenes.utils.data_classes import Box
from nuscenes.utils.data_classes import Quaternion

from vis4d.common.array import array_to_numpy
from vis4d.data.datasets.nuscenes import _get_extrinsics

# data_root = "data/nuscenes_mini"
# version = "v1.0-mini"
# split = "mini_val"

# data_root = "data/nuscenes"
# version = "v1.0-trainval"
# split = "test"

data_root = "data/nuscenes"
version = "v1.0-test"
split = "test"

bevformer_cats_mapping = {
    0: "car",
    1: "truck",
    2: "construction_vehicle",
    3: "bus",
    4: "trailer",
    5: "barrier",
    6: "motorcycle",
    7: "bicycle",
    8: "pedestrian",
    9: "traffic_cone",
}

DefaultAttribute = {
    "car": "vehicle.parked",
    "pedestrian": "pedestrian.moving",
    "trailer": "vehicle.parked",
    "truck": "vehicle.parked",
    "bus": "vehicle.moving",
    "motorcycle": "cycle.without_rider",
    "construction_vehicle": "vehicle.parked",
    "bicycle": "cycle.without_rider",
    "barrier": "",
    "traffic_cone": "",
}


def get_attributes(name: str, velocity: list[float]) -> str:
    """Get nuScenes attributes."""
    if np.sqrt(velocity[0] ** 2 + velocity[1] ** 2) > 0.2:
        if name in {
            "car",
            "construction_vehicle",
            "bus",
            "truck",
            "trailer",
        }:
            attr = "vehicle.moving"
        elif name in {"bicycle", "motorcycle"}:
            attr = "cycle.with_rider"
        else:
            attr = DefaultAttribute[name]
    elif name in {"pedestrian"}:
        attr = "pedestrian.standing"
    elif name in {"bus"}:
        attr = "vehicle.stopped"
    else:
        attr = DefaultAttribute[name]
    return attr


data = NuScenesDevkit(version=version, dataroot=data_root, verbose=False)
scene_names_per_split = create_splits_scenes()
scenes = [
    scene for scene in data.scene if scene["name"] in scene_names_per_split[split]
]

detect_3d = {}

for scene in tqdm(scenes):
    scene_name = scene["name"]

    sample_token = scene["first_sample_token"]
    while sample_token:
        annos = []
        sample = data.get("sample", sample_token)

        token = sample["token"]

        lidar_token = sample["data"]["LIDAR_TOP"]
        lidar_data = data.get("sample_data", lidar_token)

        calibration_lidar = data.get(
            "calibrated_sensor", lidar_data["calibrated_sensor_token"]
        )

        ego_pose = data.get("ego_pose", lidar_data["ego_pose_token"])

        extrinsics = _get_extrinsics(ego_pose, calibration_lidar)

        with open(f"vis4d-workspace/bevformer_base/old/{token}.pkl", "rb") as f:
            # x, y, z, w, l, h, yaw, vx, vy, score, label
            bevformer_boxes = pickle.load(f)

        boxes_3d_np = array_to_numpy(bevformer_boxes, n_dims=None, dtype=np.float32)

        if len(boxes_3d_np) != 0:
            for box_3d in boxes_3d_np:
                category = bevformer_cats_mapping[int(box_3d[10])]

                translation = box_3d[0:3].tolist()
                dimension = box_3d[3:6].tolist()
                rotation = Quaternion(axis=[0, 0, 1], radians=box_3d[6])

                velocity_list = box_3d[7:9].tolist()

                attribute_name = get_attributes(category, velocity_list)

                box = Box(
                    translation,
                    dimension,
                    rotation,
                    label=int(box_3d[10]),
                    score=float(box_3d[9]),
                    velocity=(box_3d[7], box_3d[8], 0.0),
                )

                box.rotate(Quaternion._from_matrix(extrinsics[:3, :3], atol=1))
                box.translate(extrinsics[:3, 3])

                nusc_anno = {
                    "sample_token": token,
                    "translation": box.center.tolist(),
                    "size": box.wlh.tolist(),
                    "rotation": box.orientation.elements.tolist(),
                    "velocity": box.velocity.tolist()[:2],
                    "detection_name": category,
                    "detection_score": box.score,
                    "attribute_name": attribute_name,
                }
                annos.append(nusc_anno)

        detect_3d[token] = annos
        sample_token = sample["next"]

nusc_annos = {
    "results": detect_3d,
    "meta": {
        "use_camera": True,
        "use_lidar": False,
        "use_radar": False,
        "use_map": False,
        "use_external": False,
    },
}

with open(
    "vis4d-workspace/detect_3d/bevformer_base_test.json", mode="w", encoding="utf-8"
) as f:
    json.dump(nusc_annos, f)
