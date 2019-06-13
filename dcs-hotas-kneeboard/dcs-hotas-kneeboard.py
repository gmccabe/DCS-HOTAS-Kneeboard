#!/usr/bin/python
import control_finder as controls
import control_image_maker as imager

def main():
	#get array of .lua joystick files
	controlFiles = controls.findControllerFiles('DCS.openbeta')
	#loop through files to generate kneeboard images
	addUiLayer = True
	if addUiLayer:
		indexMatches = controls.findIndexMatchesByAircraft(controlFiles, 'UiLayer')
		print(indexMatches)
	for controller, aircraft, config in controlFiles:
		configLists = controls.extractConfig(config)
		if (len(configLists[0]) > 0) and (aircraft != 'UiLayer'):
			#add UiLayer configs to appropriate controller configs
			if addUiLayer:
				configToAppend = controls.getConfigToAppend(controlFiles, controller, indexMatches)
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