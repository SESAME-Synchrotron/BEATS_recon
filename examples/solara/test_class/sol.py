import solara
from pathlib import Path
import numpy as np
import os
from time import time
import yaml
from os import getlogin, path

class alrecon:
	def __init__(self):
		pass

		#self.phase_object, self.pixelsize = self.load_app_settings(settings_file)

		#self.phase_object = solara.reactive(phase_object)
		#self.pixelsize = solara.reactive(pixelsize)

	def load_app_settings(self, filename):
		with open(filename, "r") as file_object:
			alrecon_settings = yaml.load(file_object, Loader=yaml.SafeLoader)

			# phase retrieval settings
			self.phase_object = solara.reactive(alrecon_settings['phase-retrieval']['phase_object'])
			self.pixelsize = solara.reactive(alrecon_settings['phase-retrieval']['pixelsize'])
			GLOBAL_NUMBER = self.pixelsize.value


		print('Loaded settings file: {0}'.format(filename))
		print(self.pixelsize)
		# return phase_object, pixelsize

	def myfunc(self):
		print("Hello my name is " + self.name)

	def __str__(self):
		return f"{self.phase_object}({self.pixelsize})"

dict_hallo = {}

"""
dict_hallo[1] = 2
dict_hallo[2] = 232
dict_hallo[3] = 223
dict_hallo[4] = 22342
"""

dict_hallo['hahaha_4'] = 22342
dict_hallo['shahaha_4'] = 22342
dict_hallo['sdfdshahaha_4'] = 22342


dict_2 = {f'key_{i}':i for i in range(4)}
print(dict_2)


for key, value in dict_hallo.items():
	if key.startswith("haha"):
		print(key)
		print(value)


GLOBAL_NUMBER = 0.
from random import randint
def retrieve_phase(pippo, global_list_values):
	print('reload new settings')
	pippo.load_app_settings("beats2.yml")
	for index, float_value in enumerate(global_list_values):
		float_value.set(pippo.pixelsize.value*index)


global_list_values = []

@solara.component
def PhaseRetrieval(pippo):
	GLOBAL_NUMBER = solara.use_reactive(randint(0, 20))
	with solara.Card("", margin=0):  # "Phase retrieval", subtitle="Paganin method",
		with solara.Column():

			float_value = solara.reactive(pippo.pixelsize.value)
			float_value2 = solara.reactive(pippo.pixelsize.value *2)
			global_list_values.append(float_value)
			global_list_values.append(float_value2)
			continuous_update = solara.reactive(True)

			solara.Markdown("pixelsize: {0}".format(pippo.pixelsize.value))

			with solara.Column(style={"margin": "0px"}):
				solara.Switch(label="Phase retrieval", value=pippo.phase_object,
				              style={"height": "20px", "vertical-align": "top"})
				solara.Button(label="Load settings", icon_name="mdi-play", on_click=lambda: retrieve_phase(pippo, global_list_values))





			with solara.Card(subtitle="Phase retrieval parameters", margin=0, classes=["my-2"]):
				with solara.Column():
					solara.InputFloat("Enter a float number", value=float_value,
				                  continuous_update=continuous_update.value)
					solara.InputFloat("Enter a second number", value=float_value2,
				                  continuous_update=continuous_update.value)

					# solara.Button("Clear", on_click=lambda: float_value.set(pippo.pixelsize.value))
					# solara.Markdown(f"**You entered**: {float_value.value}")
				#with solara.Column():
					#solara.InputFloat("Pixel size [\u03BCm]", value=pippo.pixelsize, continuous_update=continuous_update)
					#solara.InputFloat("Pixel size [\u03BCm]", value=continuous_update)

	# solara.Select("I stretch twice the amount", values=["a", "b", "c"], value="a")

import time

@solara.component
def Page():
	pippo = alrecon()
	pippo.load_app_settings("beats.yml")
	with solara.Columns([0.2, 1], gutters_dense=True):
		PhaseRetrieval(pippo)


	@solara.component
	def Layout(children):
		return solara.AppLayout(children=children)

Page()

