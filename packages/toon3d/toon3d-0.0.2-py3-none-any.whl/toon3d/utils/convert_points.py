from pathlib import Path
import tyro
import json
import simplejson
import numpy as np
import torch


def convert_points(json_file: str, numpy_dir: str, json_to_numpy: bool):
    if json_to_numpy:
        input_json = Path(json_file).read_text()
        Path(numpy_dir).mkdir(exist_ok=True)
        input_content = json.loads(input_json)

        counter = 0
        for img in input_content:
            points = np.zeros((len(img["points"]), 2), dtype=np.float32)
            for i, point in enumerate(img["points"]):
                points[i] = np.array([point["x"], point["y"]])
            np.save(f"{numpy_dir}/{counter:05d}.npy", points)
            counter += 1
    else:
        output_json = []

        # read from pytorch or numpy
        keypoints_filenames = sorted(list(Path(numpy_dir).glob("*.pt")))
        if len(keypoints_filenames) != 0:
            points_batch = torch.stack([torch.load(kf) for kf in keypoints_filenames]).int()
        else:
            keypoints_filenames = sorted(list(Path(numpy_dir).glob("*.npy")))
            points_batch = torch.stack([torch.from_numpy(np.load(kf)) for kf in keypoints_filenames]).int()

        # parse points to add to json
        for points in points_batch:
            points = [{"x": int(point[0]), "y": int(point[1])} for point in points]
            output_json.append({"points": points})

        # save json
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(output_json, f, indent=2)


tyro.cli(convert_points)
