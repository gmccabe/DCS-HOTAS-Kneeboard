#!/usr/bin/python
import re
import os
from pathlib import Path

#extract the button and control names from a config file
def extractConfig(path):
	#Open control input lua file
	fo = open(path, "r")
	content = fo.read()
	fo.close()

	content = content.replace('\n',' ')
	content = content.replace('\t',' ')
	#print(content)
	matches = re.findall('\"added\"(.*?),   },',content)
	#print(matches)

	buttonNames = []
	controlNames = []

	for match in matches:
		#print(match)
		buttonName = re.search('\\[\"key\"\\] = \"(.*?)\",', match)
		controlName = re.search('\\[\"name\"\\] = \"(.*?)\"', match)
		buttonNames.append(buttonName.group(1))
		controlNames.append(controlName.group(1))
	#print(buttonNames)
	#print(controlNames)
	return (buttonNames, controlNames)

#locate unique config files for every aircraft
def findControllerFiles(dcsBuild):
	controllers = ['X-55 Rhino Stick', 'X-55 Rhino Throttle']
	controllerFiles = []

	#loop through config directories
	print('******************************\tSearchign for config files')
	for root, dirs, files in os.walk(str(Path.home())+'/Saved Games/'+dcsBuild+'/Config/Input'):
		for name in files:
			#if in joystick folder
			if os.path.split(root)[1] == 'joystick':
				fullpath = os.path.join(root, name)
				#if has .lua extension
				if os.path.splitext(fullpath)[1] == '.lua':
					for controller in controllers:
						print('Searching for '+controller+' Files')
						#find file name match for controller
						if re.match('.*?'+controller+'.*?', name):
							print(fullpath)
							#extract aircraft subfolder
							aircraft = fullpath.split(os.path.sep)[len(fullpath.split(os.path.sep))-3]
							print(aircraft)
							if len(controllerFiles) == 0:
								print('First item in list')
								controllerFiles.append((controller, aircraft, fullpath))
							else:
								itemFound = False
								for item in controllerFiles:
									if (item[0] == controller) and (item[1] == aircraft):
										print('duplicate exists')
										itemFound = True
										#if found is newer than existing
										if os.path.getmtime(fullpath) > os.path.getmtime(item[2]):
											print('replacing with newer file')
											controllerFiles[controllerFiles.index((item[0], item[1], item[2]))] = (controller, aircraft, fullpath)
											break
										else:
											print('existing is newer')
								#controller and aircraft combo do not exist
								if not itemFound:
									print('None found, adding to list')
									controllerFiles.append((controller, aircraft, fullpath))	
	print('******************************\tConfig file search complete')
	return controllerFiles
	
def findIndexMatchesByAircraft(controlFiles, aircraftToIndex):
	indexMatches = []
	for index in range(len(controlFiles)):
		if controlFiles[index][1] == aircraftToIndex:
			indexMatches.append(index)
	return indexMatches
	
def	getConfigToAppend(controlFiles, controller, indexMatches):
	for index in indexMatches:
		if controlFiles[index][0] == controller:
			return extractConfig(controlFiles[index][2])
	return [[],[]]
	
def printControllerFiles():	
	for controller, aircraft, config in findControllerFiles():
		print(controller+' file for '+aircraft+'\n'+config)
		extractConfig(config)
		print('******************************')
		#exit = input("")
