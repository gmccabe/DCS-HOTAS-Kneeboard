#!/usr/bin/python
from control_finder import control_finder
import control_image_maker as imager

def main():
	#get array of .lua joystick files
	test = control_finder('DCS.openbeta')
	#loop through files to generate kneeboard images
	addUiLayer = True
	if addUiLayer:
		indexMatches = test.findIndexMatchesByAircraft('UiLayer')
		print(indexMatches)
	for controller, aircraft, config in test.controllerFiles:
		configLists = test.extractConfig(config)
		if (len(configLists[0]) > 0) and (aircraft != 'UiLayer'):
			#add UiLayer configs to appropriate controller configs
			if addUiLayer:
				configToAppend = test.getConfigToAppend(controller, indexMatches)
				print(controller)
				print(aircraft)
				print(configToAppend[0])
				print(configLists[0])
				configLists[0].extend(configToAppend[0])
				configLists[1].extend(configToAppend[1])	
				print(configLists)
			imager.makeControlImage(controller, aircraft, configLists[0], configLists[1], 'DCS.openbeta', debug=False)

if __name__ == '__main__':
	main()
	#exit = input("")