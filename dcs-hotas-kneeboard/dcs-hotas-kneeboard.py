#!/usr/bin/python
from classes import finder
from classes import imager
import sys
import os

def main():
	#get array of .lua joystick files
	controls = finder('DCS.openbeta')
	
	#get UiLayer controls to add to each aircraft
	addUiLayer = True
	if addUiLayer:
		indexMatches = controls.findIndexMatchesByAircraft('UiLayer')
		print(indexMatches)
		
	#loop through files to generate kneeboard images
	kneeboard = imager(debug=False)
	for controller, aircraft, config in controls.controllerFiles:
		configLists = controls.extractConfig(config)
		if (len(configLists[0]) > 0) and (aircraft != 'UiLayer'):
			#add UiLayer configs to appropriate controller configs
			if addUiLayer:
				configToAppend = controls.getConfigToAppend(controller, indexMatches)
				configLists[0].extend(configToAppend[0])
				configLists[1].extend(configToAppend[1])	
			kneeboard.makeControlImage(controller, aircraft, configLists[0], configLists[1], 'DCS.openbeta')

if __name__ == '__main__':
	path = getattr(sys, '_MEIPASS', os.getcwd())
	os.chdir(path)
	main()