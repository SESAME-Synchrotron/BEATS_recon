import solara
import yaml

class alrecon:
	def __init__(self):
		# pass
		# self.pixelsize = solara.reactive(0.)
		self.init_settings('beats.yml')

	def init_settings(self, filename):
		with open(filename, "r") as file_object:
			alrecon_settings = yaml.load(file_object, Loader=yaml.SafeLoader)

			# some app settings
			self.pixelsize = solara.reactive(alrecon_settings['phase-retrieval']['pixelsize'])

		print('Init settings file: {0}'.format(filename))
		print('Init pixelsize: {0}'.format(self.pixelsize))


	def load_app_settings(self, filename):
		with open(filename, "r") as file_object:
			alrecon_settings = yaml.load(file_object, Loader=yaml.SafeLoader)

			# some app settings
			self.pixelsize.set(alrecon_settings['phase-retrieval']['pixelsize'])

		print('Loaded settings file: {0}'.format(filename))
		print('Loaded pixelsize: {0}'.format(self.pixelsize))

	def myfunc(self):
		print("Hello my name is " + self.name)

@solara.component
def PhaseRetrieval(pippo):
	with solara.Card():
		with solara.Column():

			settings_file1 = 'beats.yml'
			settings_file2 = 'beats2.yml'

			solara.Markdown("pixelsize: {0}".format(pippo.pixelsize.value))
			solara.Button(label="Load settings 1", on_click=lambda: pippo.load_app_settings(settings_file1))
			solara.Button(label="Load settings 2", on_click=lambda: pippo.load_app_settings(settings_file2))

			solara.InputFloat("Enter pixelsize: ", value=pippo.pixelsize, continuous_update=False)

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