import yaml
import solara

class alrecon:
	def __init__(self):
		# pass
		# self.pixelsize = solara.reactive(0.)
		self.init_settings('beats.yml')

	def init_settings(self, filename):
		with open(filename, "r") as file_object:
			alrecon_settings = yaml.load(file_object, Loader=yaml.SafeLoader)

			# some app settings
			# self.pixelsize = solara.reactive(alrecon_settings['phase-retrieval']['pixelsize'])
			for key, val in alrecon_settings['phase-retrieval'].items():
				print('key: {0}; val: {1}'.format(key, val))
				exec('self.'+key + '=solara.reactive(val)')

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