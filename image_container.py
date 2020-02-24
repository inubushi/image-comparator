# -*- coding: utf-8 -*-

## @package Image Comparison Tool
#  
#  image_container.py
#  @author: Chamin Morikawa
#
#  Copyright Chamin Morikawa 2019. All rights reserved.
#

# GUI
from PyQt4 import QtCore, QtGui

# custom class for image
from movable_image import MovableImage

# calculations
import math

# constants
kScaleFactorMin = 0.1
kScaleFactorMax = 150.0

## ImageContainerView
#
#  Contains and manipulates an instance of MovableImage.
#  Also passes events to the main dialog, and gets directions for manipulation.
class ImageContainerView(QtGui.QGraphicsView):
    ## The constructor.
    #  @param self The object pointer.
    #  @param parent The ImageContainer that contains the object.
    def __init__(self, parent=None):
        # essentials
        super(ImageContainerView, self).__init__(parent)
        self.scene = MovableImage(self)  
        self.setScene(self.scene)
        
        # container dialog
        self.containerDialog = None
        
        # absolute image path will be stored here
        self.imagePath = None
        
        # for image dragging
        self.setMouseTracking(True)
        self.currentPos = None
        self.previousPos = None
        
        # display info
        self.sceneCenter = None
        self.width = 0
        self.height = 0
        self.originalScaleFactor = 1.0
        self.isPortrait = True
        self.currenScaleFactor = 1.0
        
        # other: tag for identification
        self.tag = -1
    
    ## Set the container for sending event notifications to
    #  @param self The object pointer.
    def setContainingDialog(self, dialog):
        self.containerDialog = dialog
        
        # done
      
    ## Image rectangle that is visible through this view
    #  @param self The object pointer.
    def visibleRect(self):
        return self.mapToScene(self.viewport().geometry()).boundingRect()
        # done
    
    ## Load an image
    #  @param self The object pointer.
    #  @param filePath The absolute path to the image.    
    def loadSceneForImage(self, filePath):
        # set property for future use
        self.imagePath = filePath
        
        # load as a pixmap
        self.image = QtGui.QPixmap(filePath)
        
        # clear previous items
        itemset = self.scene.items()
        for i in range(len(itemset)):
            self.scene.removeItem(itemset[i])

        self.scene.addPixmap(self.image)   
        self.setScene(self.scene)
        
        # estimate original scale factor, depending on the orientation
        self.width = self.geometry().width()
        self.height = self.geometry().height()
        if self.image.height() > self.image.width():
            # portrait
            self.isPortrait = True
            # scale factor is not greater than 1 at the start
            if self.height < self.image.height():
                self.originalScaleFactor = self.height / self.image.height()
            else:
                self.originalScaleFactor = 1
        else:
            # landscape
            self.isPortrait = False
            if self.width < self.image.width():
                self.originalScaleFactor = self.width / self.image.width()
            else:
                self.originalScaleFactor = 1
         
        # print(self.originalScaleFactor)
        # the current scale factor is the same
        self.currentScaleFactor = self.originalScaleFactor
        
        # image size is passed as return value
        return self.image.size()
        
        # done
    
    ## Remove the loaded image, and clean up
    #  @param self The object pointer.
    def clearContainer(self):
        # remove image from the scene
        self.scene.clear()
        # other settings
        self.sceneCenter = None
        self.width = 0
        self.height = 0
        self.originalScaleFactor = 1.0
        self.isPortrait = True
        self.currenScaleFactor = 1.0
        
        # done
        
 
    ## events
 
    ## Mouse wheel rotated on the container
    #  @param self The object pointer.
    #  @param event The event pointer.
    def wheelEvent(self, event):
        # this is the multiplication factor of scale
        scale = math.pow(2.0, -event.delta() / 240.0)
        # use directly for enlarging and shrinking
        self.containerDialog.respondToWheel(scale)
        # absolute scale for dragging
        self.currentScaleFactor *= scale
        
        # done
        
    
    ## events from the scene
    ## Right mouse button pressed on the image
    #  @param self The object pointer.
    #  @param child The MovableImageObject that is sending the event.
    def passRightClickEvent(self, child):
        # get the parent to do the work: not used in this version
        self.containerDialog.respondToRightClick()
        
        # done
    
    
    ## Mouse button released on the image
    #  @param self The object pointer.
    #  @param child The MovableImageObject that is sending the event.
    def processReleaseEvent(self, child):
        # reset things properly
        self.currentPos = None
        self.previousPos = None
        
        # done
    
    
    ## own events
    
    ## Mouse moved on the container
    #  @param self The object pointer.
    #  @param event The event pointer.
    def mouseMoveEvent(self, event):
        if self.scene.dragStarted:
            if self.currentPos != None:
                self.previousPos = self.currentPos
            else:
                self.previousPos = event.pos()
            self.currentPos = event.pos()
            
            # DEBUG
            #print('previous:', self.previousPos.x(), ',', self.previousPos.y()) 
            #print('current:', self.currentPos.x(), ',', self.currentPos.y())            
            
            # cannot move image using the first point
            if self.previousPos.x() > 0 and self.previousPos.x() > 0:
                translationX = self.currentPos.x() - self.previousPos.x()
                translationY = self.currentPos.y() - self.previousPos.y()
                
                # get the ratio of scale factors
                scaleRatio = self.currentScaleFactor/self.originalScaleFactor
                
                # normalize translation
                translationX /= scaleRatio
                translationY /= scaleRatio
                
                # get the current viewable center
                currentSceneRect = self.visibleRect()
                currentSceneCenter = QtCore.QPointF(currentSceneRect.x() + currentSceneRect.width()/2.0,currentSceneRect.y() + currentSceneRect.height()/2.0)
                        
                # calculate the new center
                newCenter = QtCore.QPointF(currentSceneCenter.x() - translationX, currentSceneCenter.y() - translationY)
                
                # send it upstairs
                self.containerDialog.respondToDrag(newCenter)
                
                # done
    
    ## Scale the image for zooming in/out
    #  @param self The object pointer.
    #  @param scaleFactor The factor of magnification.
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        # don't make the image too small or too large        
        if factor < kScaleFactorMin or factor > kScaleFactorMax:
            return
        # ready
        self.scaleFactor = factor
        self.scale(scaleFactor, scaleFactor)
        
        # done
        
    