# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                                 : debug_pydev
Description                    : Class for DEBUG by Pydev Eclipse

                                             -------------------
Begin                                : 2017-03-22
Copyright                        : (C) 2016 by Luiz Motta
Email                                : motta dot luiz at gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                                                                                                 *
 *     This program is free software; you can redistribute it and/or modify    *
 *     it under the terms of the GNU General Public License as published by    *
 *                                                                                                                                                 *
 ***************************************************************************/
"""

import os, socket, sys

class DebugPyDevEclipse:

    path_eclipse = os.path.join( os.path.expanduser('~'), 'eclipse' )
    pydev_src = 'pysrc'
    pydevd_py = 'pydevd.py'

    def __init__(self):
        self.pydevd = None
        self.isRun = False

    def init(self):
        def getPathPySrc():
            path_pysrc = None
            for dirpath, dirnames, filenames in os.walk( self.path_eclipse ):
                if os.path.split(dirpath)[-1] == self.pydev_src:
                    path_pysrc = dirpath
            if path_pysrc is None:
                msg = u"In Eclipse directory, '{0}', not found in your subdirectories the directory '{1}'".format( self.path_eclipse, self.pydev_src )
                return { 'isOk': False, 'msg': msg }
            return { 'isOk': True, 'path_pysrc': path_pysrc }

        if not os.path.exists( self.path_eclipse ):
            msg = u"Eclipse directory not found '{0}'".format( self.path_eclipse )
            return { 'isOk': False, 'msg': msg }
        r = getPathPySrc()
        if not r['isOk']:
            return r
        path_pysrc = r['path_pysrc']
        if not os.path.exists( os.path.join( path_pysrc, self.pydevd_py ) ):
            msg = u"Not found file '{0}' in directory '{1}'".format( self.pydevd_py, path_pysrc )
            return { 'isOk': False, 'msg': msg }

        sys.path.append( path_pysrc )
        try:
            import pydevd
        except Exception as e:
            msg = u"Error import '{0}' in '{1}'".format( e,    path_pysrc)
            return { 'isOk': False, 'msg': msg }
        self.pydevd = pydevd
 
        return { 'isOk': True }

    def start(self):
        def tryConnect(port=5678):
            isOk, msg = True, None
            s = socket.socket()
            try:
                s.connect( ("localhost", 5678) )
            except Exception as e:
                isOk = False
                strerror = e.strerror.decode('utf-8')
                msg = u"Error connect ({0}) for PyDev Eclipse: {1}. In Eclipse start PyDev server".format( e.errno, strerror )
            if isOk:
                s.close()
            return { 'isOk': isOk, 'msg': msg }

        r = tryConnect()
        if not r['isOk']:
            return r

        try:
            self.pydevd.settrace( port=5678, suspend=False )
        except:
            msg = u"Error attach PyDev Eclipse"
            return { 'isOk': False, 'msg': msg }

        self.isRun = True
        return { 'isOk': True }

    def stop(self):
        self.pydevd.kill_all_pydev_threads()
        self.pydevd.stoptrace()
        self.isRun = False
