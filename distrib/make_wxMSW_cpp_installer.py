# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------
# Name:        make_win_cpp_installer.py
# Purpose:     A script to create the wxWidgets C++ windows installer
#
# Author:      Kevin Ollivier
#
# Created:     19-April-2011
# RCS-ID:      $Id$
# Copyright:   (c) 2011 Kevin Ollivier
# Licence:     wxWindows license
#----------------------------------------------------------------------

"""
This script will generate a wxWidgets C++ shared dll release based on the 
binaries built for the wxPython release. 
"""


import sys, os, time, glob

KEEP_TEMPS = False

# default InnoSetup installer location
ISCC = r"%s\InnoSetup5\ISCC.exe %s"

if os.environ.has_key("INNO5"):
    ISCC = os.environ["INNO5"]


#----------------------------------------------------------------------

ISS_Template = r'''

[Setup]
AppName = wxWidgets-msw-%(SHORTVER)s
AppVerName = wxWidgets %(VERSION)s
OutputBaseFilename = wxWidgets%(SHORTVER)s-win%(BITS)s-%(VERSION)s
AppCopyright = Copyright 2010 Total Control Software
DefaultDirName = {code:GetInstallDir|c:\DoNotInstallHere}
DefaultGroupName = wxWidgets %(VERSION)s
PrivilegesRequired = %(PRIV)s
OutputDir = dist
DisableStartupPrompt = true
Compression = bzip
SolidCompression = yes
DirExistsWarning = no
DisableReadyMemo = true
DisableReadyPage = true
;;DisableDirPage = true
DisableProgramGroupPage = true
UsePreviousAppDir = no
UsePreviousGroup = no

%(ARCH)s

AppPublisher = Total Control Software
AppPublisherURL = http://www.wxwidgets.org/
AppSupportURL = http://www.wxwidgets.org/support/
AppUpdatesURL = http://www.wxwidgets.org/downloads/
AppVersion = %(VERSION)s

UninstallFilesDir = {app}\%(PKGDIR)s
LicenseFile = licence\licence.txt


;;------------------------------------------------------------

[Components]
Name: core;     Description: "wxWidgets binaries";              Types: full custom;  Flags: fixed

;;------------------------------------------------------------

[Files]
Source: "%(WXDIR)s\*";  DestDir: "{app}"; Components: core; Flags: replacesameversion, recursesubdirs; Excludes: %(WXDIR)s\wxPython\*;

;;------------------------------------------------------------

[UninstallDelete]
Type: files; Name: "{app}\*."; Flags: recursesubdirs

''' + """
;----------------------------------------------------------------------

"""


#----------------------------------------------------------------------

def main():

    verglob = {}
    execfile("wx/__version__.py", verglob)

    VERSION    = verglob["VERSION_STRING"]
    SHORTVER   = VERSION[:3]

    WXDIR           = os.environ["WXWIN"]
    SYSDIR          = get_system_dir()
    ISSFILE         = "__wxWidgets-win32.iss"

    if os.environ.get('CPU', '') == 'AMD64':
        BITS        = '64'
        VCDLLDIR    = 'vc_amd64_dll'
        GDIPLUS     = ''
        ARCH        = 'ArchitecturesInstallIn64BitMode = x64\nArchitecturesAllowed = x64'
        #ARCH        = ''
        PRIV        = 'admin'

    else:
        BITS        = '32'
        VCDLLDIR    = 'vc_dll'
        GDIPLUS     = 'Source: "distrib\msw\gdiplus.dll"; DestDir: "{app}\lib\%(VCDLLDIR)s"; Components: core; Flags: replacesameversion' % vars()
        ARCH        = ''
        PRIV        = 'none'

        
    print """
Building Win32 installer for wxWidgets:
    VERSION    = %(VERSION)s
    SHORTVER   = %(SHORTVER)s
    WXDIR      = %(WXDIR)s
    SYSDIR     = %(SYSDIR)s
    """ % vars()

    f = open(ISSFILE, "w")
    f.write(ISS_Template % vars())
    f.close()

    TOOLS = os.environ['TOOLS']
    if TOOLS.startswith('/cygdrive'):
        TOOLS = r"c:\TOOLS"  # temporary hack until I convert everything over to bash

    os.system(ISCC % (TOOLS, ISSFILE))

    if not KEEP_TEMPS:
        time.sleep(1)
        os.remove(ISSFILE)
        os.remove(ISSDEMOFILE)


#----------------------------------------------------------------------

if __name__ == "__main__":
    main()



#----------------------------------------------------------------------


