import solara
from pathlib import Path
# from typing import Optional, cast
import numpy as np
import dxchange
import tomopy
import os
import random

# ImageJ executable
Fiij_exe = solara.reactive('/opt/fiji-linux64/Fiji.app/ImageJ-linux64')
ImageJ_exe_stack = Fiij_exe.value + ' -macro FolderOpener_virtual.ijm '

h5file = solara.reactive("")
recon_dir = solara.reactive("/home/gianthk/Data/BEATS/IH/scratch/pippo/recon")
cor_dir = solara.reactive("/home/gianthk/Data/BEATS/IH/scratch/pippo/cor")
ncore = solara.reactive(4)
algorithms = ["gridrec", "fbp_cuda"]
algorithm = solara.reactive("gridrec")
norm_auto = solara.reactive(True)
COR_range = solara.reactive((1260, 1300)) # COR_range_min.value, COR_range_max.value
COR_slice_ind = solara.reactive(1000) # int(projs.shape[0]/2)
COR_steps = [0.5, 1, 2, 5, 10]
COR_step = solara.reactive(1)
COR_auto = solara.reactive(False)
continuous_update = solara.reactive(True)
COR = solara.reactive(1280)
COR_guess = solara.reactive(1280)
COR_algorithms = ["Vo", "TomoPy"]
COR_algorithm = solara.reactive("TomoPy") # "Vo"
h5dir = "~/Data/" # remove??
projs = np.zeros([0,0,0])
recon = np.zeros([0,0,0])
# flats = None
# darks = None
theta = np.zeros(0)
loaded_file = solara.reactive(False)
load_status = solara.reactive(False)
cor_status = solara.reactive(False)
reconstructed = solara.reactive(False)
recon_status = solara.reactive(False)
sino_range = solara.reactive((980, 1020))
averaging = solara.reactive("median")

def generate_title():
    titles = ["Al-Recon. CT reconstruction for dummies",
              "Al-Recon. Have fun reconstructing",
              "Al-Recon. Anyone can reconstruct",
              "Al-Recon. The CT reconstruction GUI",
              "Al-Recon. It has never been so easy",
              "Al-Recon. CT reconstruction made simple",
              ]
    return titles[random.randint(0, len(titles) - 1)]

def view_projs_with_napari():
    # from qtpy.QtWidgets import QApplication
    # app = QApplication([])
    # print(app)
    # app.exec_()

    import napari
    from napari.settings import get_settings

    get_settings().application.ipy_interactive = False
    viewer = napari.Viewer()

    # print(napari._qt.get_app())
    # viewer = napari.view_image(projs)
    # viewer = napari.imshow(projs)
    # napari.run()

def view_cor_with_ImageJ():
    os.system(ImageJ_exe_stack + cor_dir.value + '/{:04.2f}'.format(COR_range.value[0]) + '.tiff &')

def view_recon_with_ImageJ():
    os.system(ImageJ_exe_stack + recon_dir.value + '/slice.tiff &')

def load_and_normalize(filename):
    global projs
    # global flats
    # global darks
    global theta
    # global loaded_file
    load_status.set(True)

    projs, flats, darks, theta = dxchange.read_aps_32id(filename, exchange_rank=0, sino=(sino_range.value[0], sino_range.value[1], 1))
    loaded_file.set(True)

    print("Dataset size: ", projs[:, :, :].shape[:], " - dtype: ", projs.dtype)
    print("Flat fields size: ", flats[:, :, :].shape[:])
    print("Dark fields size: ", darks[:, :, :].shape[:])
    print("Theta array size: ", theta.shape[:])

    if norm_auto.value:
        projs = tomopy.normalize(projs, flats, darks, ncore=ncore.value, averaging=averaging.value)
        print("Sinogram: normalized.")

        projs = tomopy.minus_log(projs, ncore=ncore.value)
        print("Sinogram: - log transformed.")

    load_status.set(False)
    COR_slice_ind.set(int(np.mean(sino_range.value)))

    if COR_auto.value:
        guess_COR()

def guess_COR():
    cor_status.set(True)
    if COR_algorithm.value == "Vo":
        COR_guess.value = tomopy.find_center_vo(projs, ncore=ncore.value)
        print("Automatic detected COR: ", COR_guess.value, " - tomopy.find_center_vo")
    elif COR_algorithm.value == "TomoPy":
        COR_guess.value = tomopy.find_center(projs, theta)[0]
        print("Automatic detected COR: ", COR_guess.value, " - tomopy.find_center")

    COR.set(COR_guess.value)
    COR_range.set((COR_guess.value - 20, COR_guess.value + 20))
    cor_status.set(False)

