# -*- coding: utf-8 -*-

## @package Image Comparison Tool
#  
#  movable_image.py
#  @author: Chamin Morikawa
#
#  Copyright Chamin Morikawa 2019. All rights reserved.
#

# GUI
from PyQt4 import QtCore
from PyQt4.QtGui import QGraphicsScene

## MovableImage
#
#  Stores an image that the user can manipulate for looking at the details
class MovableImage(QGraphicsScene):
    ## The constructor.
    #  @param self The object pointer.
    #  @param parent The ImageContainer that contains the object.
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        # events are passed to the parent for synchronizing an image pair
        self.containingGraphicsView = parent
        # state
        self. currentPressAt = None
        self.dragStarted = False
        self.pressedButton = "None"
        
        # done
        
    ## Mouse button pressed on the image
    #  @param self The object pointer.
    #  @param event The event pointer.
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
                self.pressedButton = "Left"
                self.dragStarted = True
        # in case somebody is still using a three-button mouse...
        if event.button() == QtCore.Qt.RightButton:
                self.pressedButton = "Right"                
        
        # the position is used only for moving the image by clicking
        position = QtCore.QPointF(event.scenePos()) 
        self.currentPressAt = position 
        
        # send the event upstairs: not used in this version
        #self.containingGraphicsView.passPressEvent(self)
        
        self.update()
        
        # done
    
    ## Mouse button released on the image
    #  @param self The object pointer.    
    #  @param event The event pointer.
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragStarted = False
        
            # send a notification upstairs
            self.containingGraphicsView.processReleaseEvent(self)
            
        # in case somebody is still using a three-button mouse...
        if event.button() == QtCore.Qt.RightButton:
            # send a notification upstairs
            self.containingGraphicsView.passRightClickEvent(self)
        self.update()
        
        # done

# end
