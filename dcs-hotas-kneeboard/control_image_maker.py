#!/usr/bin/python
import os
from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def makeControlImage(controller, aircraft, buttonNames, controlNames, dcsBuild, debug=False):
	print(buttonNames)
	print(controlNames)
	controller = controller.replace(' ', '')
	img = Image.open('res'+os.path.sep+controller+'.jpg')
	draw = ImageDraw.Draw(img)
	fnt = ImageFont.truetype('arial', 14)
	if controller == 'X-55RhinoStick':
		drawHat(draw, fnt, (560,70), [printControlName(controlNames, buttonNames, 'JOY_BTN7'), printControlName(controlNames, buttonNames, 'JOY_BTN8', True), printControlName(controlNames, buttonNames, 'JOY_BTN9'), printControlName(controlNames, buttonNames, 'JOY_BTN10', True)], 'H1')
		drawHat(draw, fnt, (600,330), [printControlName(controlNames, buttonNames, 'JOY_BTN11'), printControlName(controlNames, buttonNames, 'JOY_BTN12', True), printControlName(controlNames, buttonNames, 'JOY_BTN13'), printControlName(controlNames, buttonNames, 'JOY_BTN14', True)], 'H2')
		drawHat(draw, fnt, (240, 70), [printControlName(controlNames, buttonNames, 'JOY_BTN_POV1_U'), printControlName(controlNames, buttonNames, 'JOY_BTN_POV1_R', True), printControlName(controlNames, buttonNames, 'JOY_BTN_POV1_D'), printControlName(controlNames, buttonNames, 'JOY_BTN_POV1_L', True)], 'POV')
		buttonWithLabel(draw, fnt, (20,450), 'Trigger', printControlName(controlNames, buttonNames, 'JOY_BTN1'))
		buttonWithLabel(draw, fnt, (20,500), 'Paddle', printControlName(controlNames, buttonNames, 'JOY_BTN6'))
		buttonWithLabel(draw, fnt, (20,550), 'Pinky', printControlName(controlNames, buttonNames, 'JOY_BTN5'))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN3'), (520, 200), (470, 203))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN2'), (100, 200), (340, 155))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN4'), (100, 300), (297, 329))
	if controller == 'X-55RhinoThrottle':
		drawHat(draw, fnt, (550,70), [printControlName(controlNames, buttonNames, 'JOY_BTN20'), printControlName(controlNames, buttonNames, 'JOY_BTN21', True), printControlName(controlNames, buttonNames, 'JOY_BTN22'), printControlName(controlNames, buttonNames, 'JOY_BTN23', True)], 'H3')
		drawHat(draw, fnt, (620,230), [printControlName(controlNames, buttonNames, 'JOY_BTN24'), printControlName(controlNames, buttonNames, 'JOY_BTN25', True), printControlName(controlNames, buttonNames, 'JOY_BTN26'), printControlName(controlNames, buttonNames, 'JOY_BTN27', True)], 'H4')
		drawSwitch(draw, fnt, (184,950), [printControlName(controlNames, buttonNames, 'JOY_BTN6', True), printControlName(controlNames, buttonNames, 'JOY_BTN7', True)], 'SW 1/2')
		drawSwitch(draw, fnt, (384,950), [printControlName(controlNames, buttonNames, 'JOY_BTN8', True), printControlName(controlNames, buttonNames, 'JOY_BTN9', True)], 'SW 3/4')
		drawSwitch(draw, fnt, (584,950), [printControlName(controlNames, buttonNames, 'JOY_BTN10', True), printControlName(controlNames, buttonNames, 'JOY_BTN11', True)], 'SW 5/6')
		drawSwitch(draw, fnt, (84,800), [printControlName(controlNames, buttonNames, 'JOY_BTN12', True), printControlName(controlNames, buttonNames, 'JOY_BTN13', True)], 'TGL 1')
		drawSwitch(draw, fnt, (284,800), [printControlName(controlNames, buttonNames, 'JOY_BTN14', True), printControlName(controlNames, buttonNames, 'JOY_BTN15', True)], 'TGL 2')
		drawSwitch(draw, fnt, (484,800), [printControlName(controlNames, buttonNames, 'JOY_BTN16', True), printControlName(controlNames, buttonNames, 'JOY_BTN17', True)], 'TGL 3')
		drawSwitch(draw, fnt, (684,800), [printControlName(controlNames, buttonNames, 'JOY_BTN18', True), printControlName(controlNames, buttonNames, 'JOY_BTN19', True)], 'TGL 4')
		drawSwitch(draw, fnt, (184,70), [printControlName(controlNames, buttonNames, 'JOY_BTN28', True), printControlName(controlNames, buttonNames, 'JOY_BTN29', True)], 'K1')
		drawSwitch(draw, fnt, (84,200), [printControlName(controlNames, buttonNames, 'JOY_BTN31', True), printControlName(controlNames, buttonNames, 'JOY_BTN30', True)], 'Scroll')
		buttonWithLabel(draw, fnt, (20,450), 'Rotary 1', printControlName(controlNames, buttonNames, 'JOY_Z'))
		buttonWithLabel(draw, fnt, (20,500), 'Rotary 2', printControlName(controlNames, buttonNames, 'JOY_RX'))
		buttonWithLabel(draw, fnt, (20,550), 'Rotary 3', printControlName(controlNames, buttonNames, 'JOY_RY'))
		buttonWithLabel(draw, fnt, (20,600), 'Rotary 4', printControlName(controlNames, buttonNames, 'JOY_RZ'))
		#buttonWithLabel(draw, fnt, (20,550), 'Pinky', printControlName(controlNames, buttonNames, 'JOY_BTN5'))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN1'), (70, 400), (460, 435))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN2'), (300, 200), (500, 294))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN3'), (570, 450), (523, 430))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN4'), (210, 260), (416, 336))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN5'), (150, 320), (312, 350))
		drawButtonLine(draw, fnt, printControlName(controlNames, buttonNames, 'JOY_BTN35'), (580, 410), (515, 377))
	if debug:
		img.save('output'+os.path.sep+aircraft+'-'+controller+'.jpg', "JPEG")
	else:
		outputPath = str(Path.home())+os.path.sep+'Saved Games'+os.path.sep+dcsBuild+os.path.sep+'Kneeboard'+os.path.sep+aircraft+os.path.sep
		if not os.path.exists(outputPath):
			os.mkdir(outputPath)
		img.save(outputPath+aircraft+'-'+controller+'.jpg', "JPEG")
	
