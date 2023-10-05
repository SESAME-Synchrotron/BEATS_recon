import solara

from . import ReconSettings, OutputSettings, DefaultSettings
@solara.component
def Page():

    solara.Title("Settings")
    with solara.Card("Settings", subtitle="Ask before making changes"):
        OutputSettings()
        with solara.Row():
            DefaultSettings()
            # with solara.Column(align="stretch"):
            ReconSettings()