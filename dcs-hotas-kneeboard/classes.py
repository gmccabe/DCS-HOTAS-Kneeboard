#!/usr/bin/python
import re
import os
import logging
import wx
from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

#class used to locate unique config files for every aircraft
class finder(object):
	
	def __init__(self, dirName, debug=False):
		#initialize vars
		self.debug = debug
		logging.getLogger('dcs-hotas-kneeboard')
		self.controllers = ['X-55 Rhino Stick', 'X-55 Rhino Throttle', 'X-56 Rhino Stick', 'X-56 Rhino Throttle']
		self.controllerFiles = []	
		self.dirName = dirName
		self.findControllerFiles()
		
	def debugOutput(self, text):
		if self.debug:
			logging.debug(text)	
		
	def findControllerFiles(self):
		#loop through config directories
		self.debugOutput('******************************\tSearchign for config files')
		for root, dirs, files in os.walk(str(Path.home())+'/Saved Games/'+self.dirName+'/Config/Input'):
			for name in files:
				#if in joystick folder
				if os.path.split(root)[1] == 'joystick':
					fullpath = os.path.join(root, name)
					#if has .lua extension
					if os.path.splitext(fullpath)[1] == '.lua':
						for controller in self.controllers:
							self.debugOutput('Searching for '+controller+' Files')
							#find file name match for controller
							if re.match('.*?'+controller+'.*?', name):
								self.debugOutput(fullpath)
								#extract aircraft subfolder
								aircraft = fullpath.split(os.path.sep)[len(fullpath.split(os.path.sep))-3]
								self.debugOutput(aircraft)
								if len(self.controllerFiles) == 0:
									self.debugOutput('First item in list')
									self.controllerFiles.append((controller, aircraft, fullpath))
								else:
									itemFound = False
									for item in self.controllerFiles:
										if (item[0] == controller) and (item[1] == aircraft):
											self.debugOutput('duplicate exists')
											itemFound = True
											#if found is newer than existing
											if os.path.getmtime(fullpath) > os.path.getmtime(item[2]):
												self.debugOutput('replacing with newer file')
												self.controllerFiles[self.controllerFiles.index((item[0], item[1], item[2]))] = (controller, aircraft, fullpath)
												break
											else:
												self.debugOutput('existing is newer')
									#controller and aircraft combo do not exist
									if not itemFound:
										self.debugOutput('None found, adding to list')
										self.controllerFiles.append((controller, aircraft, fullpath))
		self.debugOutput('******************************\tConfig file search complete')
		
	def findSRSConfig(self):
		#C:\Program Files\DCS-SimpleRadio-Standalone for SRS (add 1 to button assignment)
		self.SRSConfigFile = os.environ["ProgramFiles"]+os.path.sep+'DCS-SimpleRadio-Standalone'+os.path.sep+'client.cfg'
		self.debugOutput(self.SRSConfigFile)
		if os.path.isfile(self.SRSConfigFile):
			self.debugOutput('found!')
			return True
		self.debugOutput('not found!')
		return False
		
	def findUiLayer(self):
		for index in range(len(self.controllerFiles)):
			if self.controllerFiles[index][1] == 'UiLayer':
				return True
		return False

	def findIndexMatchesByAircraft(self, aircraftToIndex):
		#find indexes where aircraft in self.controllerFiles matches aircraftToIndex
		self.indexMatches = []
		for index in range(len(self.controllerFiles)):
			if self.controllerFiles[index][1] == aircraftToIndex:
				self.indexMatches.append(index)
		return self.indexMatches
		
	def listAircraft(self):
		#returns a list of unique aircraft
		self.aircraftList = []
		for index in range(len(self.controllerFiles)):
			aircraft = self.controllerFiles[index][1]
			if not (aircraft in self.aircraftList):
				if aircraft != 'UiLayer' and aircraft != 'Default':
					self.aircraftList.append(aircraft)			
		return self.aircraftList		

	def extractConfig(self, path):
		#extract the button and control names from a config file
		#Open control input lua file
		fo = open(path, "r")
		content = fo.read()
		fo.close()

		content = content.replace('\n',' ')
		content = content.replace('\t',' ')
		matches = re.findall('\"added\"(.*?),   },',content)

		buttonNames = []
		controlNames = []

		for match in matches:
			#self.debugOutput(match)
			buttonName = re.search('\\[\"key\"\\] = \"(.*?)\",', match)
			controlName = re.search('\\[\"name\"\\] = \"(.*?)\"', match)
			buttonNames.append(buttonName.group(1))
			controlNames.append(controlName.group(1))
		#self.debugOutput(buttonNames)
		#self.debugOutput(controlNames)
		return (buttonNames, controlNames)

	def	getConfigToAppend(self, controller, indexMatches):
		for index in indexMatches:
			if self.controllerFiles[index][0] == controller:
				return self.extractConfig(self.controllerFiles[index][2])
		return [[],[]]

	def printControllerFiles():	
		for controller, aircraft, config in self.controllerFiles:
			self.debugOutput(controller+' file for '+aircraft+'\n'+config)
			self.extractConfig(config)
			self.debugOutput('******************************')

