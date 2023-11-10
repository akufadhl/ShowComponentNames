# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class ComponentNamePlugin(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'ShowComponentName',
			'de': 'Komponentennamen anzeigen',
			'fr': 'Afficher le nom du composant',
			'id': 'Tampilkan Nama Komponen'
			})

	@objc.python_method
	def foreground(self, layer):
		thisLayer = Glyphs.font.selectedLayers[0]
		names = self.originalName(thisLayer.parent.name)
		self.drawNames(names)

	@objc.python_method
	def originalName(self, name):
		splitName = name.split("_")
		splittedNames = []
		
		if "-" in name:
			lang = f"-{name.split('-')[1].split('.')[0]}"

		for n in splitName:

			if "." in n:
				newName = n.split(".")[0].split("-")[0]
				splittedNames.append(newName + lang)
			elif ("-") in name:
				newName = n.split("-")[0]
				splittedNames.append(newName + lang)
			else: 
				splittedNames.append(n)


		return splittedNames

	@objc.python_method
	def drawNames(self, texts):
		# loop through list of texts, draw each one, and move down by line height
		currentZoom = Glyphs.font.currentTab.scale
		fontColor = NSColor.textColor()

		fontAttributes = {NSFontAttributeName: NSFont.labelFontOfSize_(20 / currentZoom),
						NSForegroundColorAttributeName: fontColor}

		thisLayer = Glyphs.font.selectedLayers[0]
		height = thisLayer.master.ascender

		#kerning group
		leftKernGroup = thisLayer.parent.leftKerningGroup
		rightKernGroup = thisLayer.parent.rightKerningGroup

		kerningPos1 = NSPoint(0, 0)
		kerningPos2 = NSPoint(thisLayer.width, 0)

		if leftKernGroup:
			kerningText = NSAttributedString.alloc().initWithString_attributes_(leftKernGroup, fontAttributes)
			kerningText.drawAtPoint_(kerningPos1)
		else:
			kerningText = NSAttributedString.alloc().initWithString_attributes_("None", fontAttributes)
			kerningText.drawAtPoint_(kerningPos1)

		if rightKernGroup != None:
			kerningText = NSAttributedString.alloc().initWithString_attributes_(rightKernGroup, fontAttributes)
			kerningText.drawAtPoint_(kerningPos2)
		else:
			kerningText = NSAttributedString.alloc().initWithString_attributes_("None", fontAttributes)
			kerningText.drawAtPoint_(kerningPos2)

		# Line height
		lineHeight = 30 / currentZoom

		# Starting point
		point = NSPoint(10, height)

		for text in texts:
			displayText = NSAttributedString.alloc().initWithString_attributes_(text, fontAttributes)
			displayText.drawAtPoint_(point)
			point.y -= lineHeight

		
		self.drawOriginalGlyphs(texts)

	@objc.python_method
	def drawOriginalGlyphs(self, names):
		f = Glyphs.font
		thisLayer = Glyphs.font.selectedLayers[0]

		for n in names:
			bezierPath = f.glyphs[n].layers[thisLayer.layerId].completeBezierPath
			print(bezierPath.bounds().size.width)
			width = bezierPath.bounds().size.width
			height = thisLayer.bounds.size.width
			scale = 0.1
			firstTransform = NSAffineTransform.transform()
			firstTransform.translateXBy_yBy_((width)*scale,thisLayer.master.ascender + height/8)
			firstTransform.scaleBy_(scale)
			bezierPath.transformUsingAffineTransform_(firstTransform)
			bezierPath.fill()

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
