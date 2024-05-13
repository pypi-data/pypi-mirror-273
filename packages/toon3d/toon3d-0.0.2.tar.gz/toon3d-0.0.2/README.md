# Toon3D

This project enables 3D reconstruction of non-geometrically consistent scenes, such as cartoons. _We take a few images from a cartoon and reconstruct it in 3D._

|   Image 1   |   Image 2   |   Image 3   |
| :------------------------: | :--------------------------: | :-------------------------: |
| ![](toon3d/assets/randm_left.jpeg) | ![](toon3d/assets/randm_center.jpeg) | ![](toon3d/assets/randm_right.jpeg) |

# Setting up the environment

Create a conda environment. 

1. Install the latest nerfstudio package.

2. Then install this codebase as a pip package.

```bash
pip install -e .
```

3. Install the `pytorch3d` package.

```bash
pip install git+https://github.com/facebookresearch/pytorch3d.git
```

4. Optionally, install `torch-batch-svd`:

```bash
pip install git+https://github.com/KinglittleQ/torch-batch-svd.git
```

# Download pre-processed datasets

To download all our [pre-processed datasets from Google Drive](TODO), run

```bash
tnd-download-data dataset --dataset all
```

# Running the full SfM pipeline (optional, for custom data)

This section walks you through starting from a small collection of images, annotating them, and running our custom SfM to create the initial dataset. This is how we created the pre-processed datasets, available above.

## Download images

To download one of our [image collections from Google Drive](https://drive.google.com/drive/folders/11ogFtOOBB-UIq6seMukYncqqFacxBn5-?usp=drive_link) run

```bash
tnd-download-data images --dataset [dataset]
```

For example,

```bash
tnd-download-data images --dataset bobs-burgers-dining
```

If this fails, that means the `name <=> link` association is not set at the top of the file [toon3d/scripts/download_data.py](toon3d/scripts/download_data.py). Feel free to file and issue or make a PR. Or, make sure a Google Drive folder is set to public and copy it's link.

Then do

```bash
tnd-download-data images --dataset [dataset] --link [link]
```

For example,

```bash
tnd-download-data images --dataset bobs-burgers-dining --link https://drive.google.com/drive/folders/1eicpYlQRUMuCbWfBG5SZev_4Y8FKHMKS?usp=drive_link
```

and the directory will be downloaded to `data/images/[dataset]`

## Process Data

This step runs depth estimation and Segment Anything (SAM).

Download [SAM](https://github.com/facebookresearch/segment-anything) weights with `tnd-download-data sam`.

Now, you can run

```bash
tnd-process-data initialize --dataset [dataset] --input_path [input_path]
```

Where the `input_path` is the source folder of your images while `dataset` is the name of the dataset that will be output to `data/processed/[dataset]`

For example,

```bash
tnd-process-data initialize --dataset bobs-burgers-dining --input_path data/images/bobs-burgers-dining
```

If you want to add more images to your dataset, run this

```bash
tnd-process-data add --dataset bobs-burgers-dining --input_path data/images/more-bobs-burgers-dining-photos
```

## Label images

You can use [labeler.toon3d.studio](https://labeler.toon3d.studio/).

You have two ways of getting your data in the viewer.

(1) **Uploading ZIP folders**

You can either upload a zipped process-data folder or simply a selection of images. If just images, you'll have more limited functionality (no depth images or SAM masks).

(2) **No-upload version for faster development**

Expose your processed data to a public URL. Here is an example with our script with CORS allowed for any origin. You can change the port or the relative directory from which to host the files from.

```bash
tnd-server --path data/processed --port 8000
```

Now, open your processed dataset and annotate.

Navigate to https://labeler.toon3d.studio/?path=http://localhost:8000/bobs-burgers-dining in our case. Or, if you are developing locally then http://localhost:3000/?path=http://localhost:8000/bobs-burgers-dining.

## Run structure from motion!

Now we can run our method to get a dense 3D reconstruction for novel-view synthesis.

```bash
tnd-run --help
```

For example,

```bash
tnd-run --dataset bobs-burgers-dining
```

# Run multi-view stereo!

For example,

```bash
ns-train toon3d --data data/nerfstudio/bobs-burgers-dining
```

To train a depth-nerfacto, run the following:

```bash
ns-train depth-nerfacto --data data/nerfstudio/bobs-burgers-dining \
    --pipeline.use_visibility_loss True \
    --pipeline.visibility_min_views 1 \
    --pipeline.model.is_euclidean_depth True \
    nerfstudio-data \
    --depth_unit_scale_factor 1.0
```

<details>
<summary><strong>(Optional) Regularize with a fine-tuned diffusion model</strong></summary>
<br>

<blockquote style="margin: 0 0 0 20px; border-left: 3px solid #4CAF50; padding: 0 10px;">

We can fine-tune a diffusion model on our data, and then we can apply it while optimizing the 3D model. Check out the wandb logs to see training progress.

```bash
python toon3d/scripts/finetune.py --dataset [dataset]
```


For exmaple,

```bash
python toon3d/scripts/finetune.py --dataset bobs-burgers-dining
```

Now, optimize with the fine-tuned model as a prior.

```bash
TODO!
```
</blockquote>
</details>
<br>

Render a camera path that you created

```bash
tnd-render camera-path --load-config [load-config] --camera-path-filename [camera-path-filename] --output-path [output-path].mp4
```

Render videos between training views

```bash
tnd-render interpolate --load-config [load-config] --output-path [output-path]
``` 

# Test cases

```bash
pytest tests
```

# Project structure

The `outputs` folder is organized according to the types of experiments conducted.

```bash
outputs/[dataset]/run/[timestamp]       # For SfM experiments
outputs/[dataset]/finetune/[timestamp]  # For fine-tuning experiments
outputs/[dataset]/toon3d/[timestamp]    # For MVS experiments
```
