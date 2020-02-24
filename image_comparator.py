#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package Image Comparison Tool
#  Documentation for this module.
#
#  This is a simple GUI tool for visual comparision of two equal-sized images.
#
#Copyright Chamin Morikawa 2019. All rights reserved.
#

# GUI
from PyQt4 import QtGui, QtCore
import os

# cusnot class for graphics view
from image_container import ImageContainerView

# UI layout constants
kMenuBarHeight = 40
kGroupHeight = 80
kGroupBoxHeight = 100
kButtonWidth = 105
kButtonHeight = 70
kDialogMargin = 5
kControlSpacing = 10
kLabelIndent = 40
kLabelHeight = 30
kLayoutGroupWidth = 250

# messages
kFilePathInitial = "No image selected"
kInfoInitial = "Load two images of identical size, to compare them."
kInfoSizeErrorTitle = "Image size mismatch"
kInfoSizeError = "This program is designed to handle images of equal size. Image navigation may behave oddly. Do you want to continue?"
kInfoBothLoaded = "Use mouse wheel to zoom-in/zoom-out either image.Click and drag to move the image around. The other image will mirror the movement so that you can compare fine details between the images."

# handling Unicode characters
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
        
##  Dialog-based user interface
#
class Ui_Dialog(QtGui.QWidget): 
    ## Create the UI contrlols and lay them out
    #  @param self The object pointer.
    #  @param Dialog The dialog pointer.
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Image Comparison Tool"))
        
        # get screen dimensitons for laying out the other controls
        geometry = app.desktop().availableGeometry()
    
        # resize dialog to use all available space
        Dialog.resize(geometry.width(), geometry.height() - kMenuBarHeight)
        
        # calculate container dimensions
        self.containerWidth = (geometry.width() - (2*kDialogMargin + kControlSpacing))/2
        self.containerWidthOverlay = geometry.width() - 2*kDialogMargin
        self.containerHeight = geometry.height() - 2*kGroupHeight - kMenuBarHeight - 2*kControlSpacing
        
        # graphics view for the first image
        self.containerViewFirstImage = ImageContainerView(Dialog)
        self.containerViewFirstImage.setGeometry(QtCore.QRect(kDialogMargin, kGroupHeight + kControlSpacing, self.containerWidth, self.containerHeight))
        self.containerViewFirstImage.setObjectName(_fromUtf8("containerViewFirstImage"))
        self.containerViewFirstImage.setContainingDialog(self)
        self.containerViewFirstImage.tag = 0

        # graphics view for the second image
        self.containerViewSecondImage = ImageContainerView(Dialog)
        self.containerViewSecondImage.setGeometry(QtCore.QRect(self.containerWidth + kDialogMargin + kControlSpacing, kGroupHeight + kControlSpacing, self.containerWidth, self.containerHeight))
        self.containerViewSecondImage.setObjectName(_fromUtf8("containerViewSecondImage"))
        self.containerViewSecondImage.setContainingDialog(self)
        self.containerViewSecondImage.tag = 1
        
        ## group box 1 for control inputs
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, self.containerWidth, kGroupBoxHeight))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        
        # button for loading the first image
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(kDialogMargin, kControlSpacing, kButtonWidth, kButtonHeight))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        
        # file path
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(kButtonWidth + kControlSpacing + kDialogMargin, kControlSpacing, 481, kLabelHeight))
        self.label.setObjectName(_fromUtf8("label"))
        
        # image info
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(kButtonWidth + kControlSpacing + kDialogMargin, kLabelIndent, 481, kLabelHeight))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        
        ## group box 2 for control inputs
        self.groupBox2 = QtGui.QGroupBox(Dialog)
        self.groupBox2.setGeometry(QtCore.QRect(self.containerWidth + kControlSpacing, 0, self.containerWidth, kGroupBoxHeight))
        self.groupBox2.setTitle(_fromUtf8(""))
        self.groupBox2.setObjectName(_fromUtf8("groupBox2"))
        
        # button for loading the second image
        self.pushButton_2 = QtGui.QPushButton(self.groupBox2)
        self.pushButton_2.setGeometry(QtCore.QRect(kDialogMargin, kControlSpacing, kButtonWidth, kButtonHeight))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        
        # file path
        self.label_3 = QtGui.QLabel(self.groupBox2)
        self.label_3.setGeometry(QtCore.QRect(kButtonWidth + kControlSpacing + kDialogMargin, kControlSpacing, 481, kLabelHeight))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        
        # image info
        self.label_4 = QtGui.QLabel(self.groupBox2)
        self.label_4.setGeometry(QtCore.QRect(kButtonWidth + kControlSpacing + kDialogMargin, kLabelIndent, 481, kLabelHeight))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        
        # selection info and hints
        infoLabelTop = geometry.height() - kDialogMargin - kButtonHeight - kMenuBarHeight
        infoLabelWidth = geometry.width() - (kButtonWidth + kControlSpacing + kLayoutGroupWidth + 3*kDialogMargin)
        
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(kDialogMargin, infoLabelTop, infoLabelWidth, kButtonHeight))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_5.setFrameShape(QtGui.QFrame.Panel)
        self.label_5.setLineWidth(1)
        
        # group box for layout
        self.groupBoxLayout = QtGui.QGroupBox(Dialog)
        self.groupBoxLayout.setGeometry(QtCore.QRect(kDialogMargin + infoLabelWidth + kControlSpacing, infoLabelTop, kLayoutGroupWidth, kGroupBoxHeight))
        self.groupBoxLayout.setTitle(_fromUtf8(""))
        self.groupBoxLayout.setObjectName(_fromUtf8("groupBoxLayout"))
        
        # layout label
        self.label_6 = QtGui.QLabel(self.groupBoxLayout)
        self.label_6.setGeometry(QtCore.QRect(0, 0, 200, kLabelHeight))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        
        layoutRB = QtGui.QGridLayout()
        self.groupBoxLayout.setLayout(layoutRB)

        radiobutton = QtGui.QRadioButton("Side-by-side")
        radiobutton.setChecked(True)
        radiobutton.layoutType = "Side-by-side"
        radiobutton.toggled.connect(self.radioButtonClicked)
        layoutRB.addWidget(radiobutton, 0, 0)

        radiobutton = QtGui.QRadioButton("Overlay")
        radiobutton.layoutType = "Overlay"
        radiobutton.toggled.connect(self.radioButtonClicked)
        layoutRB.addWidget(radiobutton, 0, 1)

        
        # clear button: remove images and clean up everything
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(geometry.width() - kDialogMargin - kButtonWidth, infoLabelTop, kButtonWidth, kButtonHeight))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        
        # finish up with the UI
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # image settings
        self.bothLoaded = False
        self.imageSize = None
        self.secondImageSize = None
        
        # information for display
        self.visibleRegion = None
        self.pixelUnderMouse = None
        
        # other UI settings
        self.workingDir = '../samples'
        self.imgLayout = "Side-by-side"
        
        # apply selected layout to images
        self.layoutImages()
        
        # done

    ## Add UI control text and connect event handlers
    #  @param self The object pointer.
    #  @param Dialog The dialog pointer.
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        # image 1
        self.pushButton.setText(_translate("Dialog", "Image 1", None))
        self.label.setText(_translate("Dialog", kFilePathInitial, None))
        self.label_2.setText(_translate("Dialog", "", None))
        
        # image 2
        self.pushButton_2.setText(_translate("Dialog", "Image 2", None))
        self.pushButton_2.setEnabled(False)
        self.label_3.setText(_translate("Dialog", kFilePathInitial, None))

        # info
        self.label_5.setText(_translate("Dialog", kInfoInitial, None))
        
        # layout
        self.label_6.setText(_translate("Dialog", "Layout", None))
        
        # clear
        self.pushButton_3.setText(_translate("Dialog", "Clear", None))
        self.pushButton_3.setEnabled(False)
        
        # events
        self.pushButton.clicked.connect(lambda:self.setImage(Dialog, 0))
        self.pushButton_2.clicked.connect(lambda:self.setImage(Dialog, 1))
        self.pushButton_3.clicked.connect(lambda:self.clearAll(Dialog))
    
        # done
    
    ## adjust the image containers according to the selected layout
    #  @param self The object pointer.
    def layoutImages(self):
        if self.imgLayout == "Overlay":
            # change the indicator label
            self.label_6.setText(_translate("Dialog", "Layout (overlay: image 2)", None))
            self.containerViewFirstImage.setGeometry(QtCore.QRect(kDialogMargin, kGroupHeight + kControlSpacing, self.containerWidthOverlay, self.containerHeight))
            self.containerViewSecondImage.setGeometry(QtCore.QRect(kDialogMargin, kGroupHeight + kControlSpacing, self.containerWidthOverlay, self.containerHeight))
        else:
            # change the indicator label
            self.label_6.setText(_translate("Dialog", "Layout", None))
            self.containerViewFirstImage.setGeometry(QtCore.QRect(kDialogMargin, kGroupHeight + kControlSpacing, self.containerWidth, self.containerHeight))
            self.containerViewSecondImage.setGeometry(QtCore.QRect(self.containerWidth + kDialogMargin + kControlSpacing, kGroupHeight + kControlSpacing, self.containerWidth, self.containerHeight))
        
        # done
        
    ## set an image
    #  @param self The object pointer.
    #  @param Dialog The dialog pointer.
    #  @param imageId An integer tag indicating where the image should go to.
    def setImage(self, Dialog, imageId=0):
        # get foldername from dialog
        imgFilename = QtGui.QFileDialog.getOpenFileName(Dialog, "Select the first image", self.workingDir)
        
        # set the working directory
        self.workingDir = os.path.dirname(os.path.abspath(imgFilename))        
        
        if imageId == 0:
            # load the first image
            self.label.setText(imgFilename)
                
            # set the scene
            self.imageSize = self.containerViewFirstImage.loadSceneForImage(imgFilename)  
            self.label_2.setText(str(self.imageSize.width()) + 'x' + str(self.imageSize.height()) + ' pixels')
                
            # this one can be dragged around
            self.containerViewFirstImage.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
                
            # now we can load the second image
            self.pushButton_2.setEnabled(True)
                
            # or clear everything
            self.pushButton_3.setEnabled(True)
            
        else:
            # we have to load the image first :-\
            self.secondImageSize = self.containerViewSecondImage.loadSceneForImage(imgFilename)
            
            # complain if sizes are not identical
            if self.secondImageSize.width() != self.imageSize.width() or self.secondImageSize.height() != self.imageSize.height():
                # size mismatch
                
                # if the dialog was canceled, size would be [0,0]
                if self.secondImageSize.width() == 0 and self.secondImageSize.height() == 0:
                    # just quit
                    return
                else:
                    # display warning
                    msgBox = QtGui.QMessageBox( self )
                    msgBox.setIcon( QtGui.QMessageBox.Information )
                    msgBox.setText(kInfoSizeErrorTitle)
    
                    msgBox.setInformativeText(kInfoSizeError)
                    msgBox.addButton( QtGui.QMessageBox.Yes )
                    msgBox.addButton( QtGui.QMessageBox.No )
    
                    msgBox.setDefaultButton( QtGui.QMessageBox.No ) 
                    ret = msgBox.exec_()
    
                    if ret == QtGui.QMessageBox.No:
                        # clear the image and abandon
                        self.containerViewSecondImage.clearContainer()
                        self.second_image_size = None
                        self.label_3.setText(_translate("Dialog", kFilePathInitial, None))
                        self.label_4.setText(_translate("Dialog", "", None))
                        self.bothLoaded = False
                        self.secondImageSize = None
                        self.roi = None
            
                        return
            
            # if we are here, we should keep the second image
            self.label_3.setText(imgFilename)
            self.label_4.setText(str(self.secondImageSize.width()) + 'x' + str(self.secondImageSize.height()) + ' pixels')
            
            # this too can be dragged around
            self.containerViewSecondImage.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            
            # there must be two images available now
            self.bothLoaded = True    
            
            # show relevant info
            self.label_5.setText(kInfoBothLoaded)
        
        # done
    
    ## Clear everything so that a new image pair can be loaded
    #  @param self The object pointer.
    #  @param Dialog The dialog pointer.    
    def clearAll(self, Dialog):
        self.bothLoaded = False
        # labels
        self.label.setText(_translate("Dialog", kFilePathInitial, None))
        self.label_2.setText(_translate("Dialog", "", None))
        self.label_3.setText(_translate("Dialog", kFilePathInitial, None))
        self.label_4.setText(_translate("Dialog", "", None))
        
        # buttons
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        
        # graphics views
        self.containerViewFirstImage.clearContainer()
        self.containerViewSecondImage.clearContainer()
        
        # other
        self.bothLoaded = False
        self.imageSize = None
        self.secondImageSize = None
        self.roi = None
        
        # done   

    ## UI update
    #  @param self The object pointer.
    def updateInfo(self):
        # record the visible rectangle
        self.visibleRect = self.containerViewFirstImage.visibleRect()
        
        # update the info
        infoString = "visible rectangle: x=" + str(int(self.visibleRect.x())) + ", y=" + str(int(self.visibleRect.y())) + ", width=" + str(int(self.visibleRect.width())) + ", height=" + str(int(self.visibleRect.height()))
        self.label_5.setText(infoString)
        
        # done
    
    ## Adjust both images according to mouse wheel events
    #  @param self The object pointer.
    #  @param point The image coordinate to center the view on.
    def respondToWheel(self, scale):
        self.containerViewFirstImage.scaleView(scale)
        self.containerViewSecondImage.scaleView(scale)
        
        # also update the UI
        self.updateInfo()
        
        # done
        
        
    ## Adjust both images according to mouse press events
    #  @param self The object pointer.
    #  @param point The image coordinate to center the view on.
    def respondToPress(self, point):
        self.containerViewFirstImage.centerOn(point)
        self.containerViewSecondImage.centerOn(point)
        
        # done
        
    ## Adjust both images when one is being dragged
    #  @param self The object pointer.
    #  @param point The image coordinate to center the view on.
    def respondToDrag(self, point):
        self.containerViewFirstImage.centerOn(point)
        self.containerViewSecondImage.centerOn(point)
        
        # also update the UI
        self.updateInfo()
        
        # done
        
    ## Swap visible image upon right click, in overlay mode
    #  @param self The object pointer.
    def respondToRightClick(self):
        # shrinking the second image container was the easierst way out ;-)
        if self.imgLayout == "Overlay":
            frame = self.containerViewSecondImage.geometry()
            if frame.height() > 0 :
                newFrame = QtCore.QRect(frame.left(), frame.top(), frame.width(), 0)
                self.containerViewSecondImage.setGeometry(newFrame)
                # change the indicator label
                self.label_6.setText(_translate("Dialog", "Layout (overlay, image 1)", None))
                
            else:
                self.containerViewSecondImage.setGeometry(self.containerViewFirstImage.geometry())
                # change the indicator label
                self.label_6.setText(_translate("Dialog", "Layout (overlay, image 2)", None))
        
        # also update the UI
        self.updateInfo()
        
        # done
    
    ## Respond to radio buttons and change layout
    #  @param self The object pointer.
    def radioButtonClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.imgLayout = radioButton.layoutType
            self.layoutImages()
        
        # done

## Main interaction loop
#
#  Typical QtDialog Application; no change      
if __name__ == "__main__":
    import sys
    
    # load GUI
    app = QtGui.QApplication(sys.argv)
    
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    
    sys.exit(app.exec_())

    # done
