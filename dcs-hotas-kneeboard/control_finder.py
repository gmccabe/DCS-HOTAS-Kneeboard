#!/usr/bin/python
import re
import os
from pathlib import Path

class control_finder(object):
	
	def __init__(self, dirName):
		#initialize vars
		self.controllers = ['X-55 Rhino Stick', 'X-55 Rhino Throttle']
		self.controllerFiles = []	
		self.dirName = dirName
		self.findControllerFiles()
		
	def findControllerFiles(self):
		#locate unique config files for every aircraft
		#loop through config directories
		print('******************************\tSearchign for config files')
		for root, dirs, files in os.walk(str(Path.home())+'/Saved Games/'+self.dirName+'/Config/Input'):
			for name in files:
				#if in joystick folder
				if os.path.split(root)[1] == 'joystick':
					fullpath = os.path.join(root, name)
					#if has .lua extension
					if os.path.splitext(fullpath)[1] == '.lua':
						for controller in self.controllers:
							print('Searching for '+controller+' Files')
							#find file name match for controller
							if re.match('.*?'+controller+'.*?', name):
								print(fullpath)
								#extract aircraft subfolder
								aircraft = fullpath.split(os.path.sep)[len(fullpath.split(os.path.sep))-3]
								print(aircraft)
								if len(self.controllerFiles) == 0:
									print('First item in list')
									self.controllerFiles.append((controller, aircraft, fullpath))
								else:
									itemFound = False
									for item in self.controllerFiles:
										if (item[0] == controller) and (item[1] == aircraft):
											print('duplicate exists')
											itemFound = True
											#if found is newer than existing
											if os.path.getmtime(fullpath) > os.path.getmtime(item[2]):
												print('replacing with newer file')
												self.controllerFiles[self.controllerFiles.index((item[0], item[1], item[2]))] = (controller, aircraft, fullpath)
												break
											else:
												print('existing is newer')
									#controller and aircraft combo do not exist
									if not itemFound:
										print('None found, adding to list')
										self.controllerFiles.append((controller, aircraft, fullpath))	
		print('******************************\tConfig file search complete')

	def findIndexMatchesByAircraft(self, aircraftToIndex):
		#find indexes where aircraft in self.controllerFiles matches aircraftToIndex
		self.indexMatches = []
		for index in range(len(self.controllerFiles)):
			if self.controllerFiles[index][1] == aircraftToIndex:
				self.indexMatches.append(index)
		return self.indexMatches


	def extractConfig(self, path):
		#extract the button and control names from a config file
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

	def	getConfigToAppend(self, controller, indexMatches):
		for index in indexMatches:
			if self.controllerFiles[index][0] == controller:
				return self.extractConfig(self.controllerFiles[index][2])
		return [[],[]]

	def printControllerFiles():	
		for controller, aircraft, config in self.controllerFiles:
			print(controller+' file for '+aircraft+'\n'+config)
			self.extractConfig(config)
			print('******************************')
			#exit = input("")








	

	

	