def printControlName(controlNames, buttonNames, buttonName, wrap=False):
	try:
		buttonIndex = buttonNames.index(buttonName)
		controlName = controlNames[buttonIndex]
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

def drawButtonLine(draw, fnt, text, start, end):
	if len(text) > 0:
		textLength = draw.textsize(text, font=fnt)
		#split if greater than 100 px
		if textLength[0] > 100:
				delimiter = ' '
				splitArray = text.split(delimiter)
				splitArrayLength = len(splitArray)
				splitArray[splitArrayLength//2] = splitArray[splitArrayLength//2]+'\n'
				text = delimiter.join(splitArray)		
				textLength = draw.textsize(text, font=fnt)
		drawBackgroundRect(draw, fnt, start, text)
		draw.text(start, text, font=fnt, fill=(0,0,255))
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
		draw.line([start[0] + lineStartOffset[0], start[1] + lineStartOffset[1], end[0], end[1]], fill=(255,0,255,120), width=2)
		#print(direction)

def drawHatLines(draw, fnt, center, length, hatName):
	fnt = ImageFont.truetype('arial', 18)
	textLength = draw.textsize(hatName, font=fnt)
	draw.line([center[0]-length, center[1], center[0]-textLength[0]/2, center[1]], fill=(255,0,255,255), width=6)
	draw.line([center[0]+textLength[0]/2, center[1], center[0]+length, center[1]], fill=(255,0,255,255), width=6)
	draw.line([center[0], center[1]-length, center[0], center[1]-textLength[1]/2], fill=(255,0,255,255), width=6)
	draw.line([center[0], center[1]+textLength[1]/2, center[0], center[1]+length], fill=(255,0,255,255), width=6)
	
def drawHat(draw, fnt, center, hatTextList, hatName):
	if len(hatTextList[0]+hatTextList[1]+hatTextList[2]+hatTextList[3]) > 0:
		lineLength = 30
		drawHatLines(draw, fnt, center,lineLength, hatName)
		#Draw hat name
		textLength = draw.textsize(hatName, font=fnt)
		start = (center[0]-(textLength[0]/2), center[1]-(textLength[1]/2))
		draw.text(start, hatName, font=fnt, fill=(255,0,255))
		#
		textLength = draw.textsize(hatTextList[0], font=fnt)
		start = (center[0]-(textLength[0]/2), center[1]-lineLength-(textLength[1]))
		drawBackgroundRect(draw, fnt, start, hatTextList[0])
		draw.text(start, hatTextList[0], font=fnt, fill=(0,0,255))
		#
		textLength = draw.textsize(hatTextList[1], font=fnt)
		start = (center[0]+lineLength, center[1]-(textLength[1]/2))
		drawBackgroundRect(draw, fnt, start, hatTextList[1])
		draw.text(start, hatTextList[1], font=fnt, fill=(0,0,255))
		#
		textLength = draw.textsize(hatTextList[2], font=fnt)
		start = (center[0]-(textLength[0]/2), center[1]+lineLength)
		drawBackgroundRect(draw, fnt, start, hatTextList[2])
		draw.text(start, hatTextList[2], font=fnt, fill=(0,0,255))
		#
		textLength = draw.textsize(hatTextList[3], font=fnt)
		start = (center[0]-lineLength-textLength[0], center[1]-(textLength[1]/2))
		drawBackgroundRect(draw, fnt, start, hatTextList[3])
		draw.text(start, hatTextList[3], font=fnt, fill=(0,0,255))
		
def drawSwitchLines(draw, fnt, center, length, switchName):
	fnt = ImageFont.truetype('arial', 18)
	textLength = draw.textsize(switchName, font=fnt)
	draw.line([center[0], center[1]-length, center[0], center[1]-textLength[1]/2], fill=(255,0,255,255), width=6)
	draw.line([center[0], center[1]+textLength[1]/2, center[0], center[1]+length], fill=(255,0,255,255), width=6)		
		
def drawSwitch(draw, fnt, center, switchTextList, switchName):
	if len(switchTextList[0]+switchTextList[1]) > 0:
		lineLength = 30
		drawSwitchLines(draw, fnt, center,lineLength, switchName)
		#Draw switch name
		textLength = draw.textsize(switchName, font=fnt)
		start = (center[0]-(textLength[0]/2), center[1]-(textLength[1]/2))
		draw.text(start, switchName, font=fnt, fill=(255,0,255))
		#
		textLength = draw.textsize(switchTextList[0], font=fnt)
		start = (center[0]-(textLength[0]/2), center[1]-lineLength-(textLength[1]))
		drawBackgroundRect(draw, fnt, start, switchTextList[0])
		draw.text(start, switchTextList[0], font=fnt, fill=(0,0,255))
		#
		textLength = draw.textsize(switchTextList[1], font=fnt)
		start = (center[0]-(textLength[0]/2), center[1]+lineLength)
		drawBackgroundRect(draw, fnt, start, switchTextList[1])
		draw.text(start, switchTextList[1], font=fnt, fill=(0,0,255))	

def buttonWithLabel(draw, fnt, center, buttonName, buttonLabel):
	if len(buttonLabel) > 0:
		text = buttonName+': '+buttonLabel
		drawBackgroundRect(draw, fnt, center, text)
		draw.text(center, text, font=fnt, fill=(0,0,255,255))

def drawBackgroundRect(draw, fnt, start, text):
	textLength = draw.textsize(text, font=fnt)
	draw.rectangle([start[0], start[1], start[0]+textLength[0], start[1]+textLength[1]], fill=(220,220,220,100))


