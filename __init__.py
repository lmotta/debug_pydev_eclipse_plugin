# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DebugPydevEclipse
                                 A QGIS plugin
 Plugin to connect PyDev Eclipse remote debugger
                             -------------------
        begin                : 2017-03-23
        copyright            : (C) 2017 by Luiz Motta
        email                : motta.luiz@gmail.com

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

import os

from PyQt4 import QtGui, QtCore
from debug_pydev import DebugPyDevEclipse

def classFactory(iface):
  return DebugEclipsePlugin( iface )

class DebugEclipsePlugin:
  def __init__(self, iface):
    self.debug = DebugPyDevEclipse()
    self.iface, self.action, self.hasInit = iface, None, False
    self.msgBar = iface.messageBar()
    self.iconStart = QtGui.QIcon( os.path.join( os.path.dirname(__file__), 'start_debug.png' ) )
    self.iconStop = QtGui.QIcon( os.path.join( os.path.dirname(__file__), 'stop_debug.png' ) )
    self.statusAction = { 
      'connect': "Connect to Debug PyDev Eclipse",
      'disconnect': "Disconnect to Debug PyDev Eclipse"
    }

  def initGui(self):
    self.action = QtGui.QAction( self.iconStart, self.statusAction['connect'], self.iface.mainWindow())
    self.action.triggered.connect( self.run )
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu(u"&Remote Debug", self.action)

  def unload(self):
    self.iface.removePluginMenu(u"&Remote Debug", self.action)
    self.iface.removeToolBarIcon( self.action )

  @QtCore.pyqtSlot()
  def run(self):
    self.msgBar.popWidget()
    if not self.hasInit:
      r = self.debug.init()
      if not r['isOk']:
        self.msgBar.pushCritical( "DebugEclipse", r['msg'] )
        return
    self.hasInit = True
    if not self.debug.isRun:
      r = self.debug.start()
      if not r['isOk']:
        self.msgBar.popWidget()
        self.msgBar.pushCritical( "DebugEclipse", r['msg'] )
      else:
        self.action.setIcon( self.iconStop )
        self.action.setText( self.statusAction['disconnect'] )
    else:
      self.debug.stop()
      self.action.setIcon( self.iconStart )
      self.action.setText( self.statusAction['connect'] )
