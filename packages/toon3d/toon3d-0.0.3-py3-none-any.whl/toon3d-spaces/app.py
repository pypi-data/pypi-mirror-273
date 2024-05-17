import spaces
import gradio as gr
import os
import shutil
from pathlib import Path
from toon3d.scripts.viser_vis import main as viser_vis_main
import viser
import time
import threading

viewer_thread_instance = None
stop_event = threading.Event()
shared_url = None

_HEADER_ = '''
<h2>Toon3D: Seeing Cartoons from a New Perspective</h2>
Toon3D lifts cartoons into 3D via aligning and warping backprojected monocular depth predictions. The project page is at <a href='https://toon3d.studio/' target='_blank'>https://toon3d.studio/</a> and the Toon3D Labeler is at <a href='https://labeler.toon3d.studio/' target='_blank'>https://labeler.toon3d.studio/</a>. Follow the steps below to run Toon3D!

<div style="margin-top: 20px; font-size: 16px; line-height: 1.6;">
    <div style="display: flex; justify-content: space-between;">
        <div style="width: 49%;">
            <ol>
                <li><strong>Prepare and Process Data</strong>
                    <ul>
                        <li>Upload images and click on "Process Data" to generate processed data.</li>
                        <li>Download the processed data.</li>
                    </ul>
                </li>
                <li><strong>Label Data</strong>
                    <ul>
                        <li>Upload the processed data and label points using the labeler ("Upload ZIP").</li>
                        <li>Click export and upload the points.json to the "Labeled Points" section.</li>
                    </ul>
                </li>
            </ol>
        </div>
        <div style="width: 49%;">
            <ol start="3">
                <li><strong>Generate 3D Output</strong>
                    <ul>
                        <li>Click on "Run Toon3D" to run the structure from motion pipeline.</li>
                        <li>Download the output and inspect locally (point cloud, mesh, Nerfstudio dataset).</li>
                    </ul>
                </li>
                <li><strong>View in Web!</strong>
                    <ul>
                        <li>Click on "Open Viewer" to view the output in an interactive viewer powered by <a href="https://viser.studio/">Viser</a>.</li>
                    </ul>
                    <ul>
                        <li>Reach out if you have any questions!</li>
                    </ul>
                </li>
            </ol>
        </div>
    </div>
</div>
'''

def check_input_images(input_images):
    if input_images is None:
        raise gr.Error("No images uploaded!")

@spaces.GPU(duration=120)
def process_images(input_images):

    images_path = "/tmp/gradio/images"
    processed_path = "/tmp/gradio/processed"

    # remove the images_path folder
    os.system(f"rm -rf {images_path}")
    os.system(f"rm -rf {processed_path}")

    # copy the uploaded images to the images_path folder
    os.system(f"mkdir -p {images_path}")
    os.system(f"mkdir -p {processed_path}")

    for fileobj in input_images:
        shutil.copyfile(fileobj.name, images_path + "/" + os.path.basename(fileobj.name))

    # download SAM checkpoint
    download_cmd = "tnd-download-data sam --save-dir /tmp/gradio"
    os.system(download_cmd)

    # process the data
    process_data_cmd = f"tnd-process-data initialize --dataset toon3d-dataset --input_path {images_path} --data_prefix {processed_path} --sam_checkpoint_prefix /tmp/gradio/sam-checkpoints"
    os.system(process_data_cmd)

    zip_folder = "/tmp/gradio/processed/toon3d-dataset"
    shutil.make_archive(zip_folder, 'zip', zip_folder)

    return zip_folder + ".zip"

def toggle_labeler_visibility(visible):
    if visible:
        return '<iframe src="https://labeler.toon3d.studio/" style="display: block; margin: auto; width: 100%; height: 100vh;" frameborder="0"></iframe>'
    else:
        return ""

def check_input_toon3d(processed_data_zip, labeled_data):
    if processed_data_zip is None:
        raise gr.Error("No images uploaded!")
    
@spaces.GPU(duration=120)
def run_toon3d(processed_data_zip, labeled_data):

    data_prefix = "/tmp/gradio/inputs"
    processed_path = f"{data_prefix}/toon3d-dataset"
    output_prefix = "/tmp/gradio/outputs"
    nerfstudio_folder = "/tmp/gradio/nerfstudio"

    os.system(f"rm -rf {processed_path}")
    os.system(f"rm -rf {output_prefix}")
    os.system(f"rm -rf {nerfstudio_folder}")

    shutil.unpack_archive(processed_data_zip.name, processed_path)
    shutil.copyfile(labeled_data.name, f"{processed_path}/points.json")
    
    # run toon3d
    toon3d_cmd = f"tnd-run --dataset toon3d-dataset --data_prefix {data_prefix} --output_prefix {output_prefix} --nerfstudio_folder {nerfstudio_folder} --no-view-point-cloud"
    os.system(toon3d_cmd)

    # get the last timestamped folder in output_prefix
    # output_folder = sorted([f.path for f in os.scandir(output_prefix) if f.is_dir()])[-1]
    output_dirs = Path(output_prefix) / "toon3d-dataset" / "run"
    output_dir = Path(output_dirs / sorted(os.listdir(output_dirs))[-1])

    zip_folder = str(output_dir)
    shutil.make_archive(zip_folder, 'zip', zip_folder)

    return zip_folder + ".zip"

# def open_viewer_fn(processed_data_zip, labeled_data, toon3d_output_zip):

#     print(processed_data_zip)
#     print(labeled_data)
#     print(toon3d_output_zip)

#     data_prefix = Path("/tmp/gradio/inputs")
#     processed_path = f"{data_prefix}/toon3d-dataset"

