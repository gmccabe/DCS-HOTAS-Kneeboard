#!/usr/bin/python
from classes import finder
from classes import imager
import sys
import os
import logging

def main():
	#get array of .lua joystick files
	controls = finder('DCS.openbeta', debug)
	
	#get UiLayer controls to add to each aircraft
	addUiLayer = True
	if addUiLayer:
		indexMatches = controls.findIndexMatchesByAircraft('UiLayer')
		debugOutput(indexMatches)
		
	#loop through files to generate kneeboard images
	kneeboard = imager(True)
	for controller, aircraft, config in controls.controllerFiles:
		configLists = controls.extractConfig(config)
		if (len(configLists[0]) > 0) and (aircraft != 'UiLayer'):
			#add UiLayer configs to appropriate controller configs
			if addUiLayer:
				configToAppend = controls.getConfigToAppend(controller, indexMatches)
				configLists[0].extend(configToAppend[0])
				configLists[1].extend(configToAppend[1])	
			kneeboard.makeControlImage(controller, aircraft, configLists[0], configLists[1], 'DCS.openbeta')

def debugOutput(text):
	if debug:
		logging.debug(str(text))

if __name__ == '__main__':
	#fix to ensure onefile build path is correct
	path = getattr(sys, '_MEIPASS', os.getcwd())
	os.chdir(path)
	
	#handle arguments
	debug = False
	noGUI = False
	for i in range(len(sys.argv)):
		if sys.argv[i] == '-debug':
			debug = True
			logging.basicConfig(filename=path+os.path.sep+'dcs-hotas-kneeboard.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
			logging.getLogger('dcs-hotas-kneeboard')
			logging.debug('Logger initialized')
		if sys.argv[i] == '-noGUI':
			noGUI = True
			
	#run main
	main()