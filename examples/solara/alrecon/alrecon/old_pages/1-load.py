import solara

from . import NapariViewer, FijiViewer

from pathlib import Path
from typing import Optional, cast
import dxchange
import tomopy
# import napari

github_url = solara.util.github_url(__file__)
# h5file = solara.reactive("")

h5file = None
h5dir = "~/Data/"
projs = None
# flats = None
# darks = None
# theta = None
loaded_file = solara.reactive(False)
sino_range = solara.reactive((900, 1100))
ncore = solara.reactive(4)
averaging = solara.reactive("median")

@solara.component
def Page_test():
    file, set_file = solara.use_state(cast(Optional[Path], None))
    path, set_path = solara.use_state(cast(Optional[Path], None))
    directory, set_directory = solara.use_state(Path("~").expanduser())

    with solara.VBox() as main:
        can_select = solara.ui_checkbox("Enable select")

        def reset_path():
            set_path(None)
            set_file(None)

        # reset path and file when can_select changes
        solara.use_memo(reset_path, [can_select])
        solara.FileBrowser(directory, on_directory_change=set_directory, on_path_select=set_path, on_file_open=set_file, can_select=can_select)
        solara.Info(f"You are in directory: {directory}")
        solara.Info(f"You selected path: {path}")
        solara.Info(f"You opened file: {file}")
    return main

def view_projs_with_napari():
    global projs
    # viewer = napari.view_image(projs)

def load_and_normalize(filename):
    global projs
    # global flats
    # global darks
    # global theta
    global loaded_file

    projs, flats, darks, theta = dxchange.read_aps_32id(filename, exchange_rank=0, sino=(sino_range.value[0], sino_range.value[1], 1))
    loaded_file.value = True

    print("Dataset size: ", projs[:, :, :].shape[:], " - dtype: ", projs.dtype)
    print("Flat fields size: ", flats[:, :, :].shape[:])
    print("Dark fields size: ", darks[:, :, :].shape[:])
    print("Theta array size: ", theta.shape[:])

    projs = tomopy.normalize(projs, flats, darks, ncore=ncore.value, averaging=averaging.value)
    print("Sinogram normalized.")

@solara.component
def FileSelect():
    with solara.Card("Select HDF5 file", margin=0, classes=["my-2"]):
        global h5file
        global h5dir

        h5file, set_file = solara.use_state(cast(Optional[Path], None))
        h5dir, set_directory = solara.use_state(Path(h5dir).expanduser())

        # solara.FileBrowser(directory="/home/gianthk/Data/", on_directory_change=set_directory, on_file_open=set_file)
        solara.FileBrowser(directory=h5dir, on_directory_change=set_directory, on_file_open=set_file)

        # solara.Button(label="Load file", icon_name="mdi-cloud-download",
        #               on_click=lambda: load_and_normalize(file))

@solara.component
def FileLoad():
    with solara.Card("", style={"max-width": "800px"}, margin=0, classes=["my-2"]):
        global h5file

        solara.Markdown(f"**Sinogram range**: {sino_range.value}")
        # with solara.Row():
        #     solara.Button("Reset", on_click=lambda: sino_range.set((900, 1100)))

        with solara.Row(gap="10px", justify="space-around"):
        # with solara.Column():
            solara.SliderRangeInt("Sinogram range", value=sino_range, min=0, max=2160)
            # with solara.Padding(2):
            solara.Button(label="Load data", icon_name="mdi-cloud-download", on_click=lambda: load_and_normalize(h5file))

        # with solara.Sidebar():
            # with solara.Card("Sidebar of FileLoad", margin=0, elevation=0):
            #     solara.Markdown("*Markdown* **is** 👍")
            # SharedComponent()

@solara.component
def DatasetInfo():
    global h5file
    global projs
    global loaded_file

    if loaded_file.value:
        solara.Markdown("## Dataset information")
        solara.Info(f"File name: {h5file}")
        solara.Info(f"Proj size: {projs[:, :, :].shape[:]}")

@solara.component
def Page():
    with solara.Sidebar():
        with solara.Card(margin=0, elevation=0):
            NapariViewer()
            FijiViewer()

    with solara.Card():
        solara.Title("Load your experiment data")
        FileSelect()
        FileLoad()
        DatasetInfo()