#     # extract the zip file
#     viewer_folder = "/tmp/gradio/viewer/toon3d-dataset/run/temp"
#     os.system(f"rm -rf {viewer_folder}")
#     shutil.unpack_archive(toon3d_output_zip.name, viewer_folder)

#     shutil.unpack_archive(processed_data_zip.name, processed_path)
#     shutil.copyfile(labeled_data.name, f"{processed_path}/points.json")

#     viser_server = viser.ViserServer()
#     url = viser_server.request_share_url()
#     print(url)

#     # this is an infinite while loop so needs to be run in a separate thread
#     # TODO:
#     viser_vis_main(
#         data_prefix=data_prefix,
#         dataset="toon3d-dataset",
#         output_prefix=Path("/tmp/gradio/viewer"),
#         output_method=Path("run"),
#         server=viser_server,
#         visible=True,
#     )

def viewer_thread(processed_data_zip, labeled_data, toon3d_output_zip):
    global shared_url
    data_prefix = Path("/tmp/gradio/inputs")
    processed_path = f"{data_prefix}/toon3d-dataset"

    viewer_folder = "/tmp/gradio/viewer/toon3d-dataset/run/temp"
    os.system(f"rm -rf {viewer_folder}")
    shutil.unpack_archive(toon3d_output_zip.name, viewer_folder)
    shutil.unpack_archive(processed_data_zip.name, processed_path)
    shutil.copyfile(labeled_data.name, f"{processed_path}/points.json")

    viser_server = viser.ViserServer()
    url = viser_server.request_share_url()
    shared_url = url  # Save the URL to the global variable
    print(url)

    viser_vis_main(
        data_prefix=data_prefix,
        dataset="toon3d-dataset",
        output_prefix=Path("/tmp/gradio/viewer"),
        output_method=Path("run"),
        server=viser_server,
        visible=True,
        return_early=True
    )
    while not stop_event.is_set():
        time.sleep(1)

    viser_server.stop()  # Ensure the server is stopped when the loop exits

def kill_viewer():
    global viewer_thread_instance, stop_event
    if viewer_thread_instance and viewer_thread_instance.is_alive():
        stop_event.set()  # Signal the thread to stop
        viewer_thread_instance.join()  # Wait for the thread to actually stop
        viewer_thread_instance = None
        print("Viewer has been stopped.")
    else:
        print("No viewer is running.")

def get_html_for_shared_url(url):
    return f'<h1>Open <a href="{url}" target="_blank">{url}</a>!</h1>'

def check_input_open_viewer(processed_data_zip, labeled_data, toon3d_output_zip):
    if processed_data_zip is None:
        raise gr.Error("No processed data uploaded!")
    if labeled_data is None:
        raise gr.Error("No labeled points uploaded!")
    if toon3d_output_zip is None:
        raise gr.Error("No Toon3D output uploaded!")

def start_viewer(processed_data_zip, labeled_data, toon3d_output_zip):
    kill_viewer()  # Kill the existing viewer if it's running

    global viewer_thread_instance, stop_event, shared_url
    stop_event.clear()  # Reset the stop event
    shared_url = None  # Reset the URL before starting
    if viewer_thread_instance is None or not viewer_thread_instance.is_alive():
        viewer_thread_instance = threading.Thread(target=viewer_thread, args=(processed_data_zip, labeled_data, toon3d_output_zip))
        viewer_thread_instance.start()
        while not shared_url:
            # Wait for the URL to be set by the thread
            time.sleep(0.1)
        return get_html_for_shared_url(shared_url)  # Return the URL after the thread has set it
    else:
        print("Viewer is already running.")
        return get_html_for_shared_url(shared_url)  # Return the current URL if the viewer is already running

with gr.Blocks(title="Toon3D") as demo:
    gr.Markdown(_HEADER_)
    with gr.Row(variant="panel"):
            input_images = gr.File(label="Upload Images", file_count="multiple", file_types=[".jpg", "jpeg", "png"])
            process_data_button = gr.Button("Process Data", elem_id="process_data_button", variant="primary")
            processed_data_zip = gr.File(label="Processed Data", file_count="single", file_types=[".zip"], interactive=True)
    with gr.Row(variant="panel"):
        labeler_visible = gr.Checkbox(label="Show Labeler", value=False)
    with gr.Row(variant="panel"):
        labeler_frame = gr.HTML()
        labeler_visible.change(toggle_labeler_visibility, inputs=[labeler_visible], outputs=[labeler_frame])
    with gr.Row(variant="panel"):
        labeled_data = gr.File(label="Labeled Points", file_count="single", file_types=[".json"])
        run_toon3d_button = gr.Button("Run Toon3D", elem_id="run_toon3d_button", variant="primary")
        toon3d_output_zip = gr.File(label="Toon3D Output", file_count="single", file_types=[".zip"], interactive=True)
    with gr.Row(variant="panel"):
        open_viewer_button = gr.Button("Open Viewer", elem_id="open_viser_button", variant="primary")
    with gr.Row(variant="panel"):
        viser_link = gr.HTML()

    process_data_button.click(fn=check_input_images, inputs=[input_images]).success(
        fn=process_images,
        inputs=[input_images],
        outputs=[processed_data_zip],
    )

    run_toon3d_button.click(fn=check_input_toon3d, inputs=[processed_data_zip, labeled_data]).success(
        fn=run_toon3d,
        inputs=[processed_data_zip, labeled_data],
        outputs=[toon3d_output_zip],
    )

    open_viewer_button.click(fn=check_input_open_viewer, inputs=[processed_data_zip, labeled_data, toon3d_output_zip]).success(
        fn=start_viewer,
        inputs=[processed_data_zip, labeled_data, toon3d_output_zip],
        outputs=[viser_link],
    )

if __name__ == "__main__":
    demo.queue(max_size=10)
    demo.launch()