#class to create kneeboard images			
class imager(object):

	def __init__(self, debug=False):
		#initialize vars
		self.debug = debug
		logging.getLogger('dcs-hotas-kneeboard')
		self.fnt1 = ImageFont.truetype('arial', 14)
		self.fnt2 = ImageFont.truetype('arial', 18)
		
	def debugOutput(self, text):
		if self.debug:
			logging.debug(text)

	def makeControlImage(self, controller, aircraft, buttonNames, controlNames, dirName):
		self.controller = controller
		self.aircraft = aircraft
		self.buttonNames = buttonNames
		self.controlNames = controlNames
		self.dirName = dirName
		self.debugOutput(self.buttonNames)
		self.debugOutput(self.controlNames)
		self.controller = self.controller.replace(' ', '')
		self.img = Image.open('res'+os.path.sep+self.controller+'.jpg')
		self.draw = ImageDraw.Draw(self.img)

		#X-55
		if self.controller == 'X-55RhinoStick':
			self.drawHat((560,70), [self.printControlName('JOY_BTN7'), self.printControlName('JOY_BTN8', True), self.printControlName('JOY_BTN9'), self.printControlName('JOY_BTN10', True)], 'H1')
			self.drawHat((600,330), [self.printControlName('JOY_BTN11'), self.printControlName('JOY_BTN12', True), self.printControlName('JOY_BTN13'), self.printControlName('JOY_BTN14', True)], 'H2')
			self.drawHat((240, 70), [self.printControlName('JOY_BTN_POV1_U'), self.printControlName('JOY_BTN_POV1_R', True), self.printControlName('JOY_BTN_POV1_D'), self.printControlName('JOY_BTN_POV1_L', True)], 'POV')
			self.buttonWithLabel((20,450), 'Trigger', self.printControlName('JOY_BTN1'))
			self.buttonWithLabel((20,500), 'Paddle', self.printControlName('JOY_BTN6'))
			self.buttonWithLabel((20,550), 'Pinky', self.printControlName('JOY_BTN5'))
			self.drawButtonLine(self.printControlName('JOY_BTN3'), (520, 200), (470, 203))
			self.drawButtonLine(self.printControlName('JOY_BTN2'), (100, 200), (340, 155))
			self.drawButtonLine(self.printControlName('JOY_BTN4'), (100, 300), (297, 329))
		if self.controller == 'X-55RhinoThrottle':
			self.drawHat((550,70), [self.printControlName('JOY_BTN20'), self.printControlName('JOY_BTN21', True), self.printControlName('JOY_BTN22'), self.printControlName('JOY_BTN23', True)], 'H3')
			self.drawHat((620,230), [self.printControlName('JOY_BTN24'), self.printControlName('JOY_BTN25', True), self.printControlName('JOY_BTN26'), self.printControlName('JOY_BTN27', True)], 'H4')
			self.drawSwitch((184,950), [self.printControlName('JOY_BTN6', True), self.printControlName('JOY_BTN7', True)], 'SW 1/2')
			self.drawSwitch((384,950), [self.printControlName('JOY_BTN8', True), self.printControlName('JOY_BTN9', True)], 'SW 3/4')
			self.drawSwitch((584,950), [self.printControlName('JOY_BTN10', True), self.printControlName('JOY_BTN11', True)], 'SW 5/6')
			self.drawSwitch((84,800), [self.printControlName('JOY_BTN12', True), self.printControlName('JOY_BTN13', True)], 'TGL 1')
			self.drawSwitch((284,800), [self.printControlName('JOY_BTN14', True), self.printControlName('JOY_BTN15', True)], 'TGL 2')
			self.drawSwitch((484,800), [self.printControlName('JOY_BTN16', True), self.printControlName('JOY_BTN17', True)], 'TGL 3')
			self.drawSwitch((684,800), [self.printControlName('JOY_BTN18', True), self.printControlName('JOY_BTN19', True)], 'TGL 4')
			self.drawSwitch((184,70), [self.printControlName('JOY_BTN28', True), self.printControlName('JOY_BTN29', True)], 'K1')
			self.drawSwitch((84,200), [self.printControlName('JOY_BTN31', True), self.printControlName('JOY_BTN30', True)], 'Scroll')
			self.buttonWithLabel((20,450), 'Rotary 1', self.printControlName('JOY_Z'))
			self.buttonWithLabel((20,500), 'Rotary 2', self.printControlName('JOY_RX'))
			self.buttonWithLabel((20,550), 'Rotary 3', self.printControlName('JOY_RY'))
			self.buttonWithLabel((20,600), 'Rotary 4', self.printControlName('JOY_RZ'))
			self.drawButtonLine(self.printControlName('JOY_BTN1'), (70, 400), (460, 435))
			self.drawButtonLine(self.printControlName('JOY_BTN2'), (300, 180), (500, 294))
			self.drawButtonLine(self.printControlName('JOY_BTN3'), (570, 450), (523, 430))
			self.drawButtonLine(self.printControlName('JOY_BTN4'), (260, 240), (451, 333))
			self.drawButtonLine(self.printControlName('JOY_BTN5'), (200, 300), (390, 339))
			self.drawButtonLine(self.printControlName('JOY_BTN35'), (580, 410), (515, 377))

		#X-56
		if self.controller == 'X-56Stick':
			self.drawHat((560,70), [self.printControlName('JOY_BTN7'), self.printControlName('JOY_BTN8', True), self.printControlName('JOY_BTN9'), self.printControlName('JOY_BTN10', True)], 'H1')
			self.drawHat((600,330), [self.printControlName('JOY_BTN11'), self.printControlName('JOY_BTN12', True), self.printControlName('JOY_BTN13'), self.printControlName('JOY_BTN14', True)], 'H2')
			self.drawHat((240, 70), [self.printControlName('JOY_BTN_POV1_U'), self.printControlName('JOY_BTN_POV1_R', True), self.printControlName('JOY_BTN_POV1_D'), self.printControlName('JOY_BTN_POV1_L', True)], 'POV')
			self.buttonWithLabel((20,350), 'Mini Stick X', self.printControlName('JOY_RX'))
			self.buttonWithLabel((20,400), 'Mini Stick Y', self.printControlName('JOY_RY'))
			self.buttonWithLabel((20,450), 'Trigger', self.printControlName('JOY_BTN1'))
			self.buttonWithLabel((20,500), 'Paddle', self.printControlName('JOY_BTN6'))
			self.buttonWithLabel((20,550), 'Pinky', self.printControlName('JOY_BTN5'))
			self.drawButtonLine(self.printControlName('JOY_BTN3'), (520, 200), (445, 205))
			self.drawButtonLine(self.printControlName('JOY_BTN2'), (50, 150), (325, 167))
			self.drawButtonLine(self.printControlName('JOY_BTN4'), (50, 250), (274, 341))
		if self.controller == 'X-56Throttle':
			self.drawHat((550,70), [self.printControlName('JOY_BTN20'), self.printControlName('JOY_BTN21', True), self.printControlName('JOY_BTN22'), self.printControlName('JOY_BTN23', True)], 'H3')
			self.drawHat((620,230), [self.printControlName('JOY_BTN24'), self.printControlName('JOY_BTN25', True), self.printControlName('JOY_BTN26'), self.printControlName('JOY_BTN27', True)], 'H4')
			self.drawSwitch((184,950), [self.printControlName('JOY_BTN6', True), self.printControlName('JOY_BTN7', True)], 'SW 1/2')
			self.drawSwitch((384,950), [self.printControlName('JOY_BTN8', True), self.printControlName('JOY_BTN9', True)], 'SW 3/4')
			self.drawSwitch((584,950), [self.printControlName('JOY_BTN10', True), self.printControlName('JOY_BTN11', True)], 'SW 5/6')
			self.drawSwitch((84,800), [self.printControlName('JOY_BTN12', True), self.printControlName('JOY_BTN13', True)], 'TGL 1')
			self.drawSwitch((284,800), [self.printControlName('JOY_BTN14', True), self.printControlName('JOY_BTN15', True)], 'TGL 2')
			self.drawSwitch((484,800), [self.printControlName('JOY_BTN16', True), self.printControlName('JOY_BTN17', True)], 'TGL 3')
			self.drawSwitch((684,800), [self.printControlName('JOY_BTN18', True), self.printControlName('JOY_BTN19', True)], 'TGL 4')
			self.drawSwitch((184,70), [self.printControlName('JOY_BTN28', True), self.printControlName('JOY_BTN29', True)], 'K1')
			self.drawSwitch((84,200), [self.printControlName('JOY_BTN31', True), self.printControlName('JOY_BTN30', True)], 'Scroll')
			self.buttonWithLabel((20,450), 'Rotary 1', self.printControlName('JOY_Z'))
			self.buttonWithLabel((20,500), 'Rotary 2', self.printControlName('JOY_RX'))
			self.buttonWithLabel((20,550), 'Rotary 3', self.printControlName('JOY_RY'))
			self.buttonWithLabel((20,600), 'Rotary 4', self.printControlName('JOY_RZ'))
			self.drawButtonLine(self.printControlName('JOY_BTN1'), (70, 400), (477, 451))
			self.drawButtonLine(self.printControlName('JOY_BTN2'), (300, 200), (500, 294))
			self.drawButtonLine(self.printControlName('JOY_BTN3'), (570, 450), (523, 430))
			self.drawButtonLine(self.printControlName('JOY_BTN4'), (210, 260), (461, 340))
			self.drawButtonLine(self.printControlName('JOY_BTN5'), (150, 320), (415, 344))
			self.drawButtonLine(self.printControlName('JOY_BTN35'), (580, 410), (515, 377))
			
		if self.debug:
			outputPath = os.getcwd()+os.path.sep+'kneeboard-images'
			if not os.path.exists(outputPath):
				os.mkdir(outputPath)			
			self.img.save(outputPath+os.path.sep+self.aircraft+'-'+self.controller+'.jpg', "JPEG")
		else:
			outputPath = str(Path.home())+os.path.sep+'Saved Games'+os.path.sep+self.dirName+os.path.sep+'Kneeboard'+os.path.sep+self.aircraft+os.path.sep
			if not os.path.exists(outputPath):
				os.mkdir(outputPath)
			self.img.save(outputPath+self.aircraft+'-'+self.controller+'.jpg', "JPEG")
	
	def printControlName(self, buttonName, wrap=False):
		try:
			buttonIndex = self.buttonNames.index(buttonName)
			controlName = self.controlNames[buttonIndex]
			if wrap:
				delimiter = ' '
				splitArray = controlName.split(delimiter)
				splitArrayLength = len(splitArray)
				if splitArrayLength > 2:
					splitArray[splitArrayLength//2] = splitArray[splitArrayLength//2]+'\n'
					controlName = delimiter.join(splitArray)
			return controlName
		except ValueError:
			return ''

	def drawButtonLine(self, text, start, end):
		if len(text) > 0:
			textLength = self.draw.textsize(text, font=self.fnt1)
			#split if greater than 100 px
			if textLength[0] > 100:
					delimiter = ' '
					splitArray = text.split(delimiter)
					splitArrayLength = len(splitArray)
					splitArray[splitArrayLength//2] = splitArray[splitArrayLength//2]+'\n'
					text = delimiter.join(splitArray)		
					textLength = self.draw.textsize(text, font=self.fnt1)
			self.drawBackgroundRect(start, text)
			self.draw.text(start, text, font=self.fnt1, fill=(0,0,255))
			direction = [end[0] - start[0], end[1] - start[1]]
			lineStartOffset = [0, 0]
			if abs(direction[0]) > abs(direction[1]):
					if direction[0] > 0:
							#right side
							lineStartOffset[0] = textLength[0]
							lineStartOffset[1] = textLength[1]/2
					else:
							#left side
							lineStartOffset[0] = 0
							lineStartOffset[1] = textLength[1]/2
			else:
					if direction[1] < 0:
							#top side
							lineStartOffset[0] = textLength[0]/2  
							lineStartOffset[1] = 0                      
					else:
							#bottom side
							lineStartOffset[0] = textLength[0]/2  
							lineStartOffset[1] = textLength[1]
			self.draw.line([start[0] + lineStartOffset[0], start[1] + lineStartOffset[1], end[0], end[1]], fill=(255,0,255,120), width=2)
			#self.debugOutput(direction)

	def drawHatLines(self, center, length, hatName):
		textLength = self.draw.textsize(hatName, font=self.fnt2)
		self.draw.line([center[0]-length, center[1], center[0]-textLength[0]/2, center[1]], fill=(255,0,255,255), width=6)
		self.draw.line([center[0]+textLength[0]/2, center[1], center[0]+length, center[1]], fill=(255,0,255,255), width=6)
		self.draw.line([center[0], center[1]-length, center[0], center[1]-textLength[1]/2], fill=(255,0,255,255), width=6)
		self.draw.line([center[0], center[1]+textLength[1]/2, center[0], center[1]+length], fill=(255,0,255,255), width=6)
	
	def drawHat(self, center, hatTextList, hatName):
		if len(hatTextList[0]+hatTextList[1]+hatTextList[2]+hatTextList[3]) > 0:
			lineLength = 30
			self.drawHatLines(center,lineLength, hatName)
			#Draw hat name
			textLength = self.draw.textsize(hatName, font=self.fnt1)
			start = (center[0]-(textLength[0]/2), center[1]-(textLength[1]/2))
			self.draw.text(start, hatName, font=self.fnt1, fill=(255,0,255))
			#U
			textLength = self.draw.textsize(hatTextList[0], font=self.fnt1)
			start = (center[0]-(textLength[0]/2), center[1]-lineLength-(textLength[1]))
			self.drawBackgroundRect(start, hatTextList[0])
			self.draw.text(start, hatTextList[0], font=self.fnt1, fill=(0,0,255))
			#R
			textLength = self.draw.textsize(hatTextList[1], font=self.fnt1)
			start = (center[0]+lineLength, center[1]-(textLength[1]/2))
			self.drawBackgroundRect(start, hatTextList[1])
			self.draw.text(start, hatTextList[1], font=self.fnt1, fill=(0,0,255))
			#D
			textLength = self.draw.textsize(hatTextList[2], font=self.fnt1)
			start = (center[0]-(textLength[0]/2), center[1]+lineLength)
			self.drawBackgroundRect(start, hatTextList[2])
			self.draw.text(start, hatTextList[2], font=self.fnt1, fill=(0,0,255))
			#L
			textLength = self.draw.textsize(hatTextList[3], font=self.fnt1)
			start = (center[0]-lineLength-textLength[0], center[1]-(textLength[1]/2))
			self.drawBackgroundRect(start, hatTextList[3])
			self.draw.text(start, hatTextList[3], font=self.fnt1, fill=(0,0,255))
		
	def drawSwitchLines(self, center, length, switchName):
		textLength = self.draw.textsize(switchName, font=self.fnt2)
		self.draw.line([center[0], center[1]-length, center[0], center[1]-textLength[1]/2], fill=(255,0,255,255), width=6)
		self.draw.line([center[0], center[1]+textLength[1]/2, center[0], center[1]+length], fill=(255,0,255,255), width=6)		
		
	def drawSwitch(self, center, switchTextList, switchName):
		if len(switchTextList[0]+switchTextList[1]) > 0:
			lineLength = 30
			self.drawSwitchLines(center,lineLength, switchName)
			#Draw switch name
			textLength = self.draw.textsize(switchName, font=self.fnt1)
			start = (center[0]-(textLength[0]/2), center[1]-(textLength[1]/2))
			self.draw.text(start, switchName, font=self.fnt1, fill=(255,0,255))
			#
			textLength = self.draw.textsize(switchTextList[0], font=self.fnt1)
			start = (center[0]-(textLength[0]/2), center[1]-lineLength-(textLength[1]))
			self.drawBackgroundRect(start, switchTextList[0])
			self.draw.text(start, switchTextList[0], font=self.fnt1, fill=(0,0,255))
			#
			textLength = self.draw.textsize(switchTextList[1], font=self.fnt1)
			start = (center[0]-(textLength[0]/2), center[1]+lineLength)
			self.drawBackgroundRect(start, switchTextList[1])
			self.draw.text(start, switchTextList[1], font=self.fnt1, fill=(0,0,255))	

	def buttonWithLabel(self, center, buttonName, buttonLabel):
		if len(buttonLabel) > 0:
			text = buttonName+': '+buttonLabel
			self.drawBackgroundRect(center, text)
			self.draw.text(center, text, font=self.fnt1, fill=(0,0,255,255))

	def drawBackgroundRect(self, start, text):
		textLength = self.draw.textsize(text, font=self.fnt1)
		self.draw.rectangle([start[0], start[1], start[0]+textLength[0], start[1]+textLength[1]], fill=(220,220,220,100))

class panel(wx.Panel):

	def __init__(self, parent):
		super(panel, self).__init__(parent)
		
		self.debug = parent.debug
		logging.getLogger('dcs-hotas-kneeboard')
		
		#select DCS folder
		selectDCSText = wx.StaticText(self, -1, label='Select DCS Folder:', style=wx.ALIGN_RIGHT, pos=(0,50), size=(290,50))
		font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) 
		selectDCSText.SetFont(font)
		dcsFolderList = ['DCS', 'DCS.openbeta']
		self.selectDCSComboBox = wx.Choice(self, -1, choices=dcsFolderList, pos=(310,50), size=(100,50))
		self.selectDCSComboBox.SetSelection(1)
		self.selectDCSComboBox.Bind(wx.EVT_CHOICE, self.findConfigsClicked)
		
		#detected aircraft list
		boxPos = (50,100)
		boxSize = (275,250)
		aircraftListBox = wx.StaticBox(self, -1, 'HOTAS Configs Detected', pos=boxPos, size=boxSize)
		self.aircraftList = wx.CheckListBox(self, pos=(boxPos[0]+75+20,boxPos[1]+20), size=(boxSize[0]-75-30,boxSize[1]-30))
		findConfigs = wx.Button(self, label = 'Refresh', pos=(boxPos[0]+10,boxPos[1]+25), size=(75,30))
		findConfigs.Bind(wx.EVT_BUTTON, self.findConfigsClicked)
		selectAllButton = wx.Button(self, label = 'Select All', pos=(boxPos[0]+10,boxPos[1]+25+40), size=(75, 30))
		selectAllButton.Bind(wx.EVT_BUTTON, self.selectAll)
		selectNoneButton = wx.Button(self, label = 'Select None', pos=(boxPos[0]+10,boxPos[1]+25+80), size=(75, 30))
		selectNoneButton.Bind(wx.EVT_BUTTON, self.selectNone)
		
		#options
		boxPos = (350,100)
		boxSize = (200,250)
		optionsBox = wx.StaticBox(self, -1, 'Options', pos=boxPos, size=boxSize)
		self.includeUILayerCheckBox = wx.CheckBox(self, -1, label='Include UiLayer', pos=(boxPos[0]+10,boxPos[1]+25))
		self.includeUILayerCheckBox.SetValue(True)
		self.includeDiscordCheckBox = wx.CheckBox(self, -1, label='Include Discord', pos=(boxPos[0]+10,boxPos[1]+50))
		self.includeDiscordCheckBox.Disable()
		self.includeSRSCheckBox = wx.CheckBox(self, -1, label='Include SRS', pos=(boxPos[0]+10,boxPos[1]+75))
		self.includeSRSCheckBox.SetValue(True)
		
		generateKneeboardImages = wx.Button(self, label = 'GENERATE KNEEBOARD IMAGES', pos=(50,375), size=(500,50))
		generateKneeboardImages.Bind(wx.EVT_BUTTON, self.generateKneeboardImagesClicked)
		
		self.findConfigsClicked(None)
		self.selectAll(None)

	def findConfigsClicked(self, e):
		self.controls = finder(self.selectDCSComboBox.GetString(self.selectDCSComboBox.GetCurrentSelection()), self.debug)
		aircraft = self.controls.listAircraft()
		self.aircraftList.Set(aircraft)
		self.selectAll(None)
		if not self.controls.findSRSConfig():
			self.includeSRSCheckBox.SetValue(False)
			self.includeSRSCheckBox.Disable()
		else:
			self.includeSRSCheckBox.SetValue(True)
			self.includeSRSCheckBox.Enable()			
		if not self.controls.findUiLayer():
			self.includeUILayerCheckBox.SetValue(False)
			self.includeUILayerCheckBox.Disable()			
		else:
			self.includeUILayerCheckBox.SetValue(True)
			self.includeUILayerCheckBox.Enable()			
		
	def generateKneeboardImagesClicked(self, e):
		
		#get selected aircraft
		selectedAircraft = self.aircraftList.GetCheckedStrings()
		print(selectedAircraft)
		
		#get UiLayer controls to add to each aircraft
		if self.includeUILayerCheckBox.IsChecked():
			indexMatches = self.controls.findIndexMatchesByAircraft('UiLayer')
			self.debugOutput(indexMatches)
			
		#loop through files to generate kneeboard images
		kneeboard = imager(self.debug)
		for controller, aircraft, config in self.controls.controllerFiles:
			configLists = self.controls.extractConfig(config)
			if (len(configLists[0]) > 0) and (aircraft != 'UiLayer') and (aircraft in selectedAircraft):
				#add UiLayer configs to appropriate controller configs
				if self.includeUILayerCheckBox.IsChecked():
					configToAppend = self.controls.getConfigToAppend(controller, indexMatches)
					configLists[0].extend(configToAppend[0])
					configLists[1].extend(configToAppend[1])	
				kneeboard.makeControlImage(controller, aircraft, configLists[0], configLists[1], 'DCS.openbeta')
		
	def selectAll(self, e):
		self.aircraftList.SetCheckedItems(range(self.aircraftList.GetCount()))
		
	def selectNone(self, e):
		self.aircraftList.SetCheckedItems([])
		
	def debugOutput(self, text):
		if self.debug:
			logging.debug(text)			

class GUI(wx.Frame):

	def __init__(self, parent, debug=False):
		super(GUI, self).__init__(parent, size=wx.Size(600,500))
		self.debug = debug
		self.buildGUI()
		
	def buildGUI(self):
		pnl = panel(self)
		self.SetTitle('DCS HOTAS Kneeboard Generator')
		self.Centre()
		self.Show(True)	