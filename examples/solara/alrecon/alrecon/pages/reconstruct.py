import solara

from . import NapariViewer, ImageJViewer, SetCOR, DispH5FILE, Recon, CORwrite, CORinspect, CORdisplay, OutputSettings

# from pathlib import Path
# from typing import Optional, cast
# import dxchange
# import tomopy
# import napari

github_url = solara.util.github_url(__file__)

@solara.component
def CORwriteLocal():
    with solara.Card("Center Of Rotation (COR)", style={"max-width": "800px"}, margin=0, classes=["my-2"]):

        with solara.Column():
            CORdisplay()
            CORinspect()
        # with solara.Row(gap="10px", justify="space-around"):
            CORwrite()
            # solara.Button(label="Inspect", icon_name="mdi-eye", on_click=lambda: load_and_normalize(h5file))

@solara.component
def Page():
    with solara.Sidebar():
        with solara.Card(margin=0, elevation=0):
            DispH5FILE()
            SetCOR()
            OutputSettings(disabled=False)
            NapariViewer()
            ImageJViewer()

    with solara.Card():
        solara.Title("CT reconstruction") # "Find the Center Of Rotation (COR)"
        CORwriteLocal()
        Recon()
        # DatasetInfo()
