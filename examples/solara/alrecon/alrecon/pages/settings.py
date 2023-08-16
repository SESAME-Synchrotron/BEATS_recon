import solara

from . import Settings
@solara.component
def Page():

    solara.Title("Settings")
    with solara.Card("Settings"):
        solara.Markdown("Ask before changing these.")
        Settings()


