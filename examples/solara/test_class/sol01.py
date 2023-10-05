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


GLOBAL_NUMBER = 0.
from random import randint
def retrieve_phase(pippo):
	print('reload new settings')
	pippo.load_app_settings("beats2.yml")

def gene():
	yield randint(0, 20)

generator = gene

@solara.component
def PhaseRetrieval(pippo):
	GLOBAL_NUMBER = solara.use_reactive(randint(0, 20))
	with solara.Card("", margin=0, classes=["my-2"]):  # "Phase retrieval", subtitle="Paganin method",
		with solara.Column():

			with solara.Column(style={"margin": "0px"}):
				solara.Switch(label="Phase retrieval", value=pippo.phase_object,
				              style={"height": "20px", "vertical-align": "top"})
				solara.Button(label="Retrieve phase", icon_name="mdi-play", on_click=lambda: retrieve_phase(pippo))

			solara.Markdown("pixelsize: {0}".format(pippo.pixelsize.value))
			with solara.Card(subtitle="Phase retrieval parameters", margin=0, classes=["my-2"]):
				with solara.Column():
					solara.InputFloat("Pixel size [\u03BCm]", value=pippo.pixelsize, continuous_update=solara.reactive(True))

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