def write_cor():
    cor_status.set(True)
    tomopy.write_center(projs,
                        theta,
                        cor_dir.value,
                        [COR_range.value[0], COR_range.value[1], COR_step.value],
                        ind=int(COR_slice_ind.value-sino_range.value[0])
                        )
    print("Reconstructed slice with COR range: ", ([COR_range.value[0], COR_range.value[1], COR_step.value]))
    cor_status.set(False)

def reconstruct_dataset():
    global projs
    global theta
    global recon
    recon_status.set(True)
    recon = tomopy.recon(projs,
                         theta,
                         center=COR.value,
                         algorithm=algorithm.value,
                         sinogram_order=False,
                         ncore=ncore.value)
    print("Dataset reconstructed.")
    recon_status.set(False)
    reconstructed.set(True)

def write_recon():
    fileout = recon_dir.value + '/slice.tiff'
    recon_status.set(True)
    dxchange.writer.write_tiff_stack(recon, fname=fileout, axis=0, digit=4, start=0, overwrite=True)
    recon_status.set(False)

@solara.component
def CORdisplay():
    with solara.Card("", style={"max-width": "800px"}, margin=0, classes=["my-2"]):
        with solara.Row(gap="10px", justify="space-around"):
            solara.Button(label="Guess COR", icon_name="mdi-play", on_click=lambda: guess_COR(), disabled=not(loaded_file.value))
            solara.InputFloat("COR guess", value=COR_guess, continuous_update=False)
            # solara.InputText("COR", value=COR, continuous_update=continuous_update.value)
            SetCOR()
        solara.ProgressLinear(cor_status.value)

@solara.component
def CORinspect():
    with solara.Card(subtitle="COR manual inspection", style={"max-width": "800px"}, margin=0, classes=["my-2"]):
        with solara.Column(): # style={"width": "450px"}
            with solara.Row():
                solara.Markdown(f"Min: {COR_range.value[0]}")
                solara.SliderRangeInt("COR range", value=COR_range, step=5, min=0, max=projs.shape[2], thumb_label="always")
                solara.Markdown(f"Max: {COR_range.value[1]}")
            with solara.Row():
                solara.SliderInt("COR slice", value=COR_slice_ind, step=5, min=sino_range.value[0], max=sino_range.value[1], thumb_label="always")
                solara.SliderValue("COR step", value=COR_step, values=COR_steps)

            solara.Button(label="Write images with COR range", icon_name="mdi-play", on_click=lambda: write_cor(),
                          disabled=not (loaded_file.value))
            solara.ProgressLinear(cor_status.value)
            solara.Button(label="inspect COR range images", icon_name="mdi-eye",
                          on_click=lambda: view_cor_with_ImageJ())

@solara.component
def SetCOR():
    solara.InputFloat("Your COR choice", value=COR, continuous_update=True)

@solara.component
def NapariViewer():
    with solara.Card("Napari viewer", style={"max-width": "500px"}, margin=0, classes=["my-2"]):
        with solara.Row(gap="10px", justify="space-around"):
            solara.Button(label="Sinogram", icon_name="mdi-eye", on_click=lambda: view_projs_with_napari(), text=True, outlined=True) # , attributes={"href": github_url, "target": "_blank"}
            solara.Button(label="Reconstruction", icon_name="mdi-eye", on_click=lambda: view_recon_with_napari(), text=True, outlined=True) # , attributes={"href": github_url, "target": "_blank"}

@solara.component
def ImageJViewer():
    with solara.Card("ImageJ viewer", subtitle="Launch ImageJ to inspect:", style={"max-width": "500px"}, margin=0, classes=["my-2"]):
        with solara.Row(gap="10px", justify="space-around"):
            solara.Button(label="COR range", icon_name="mdi-eye", on_click=lambda: view_cor_with_ImageJ(), text=True, outlined=True) # , attributes={"href": github_url, "target": "_blank"}
            solara.Button(label="Reconstruction", icon_name="mdi-eye", on_click=lambda: view_recon_with_ImageJ(), text=True, outlined=True) # , attributes={"href": github_url, "target": "_blank"}

@solara.component
def FileSelect():
    with solara.Card("Select HDF5 dataset file", margin=0, classes=["my-2"], style={"max-height": "500px"}): # style={"max-width": "800px"},
        global h5file
        global h5dir

        # h5file, set_file = solara.use_state_or_update(cast(Optional[Path], None))
        # h5file, set_file = solara.use_state(cast(Optional[Path], None))
        h5dir, set_directory = solara.use_state(Path(h5dir).expanduser())

        solara.FileBrowser(can_select=False, directory=h5dir, on_directory_change=set_directory, on_file_open=h5file.set)

