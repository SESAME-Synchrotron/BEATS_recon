import solara
from alrecon import alrecon

@solara.component
def PhaseRetrieval(pippo):
	with solara.Card():
		with solara.Column():

			settings_file1 = 'beats.yml'
			settings_file2 = 'beats2.yml'

			solara.Markdown("pixelsize: {0}".format(pippo.pixelsize.value))
			solara.Button(label="Load settings 1", on_click=lambda: pippo.load_app_settings(settings_file1))
			solara.Button(label="Load settings 2", on_click=lambda: pippo.load_app_settings(settings_file2))
			solara.Switch(label="Hide Message", value=pippo.phase_object)

			solara.InputFloat("Enter pixelsize: ", value=pippo.pixelsize, continuous_update=False)
			solara.Markdown("Phase object: {0}".format(pippo.phase_object.value))


# pippo.load_app_settings('beats.yml')
pippo = alrecon()

@solara.component
def Page():

	with solara.Columns([0.2, 1], gutters_dense=True):
		PhaseRetrieval(pippo)

	@solara.component
	def Layout(children):
		return solara.AppLayout(children=children)

Page()