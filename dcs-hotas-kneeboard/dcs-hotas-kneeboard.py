#!/usr/bin/python
from classes import finder
from classes import imager
from classes import GUI
import sys
import os
import logging
import wx 
import requests
import json

def main():
	#get array of .lua joystick files
	controls = finder('DCS.openbeta', debug)
	
	#get UiLayer controls to add to each aircraft
	if includeUiLayer:
		indexMatches = controls.findIndexMatchesByAircraft('UiLayer')
		debugOutput(indexMatches)
		
	#loop through files to generate kneeboard images
	kneeboard = imager(debug)
	for controller, aircraft, config in controls.controllerFiles:
		configLists = controls.extractConfig(config)
		if (len(configLists[0]) > 0) and (aircraft != 'UiLayer'):
			#add UiLayer configs to appropriate controller configs
			if includeUiLayer:
				configToAppend = controls.getConfigToAppend(controller, indexMatches)
				configLists[0].extend(configToAppend[0])
				configLists[1].extend(configToAppend[1])
			#add SRS configs if they exist
			if controls.findSRSConfig() and includeSRS:
				configToAppend = controls.getSRSConfigToAppend(controller)
				configLists[0].extend(configToAppend[0])
				configLists[1].extend(configToAppend[1])
			#create kneeboard image
			kneeboard.makeControlImage(controller, aircraft, configLists[0], configLists[1], 'DCS.openbeta')
			print('.', end='', flush=True)
	print('Complete')

def debugOutput(text):
	if debug:
		logging.debug(str(text))
		
def checkForUpdate():
	with open('version.txt', 'r') as versionFile:
		versionString = versionFile.read()
	try:
		r = requests.get('https://api.github.com/repos/gmccabe/DCS-HOTAS-Kneeboard/releases/latest') 
		r.raise_for_status()
	except requests.exceptions.RequestException as e:
		debugOutput(str(e))
		return ''

	data = json.loads(r.content)
	remoteVersionString = data['tag_name']
	remoteVersionString = remoteVersionString.replace('v', '')
	remoteVersionString = remoteVersionString.replace('.', '')
	if int(remoteVersionString) > int(versionString):
		return data['assets'][0]['browser_download_url']
#	
	return ''

if __name__ == '__main__':
	#fix to ensure onefile build path is correct
	path = getattr(sys, '_MEIPASS', os.getcwd())
	os.chdir(path)

	#handle arguments
	debug = False
	noGUI = False
	includeUiLayer = False
	includeSRS = False
	for i in range(len(sys.argv)):
		if sys.argv[i] == '-debug':
			debug = True
			logging.basicConfig(filename=path+os.path.sep+'dcs-hotas-kneeboard.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
			logging.getLogger('dcs-hotas-kneeboard')
			logging.debug('Logger initialized')
		if sys.argv[i] == '-noGUI':
			noGUI = True
		if sys.argv[i] == '-UiLayer':
			includeUiLayer = True
		if sys.argv[i] == '-SRS':
			includeSRS = True

	if noGUI:
		#run main
		main()
	else:
		#run GUI
		app = wx.App()
		GUI(None, debug, checkForUpdate())
		app.MainLoop()