@solara.component
def FileLoad():
    with solara.Card("", margin=0, classes=["my-2"]): # style={"max-width": "800px"},
        global h5file

        with solara.Column():
            solara.SliderRangeInt("Sinogram range", value=sino_range, min=0, max=2160, thumb_label="always")
            with solara.Row(): # gap="10px", justify="space-around"
                # with solara.Column():
                solara.Button(label="Load data", icon_name="mdi-cloud-download", on_click=lambda: load_and_normalize(h5file.value), style={"height": "40px", "width": "400px"}, disabled=not(os.path.splitext(h5file.value)[1]=='.h5'))
                solara.Switch(label="Normalize", value=norm_auto, style={"height": "20px"})
                solara.Switch(label="Guess Center Of Rotation", value=COR_auto, style={"height": "20px"})

            solara.ProgressLinear(load_status.value)

@solara.component
def DispH5FILE():
    # solara.Markdown("## Dataset information")
    # solara.Markdown(f"**File name**: {h5file.value}")
    return solara.Markdown(f'''
            ## Dataset information
            * File name: <mark>`{Path(h5file.value).stem}`</mark>
            * Proj size: {projs[:, :, :].shape[:]}
            * Sinogram range: `{sino_range.value}`
            ''')
    # solara.Markdown(f"* Sinogram range: `{sino_range.value}`")
    # solara.Markdown(f"* Recon dir: {recon_dir.value}")
    # solara.Markdown(f"COR dir: {cor_dir.value}")

@solara.component
def DatasetInfo():
    # global loaded_file
    # if loaded_file.value:
    with solara.VBox():
        solara.Markdown("### Dataset information")
        solara.Info(f"File name: {Path(h5file.value).stem}", dense=True)
        solara.Info(f"Proj size: {projs[:, :, :].shape[:]}", dense=True)

@solara.component
def Recon():
    with solara.Card("CT reconstruction", style={"max-width": "800px"}, margin=0, classes=["my-2"]):
        with solara.Column():
            solara.Select("Algorithm", value=algorithm, values=algorithms)
            solara.Button(label="Reconstruct", icon_name="mdi-car-turbocharger", on_click=lambda: reconstruct_dataset(), disabled=not(loaded_file.value))
            solara.ProgressLinear(recon_status.value)
            solara.Button(label="Inspect with Napari", icon_name="mdi-eye", on_click=lambda: load_and_normalize(h5file), disabled=not(reconstructed.value))
            solara.Button(label="Write to disk", icon_name="mdi-content-save-all-outline", on_click=lambda: write_recon(), disabled=not(reconstructed.value))

@solara.component
def OutputSettings(disabled=False, style=None):
    with solara.Card("Output directories", margin=0, classes=["my-2"]): # style={"max-width": "500px"},
        solara.InputText("Reconstruction directory", value=recon_dir, continuous_update=False, disabled=disabled)
        solara.InputText("COR directory", value=cor_dir, continuous_update=False, disabled=disabled)

@solara.component
def DefaultSettings():
    with solara.Card("Default settings", style={"max-width": "500px"}, margin=0, classes=["my-2"]):
        solara.InputInt("Number of cores", value=ncore, continuous_update=False)
        solara.InputText("Sinogram averaging:", value=averaging, continuous_update=False)
        solara.Select("Auto COR algorithm", value=COR_algorithm, values=COR_algorithms)
        solara.Switch(label="Normalize dataset upon loading", value=norm_auto, style={"height": "20px"})
        solara.Switch(label="Attempt auto COR upon loading", value=COR_auto, style={"height": "40px"})
        solara.InputText("ImageJ launcher", value=Fiij_exe, continuous_update=False)

@solara.component
def ReconSettings():
    with solara.Card("Reconstruction settings", style={"max-width": "500px"}, margin=0, classes=["my-2"]):
        solara.Select("Algorithm", value=algorithm, values=algorithms)

@solara.component
def Page():
    with solara.Sidebar():
        with solara.Card(margin=0, elevation=0):
            DispH5FILE()
            SetCOR()
            OutputSettings(disabled=False)
            NapariViewer()
            ImageJViewer()
            # DatasetInfo()
            # solara.Markdown("This is the sidebar at the home page!")

    with solara.Card("Load dataset"):
        solara.Title(generate_title())
        # solara.Markdown("This is the home page")
        FileSelect()
        FileLoad()
        DatasetInfo()

@solara.component
def Layout(children):
    return solara.AppLayout(children=children)

Page()