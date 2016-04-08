#!/usr/bin/env python
# -*- coding: UTF-8 -*-

###################################################################################
# Macro destinée à l'affichage de textes en couleur et à la segmentation
# de mots en syllabes
#
# voir http://lirecouleur.arkaline.fr
#
# @author Marie-Pierre Brungard
# @version 3.5
# @since 2015
#
# GNU General Public Licence (GPL) version 3
#
# LireCouleur is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
# LireCouleur is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# LireCouleur; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
###################################################################################

import uno
import unohelper
import traceback
import sys
import os
import gettext
from gettext import gettext as _
from com.sun.star.awt import XActionListener
from com.sun.star.task import XJobExecutor
from com.sun.star.task import XJob

from com.sun.star.awt import XKeyHandler
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK
from com.sun.star.awt import Rectangle
from com.sun.star.awt.KeyModifier import MOD2
from com.sun.star.awt.Key import LEFT as keyLeft
from com.sun.star.awt.Key import RIGHT as keyRight

try:
    # nécessaire pour Python 3
    from functools import reduce
except:
    pass
import string
import re
from lirecouleur import *

__version__ = "3.5.0"

# create LANG environment variable
import locale
if os.getenv('LANG') is None:
    lang, enc = locale.getdefaultlocale()
    os.environ['LANG'] = lang
#os.environ['LANGUAGE'] = os.environ['LANG']

__memoKeys__ = {}

#########################################################################################################
#########################################################################################################
#
#    Fonctions préliminaires utilitaires
#
#                                    @@@@@@@@@@@@@@@@@@@@@@
#
#########################################################################################################
#########################################################################################################
def getLirecouleurTemplateURL():
    url = handleMaskTemplate()
    if len(url) > 0:
        return url

    localdir = os.sep.join([getLirecouleurDirectory(), 'locale'])
    loclang = os.environ['LANG']
    tempname = os.sep.join([localdir, loclang, "lirecouleur.ott"])
    if os.path.isfile(tempname):
        return uno.systemPathToFileUrl(tempname)
    loclang = loclang.split('.')[0]
    tempname = os.sep.join([localdir, loclang, "lirecouleur.ott"])
    if os.path.isfile(tempname):
        return uno.systemPathToFileUrl(tempname)
    loclang = loclang.split('_')[0]
    tempname = os.sep.join([localdir, loclang, "lirecouleur.ott"])
    if os.path.isfile(tempname):
        return uno.systemPathToFileUrl(tempname)
    
    url = os.sep.join([getLirecouleurURL(), "template", "lirecouleur.ott"])
    if os.path.isfile(uno.fileUrlToSystemPath(url)):
        return url
    return ""

def getLirecouleurDictionary():
    localdir = os.sep.join([getLirecouleurDirectory(), 'locale'])
    loclang = os.environ['LANG']
    tempname = os.sep.join([localdir, loclang, "lirecouleur.dic"])
    if os.path.isfile(tempname):
        return tempname
    loclang = loclang.split('.')[0]
    tempname = os.sep.join([localdir, loclang, "lirecouleur.dic"])
    if os.path.isfile(tempname):
        return tempname
    loclang = loclang.split('_')[0]
    tempname = os.sep.join([localdir, loclang, "lirecouleur.dic"])
    if os.path.isfile(tempname):
        return tempname
    return os.sep.join([getLirecouleurDirectory(), "lirecouleur.dic"])

def createUnoStruct(cTypeName):
    """Create a UNO struct and return it.
    Similar to the function of the same name in OOo Basic. -- Copied from Danny Brewer library
    """
    sm = uno.getComponentContext().ServiceManager
    oCoreReflection = sm.createInstance( "com.sun.star.reflection.CoreReflection" )
    # Get the IDL class for the type name
    oXIdlClass = oCoreReflection.forName( cTypeName )
    # Create the struct.
    oReturnValue, oStruct = oXIdlClass.createObject( None )
    return oStruct

def createUnoService(serviceName, ctx=None):
    if ctx is None:
        ctx = uno.getComponentContext()

    sm = ctx.ServiceManager
    try:
        serv = sm.createInstanceWithContext(serviceName, ctx)
    except:
        serv = sm.createInstance(serviceName)

    return serv

"""
    morceau de code très sale pour identifier si on utilise OpenOffice ou LibreOffice : les 2 n'ont pas
    la même façon de noter le style par défaut.
"""
def getOOoSetupNode(sNodePath):
    oConfigProvider = createUnoService('com.sun.star.configuration.ConfigurationProvider')
    ppp = createUnoStruct("com.sun.star.beans.PropertyValue")
    ppp.Name = "nodepath"
    ppp.Value = sNodePath
    return oConfigProvider.createInstanceWithArguments("com.sun.star.configuration.ConfigurationAccess", (ppp,))

def getOOoSetupValue(sNodePath, sProperty):
    xConfig = getOOoSetupNode(sNodePath)
    return xConfig.getByName(sProperty)

__style_par_defaut__ = ""
#applic = getOOoSetupValue("/org.openoffice.Setup/Product", "ooName").lower()
#if applic.startswith("libreoffice"):
    #__style_par_defaut__ = "Style par défaut"

"""
    Get the URL of LireCouleur
"""
def getLirecouleurURL():
    """Get the URL of LireCouleur"""
    try:
        pip = uno.getComponentContext().getValueByName("/singletons/com.sun.star.deployment.PackageInformationProvider")
        url = pip.getPackageLocation("LireCouleur")
        if len(url) > 0:
            return url
    except:
        pass

    try:
        # just for debugging outside the extension scope
        filename = uno.fileUrlToSystemPath(__file__)
        return uno.sytemPathToFileUrl(os.path.dirname(os.path.abspath(filename)))
    except:
        pass

    xPathSettingsService = createUnoService('com.sun.star.util.PathSettings')
    xUserPath = xPathSettingsService.getPropertyValue('UserConfig').split(os.sep)[:-1]
    xUserPath.extend(['Scripts', 'python'])
    return os.sep.join(xUserPath)

"""
    Get the name of the directory of LireCouleur
"""
def getLirecouleurDirectory():
    """Get the name of the directory of LireCouleur"""
    return uno.fileUrlToSystemPath(getLirecouleurURL())

"""

"""
def i18n():
    localdir = os.sep.join([getLirecouleurDirectory(), 'locale'])
    gettext.bindtextdomain('lirecouleur', localdir)
    gettext.textdomain('lirecouleur')

#########################################################################################################
#########################################################################################################
#
#    Cette partie du code est destinée à la présentation dans OOo des phonèmes
#    et des syllabes de différentes manières.
#
#                                    @@@@@@@@@@@@@@@@@@@@@@
#
#########################################################################################################
#########################################################################################################

###################################################################################
# Ensemble des styles d'affichage des phonèmes selon différents codages
# voir http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/Text/Formatting
###################################################################################
style_phon_perso = {
        'verb_3p':{'CharStyleName':'conjug_3p'},
        '#':{'CharStyleName':'phon_muet'},
        'q_caduc':{'CharStyleName':'phon_e_caduc'},
        'a':{'CharStyleName':'phon_a'},
        'q':{'CharStyleName':'phon_e'},
        'i':{'CharStyleName':'phon_i'},
        'o':{'CharStyleName':'phon_o'},
        'o_comp':{'CharStyleName':'phon_o_comp'},
        'o_ouvert':{'CharStyleName':'phon_o_ouvert'},
        'u':{'CharStyleName':'phon_ou'},
        'y':{'CharStyleName':'phon_u'},
        'e':{'CharStyleName':'phon_ez'},
        'e_comp':{'CharStyleName':'phon_ez_comp'},
        'w':{'CharStyleName':'phon_w'},
        'wa':{'CharStyleName':'phon_wa'},
        'w5':{'CharStyleName':'phon_w5'},
        'e^':{'CharStyleName':'phon_et'},
        'e^_comp':{'CharStyleName':'phon_et_comp'},
        'a~':{'CharStyleName':'phon_an'},
        'e~':{'CharStyleName':'phon_in'},
        'x~':{'CharStyleName':'phon_un'},
        'o~':{'CharStyleName':'phon_on'},
        'x':{'CharStyleName':'phon_oe'},
        'x^':{'CharStyleName':'phon_eu'},
        'j':{'CharStyleName':'phon_y'},
        'z_s':{'CharStyleName':'phon_z'},
        'g_u':{'CharStyleName':'phon_g'},
        'z^_g':{'CharStyleName':'phon_ge'},
        's_x':{'CharStyleName':'phon_s'},
        'n~':{'CharStyleName':'phon_gn'},
        'p':{'CharStyleName':'phon_p'},
        't':{'CharStyleName':'phon_t'},
        'k':{'CharStyleName':'phon_k'},
        'k_qu':{'CharStyleName':'phon_k'},
        'b':{'CharStyleName':'phon_b'},
        'd':{'CharStyleName':'phon_d'},
        'g':{'CharStyleName':'phon_g'},
        'f':{'CharStyleName':'phon_f'},
        'f_ph':{'CharStyleName':'phon_f'},
        's':{'CharStyleName':'phon_s'},
        's_c':{'CharStyleName':'phon_s'},
        's_t':{'CharStyleName':'phon_s'},
        's^':{'CharStyleName':'phon_ch'},
        'v':{'CharStyleName':'phon_v'},
        'z':{'CharStyleName':'phon_z'},
        'z^':{'CharStyleName':'phon_ge'},
        'm':{'CharStyleName':'phon_m'},
        'n':{'CharStyleName':'phon_n'},
        'l':{'CharStyleName':'phon_l'},
        'r':{'CharStyleName':'phon_r'},
        'ks':{'CharStyleName':'phon_ks'},
        'gz':{'CharStyleName':'phon_gz'},
        '#_amb':{'CharStyleName':__style_par_defaut__},
        'espace':{'CharStyleName':'espace'},
        'liaison':{'CharStyleName':'liaison'},
        'lettre_b':{'CharStyleName':'lettre_b'},
        'lettre_d':{'CharStyleName':'lettre_d'},
        'lettre_p':{'CharStyleName':'lettre_p'},
        'lettre_q':{'CharStyleName':'lettre_q'},
        'consonne':{'CharStyleName':'phon_consonne'},
        'voyelle':{'CharStyleName':'phon_voyelle'},
        'Majuscule':{'CharStyleName':'Majuscule'},
        'Ponctuation':{'CharStyleName':'Ponctuation'},
        'defaut':{'CharStyleName':__style_par_defaut__}
        }

style_phon_complexes = {
        'verb_3p':{'CharStyleName':'conjug_3p'},
        '#':{'CharStyleName':'phon_muet'},
        'q_caduc':{'CharStyleName':__style_par_defaut__},
        'a':{'CharStyleName':__style_par_defaut__},
        'q':{'CharStyleName':__style_par_defaut__},
        'i':{'CharStyleName':__style_par_defaut__},
        'o':{'CharStyleName':__style_par_defaut__},
        'o_comp':{'CharStyleName':'phon_voyelle_comp'},
        'o_ouvert':{'CharStyleName':__style_par_defaut__},
        'u':{'CharStyleName':'phon_voyelle_comp'},
        'y':{'CharStyleName':__style_par_defaut__},
        'e':{'CharStyleName':__style_par_defaut__},
        'e_comp':{'CharStyleName':'phon_voyelle_comp'},
        'w':{'CharStyleName':'phon_voyelle_comp'},
        'wa':{'CharStyleName':'phon_voyelle_comp'},
        'w5':{'CharStyleName':'phon_voyelle_comp'},
        'e^':{'CharStyleName':__style_par_defaut__},
        'e^_comp':{'CharStyleName':'phon_voyelle_comp'},
        'a~':{'CharStyleName':'phon_voyelle_comp'},
        'e~':{'CharStyleName':'phon_voyelle_comp'},
        'x~':{'CharStyleName':'phon_voyelle_comp'},
        'o~':{'CharStyleName':'phon_voyelle_comp'},
        'x':{'CharStyleName':'phon_voyelle_comp'},
        'x^':{'CharStyleName':'phon_voyelle_comp'},
        'j':{'CharStyleName':'phon_consonne_comp'},
        'z_s':{'CharStyleName':'phon_consonne_comp'},
        'g_u':{'CharStyleName':'phon_consonne_comp'},
        'z^_g':{'CharStyleName':'phon_consonne_comp'},
        's_x':{'CharStyleName':'phon_consonne_comp'},
        'n~':{'CharStyleName':'phon_consonne_comp'},
        'p':{'CharStyleName':__style_par_defaut__},
        't':{'CharStyleName':__style_par_defaut__},
        'k':{'CharStyleName':__style_par_defaut__},
        'k_qu':{'CharStyleName':'phon_consonne_comp'},
        'b':{'CharStyleName':__style_par_defaut__},
        'd':{'CharStyleName':__style_par_defaut__},
        'g':{'CharStyleName':__style_par_defaut__},
        'f':{'CharStyleName':__style_par_defaut__},
        'f_ph':{'CharStyleName':'phon_consonne_comp'},
        's':{'CharStyleName':__style_par_defaut__},
        's_c':{'CharStyleName':'phon_consonne_comp'},
        's_t':{'CharStyleName':'phon_consonne_comp'},
        's^':{'CharStyleName':'phon_consonne_comp'},
        'v':{'CharStyleName':__style_par_defaut__},
        'z':{'CharStyleName':__style_par_defaut__},
        'z^':{'CharStyleName':__style_par_defaut__},
        'm':{'CharStyleName':__style_par_defaut__},
        'n':{'CharStyleName':__style_par_defaut__},
        'l':{'CharStyleName':__style_par_defaut__},
        'r':{'CharStyleName':__style_par_defaut__},
        'ks':{'CharStyleName':'phon_consonne_comp'},
        'gz':{'CharStyleName':'phon_consonne_comp'},
        '#_amb':{'CharStyleName':__style_par_defaut__},
        'espace':{'CharStyleName':'espace'},
        'liaison':{'CharStyleName':'liaison'},
        'lettre_b':{'CharStyleName':'lettre_b'},
        'lettre_d':{'CharStyleName':'lettre_d'},
        'lettre_p':{'CharStyleName':'lettre_p'},
        'lettre_q':{'CharStyleName':'lettre_q'},
        'consonne':{'CharStyleName':'phon_consonne'},
        'voyelle':{'CharStyleName':'phon_voyelle'},
        'Majuscule':{'CharStyleName':'Majuscule'},
        'Ponctuation':{'CharStyleName':'Ponctuation'},
        'defaut':{'CharStyleName':__style_par_defaut__}
        }

style_syll_souligne = {
        '1': {'CharUnderline':3,'CharUnderlineHasColor':True,'CharUnderlineColor':0X0000000},
        '2': {'CharUnderline':1,'CharUnderlineHasColor':True,'CharUnderlineColor':0X0000000}
        }

__style_syll_souligne__ = {
        '1': {'CharUnderline':3,'CharUnderlineHasColor':True,'CharUnderlineColor':0X0000000},
        '2': {'CharUnderline':1,'CharUnderlineHasColor':True,'CharUnderlineColor':0X0000000}
        }

__style_phon_perso__ = {
        'verb_3p':{'CharColor':0x00aaaaaa, 'CharContoured':False},
        '#':{'CharColor':0x00aaaaaa, 'CharContoured':False},
        '#_amb':{'CharColor':0x0000000, 'CharContoured':True},
        'q_caduc':{'CharColor':0X00aaaaaa},
        'a':{'CharColor':0x000068de},
        'a~':{'CharColor':0x000068de, 'CharShadowed':True},
        'q':{'CharColor':0X00ef001e},
        'i':{'CharColor':0X003deb3d},
        'e~':{'CharColor':0X003deb3d, 'CharShadowed':True},
        'o':{'CharColor':0X00de7004},
        'o_comp':{'CharColor':0X00de7004},
        'o_ouvert':{'CharColor':0X00de7004},
        'o~':{'CharColor':0X00de7004, 'CharShadowed':True},
        'u':{'CharColor':0X00ffc305},
        'y':{'CharColor':0X005c8526},
        'x~':{'CharColor':0X005c8526, 'CharShadowed':True},
        'e':{'CharColor':0X00008080},
        'e_comp':{'CharColor':0X00008080},
        'e^':{'CharColor':0X000ecd5, 'CharShadowed':True},
        'e^_comp':{'CharColor':0X000ecd5, 'CharShadowed':True},
        'x':{'CharColor':0X00dc2300},
        'x^':{'CharColor':0X00800000},
        'w':{'CharColor':0X00892ca0},
        'wa':{'CharColor':0X00892ca0},
        'w5':{'CharColor':0X003deb3d, 'CharShadowed':True, 'CharUnderline':6},
        'j':{'CharColor':0X00892ca0, 'CharShadowed':True},
        'z_s':{'CharColor':0x0000000, 'CharWeight':150.0},
        'g_u':{'CharColor':0x0000000, 'CharWeight':150.0},
        'z^_g':{'CharColor':0x0000000, 'CharWeight':150.0},
        's_x':{'CharColor':0x0000000, 'CharWeight':150.0},
        'n~':{'CharColor':0x0000000, 'CharWeight':150.0},
        'p':{'CharColor':0x0000000, 'CharWeight':150.0},
        't':{'CharColor':0x0000000, 'CharWeight':150.0},
        'k':{'CharColor':0x0000000, 'CharWeight':150.0},
        'k_qu':{'CharColor':0x0000000, 'CharWeight':150.0},
        'b':{'CharColor':0x0000000, 'CharWeight':150.0},
        'd':{'CharColor':0x0000000, 'CharWeight':150.0},
        'g':{'CharColor':0x0000000, 'CharWeight':150.0},
        'f':{'CharColor':0x0000000, 'CharWeight':150.0},
        'f_ph':{'CharColor':0x0000000, 'CharWeight':150.0},
        's':{'CharColor':0x0000000, 'CharWeight':150.0},
        's_c':{'CharColor':0x0000000, 'CharWeight':150.0},
        's_t':{'CharColor':0x0000000, 'CharWeight':150.0},
        's^':{'CharColor':0x0000000, 'CharWeight':150.0},
        'v':{'CharColor':0x0000000, 'CharWeight':150.0},
        'z':{'CharColor':0x0000000, 'CharWeight':150.0},
        'z^':{'CharColor':0x0000000, 'CharWeight':150.0},
        'm':{'CharColor':0x0000000, 'CharWeight':150.0},
        'n':{'CharColor':0x0000000, 'CharWeight':150.0},
        'l':{'CharColor':0x0000000, 'CharWeight':150.0},
        'r':{'CharColor':0x0000000, 'CharWeight':150.0},
        'ks':{'CharColor':0x0000000, 'CharWeight':150.0},
        'gz':{'CharColor':0x0000000, 'CharWeight':150.0},
        'espace':{'CharBackColor':0x00ff00ff},
        'liaison':{'CharScaleWidth':200, 'CharUnderline':10},
        'lettre_b':{'CharColor':0x0000ff00, 'CharWeight':150.0},
        'lettre_d':{'CharColor':0x00ff0000, 'CharWeight':150.0},
        'lettre_p':{'CharColor':0x000000ff, 'CharWeight':150.0},
        'lettre_q':{'CharColor':0x00555555, 'CharWeight':150.0},
        'consonne':{'CharColor':0x000000ff},
        'voyelle':{'CharColor':0x00ff0000},
        'Majuscule':{'CharBackColor':0x00ffff00},
        'Ponctuation':{'CharBackColor':0x00ff0000},
        'defaut':{'CharUnderline':0, 'CharPosture':0, 'CharColor':0X00000000, 'CharWeight':100.0, 'CharShadowed':False, 'CharBackColor':0x00ffffff}
        }

__style_phon_complexes__ = {
        'verb_3p':{'CharColor':0x0000000, 'CharContoured':True},
        '#':{'CharColor':0x0000000, 'CharContoured':True},
        'q_caduc':{'CharColor':0x00000000},
        'a':{'CharColor':0x0000000},
        'q':{'CharColor':0x0000000},
        'i':{'CharColor':0x0000000},
        'o':{'CharColor':0x0000000},
        'o_comp':{'CharColor':0x00ff950e},
        'o_ouvert':{'CharColor':0x0000000},
        'u':{'CharColor':0x00ff950e},
        'y':{'CharColor':0x0000000},
        'e':{'CharColor':0x0000000},
        'e_comp':{'CharColor':0x00ff950e},
        'w':{'CharColor':0x00ff950e},
        'wa':{'CharColor':0x00ff950e},
        'w5':{'CharColor':0x00ff950e},
        'e^':{'CharColor':0x0000000},
        'e^_comp':{'CharColor':0x00ff950e},
        'a~':{'CharColor':0x00ff950e},
        'e~':{'CharColor':0x00ff950e},
        'x~':{'CharColor':0x00ff950e},
        'o~':{'CharColor':0x00ff950e},
        'x':{'CharColor':0x00ff950e},
        'x^':{'CharColor':0x00ff950e},
        'j':{'CharColor':0x00aecf00},
        'z_s':{'CharColor':0x00aecf00},
        'g_u':{'CharColor':0x00aecf00},
        'z^_g':{'CharColor':0x00aecf00},
        's_x':{'CharColor':0x00aecf00},
        'n~':{'CharColor':0x00aecf00},
        'p':{'CharColor':0x0000000},
        't':{'CharColor':0x0000000},
        'k':{'CharColor':0x0000000},
        'k_qu':{'CharColor':0x00aecf00},
        'b':{'CharColor':0x0000000},
        'd':{'CharColor':0x0000000},
        'g':{'CharColor':0x0000000},
        'f':{'CharColor':0x0000000},
        'f_ph':{'CharColor':0x00aecf00},
        's':{'CharColor':0x0000000},
        's_c':{'CharColor':0x00aecf00},
        's_t':{'CharColor':0x00aecf00},
        's^':{'CharColor':0x00aecf00},
        'v':{'CharColor':0x0000000},
        'z':{'CharColor':0x0000000},
        'z^':{'CharColor':0x0000000},
        'm':{'CharColor':0x0000000},
        'n':{'CharColor':0x0000000},
        'l':{'CharColor':0x0000000},
        'r':{'CharColor':0x0000000},
        'ks':{'CharColor':0x00aecf00},
        'gz':{'CharColor':0x00aecf00},
        '#_amb':{'CharColor':0x0000000},
        'espace':{'CharBackColor':0x00ff00ff},
        'liaison':{'CharScaleWidth':200, 'CharUnderline':10},
        'lettre_b':{'CharColor':0x0000ff00, 'CharWeight':150.0},
        'lettre_d':{'CharColor':0x00ff0000, 'CharWeight':150.0},
        'lettre_p':{'CharColor':0x000000ff, 'CharWeight':150.0},
        'lettre_q':{'CharColor':0x00555555, 'CharWeight':150.0},
        'consonne':{'CharColor':0x000000ff},
        'voyelle':{'CharColor':0x00ff0000},
        'Majuscule':{'CharBackColor':0x00ffff00},
        'Ponctuation':{'CharBackColor':0x00ff0000},
        'defaut':{'CharUnderline':0, 'CharPosture':0, 'CharColor':0X00000000, 'CharWeight':100.0, 'CharShadowed':False, 'CharBackColor':0x00ffffff}
        }

style_syll_dys = {
        '1': {'CharStyleName':'syll_dys_1'},
        '2': {'CharStyleName':'syll_dys_2'},
        '3': {'CharStyleName':'syll_dys_3'}
        }

__style_syll_dys__ = {
        '1': {'CharColor':0x000000ff},
        '2': {'CharColor':0x00ff0000},
        '3': {'CharColor':0x0000ff00}
        }

######################################################################################
#
######################################################################################
styles_phonemes = {
        'perso' : style_phon_perso,
        'complexes' : style_phon_complexes
        }

styles_syllabes = {
        'souligne' : style_syll_souligne,
        'dys' : style_syll_dys
        }

######################################################################################
#
######################################################################################
__styles_lignes_altern__ = {
        '1':{'CharBackColor':0x00ffff66},
        '2':{'CharBackColor':0x0023ff23},
        '3':{'CharBackColor':0x00ff9966},
        '4':{'CharBackColor':0x0000ffdc}
        }

styles_lignes_altern = {
        '1':{'CharStyleName':'altern_ligne_1'},
        '2':{'CharStyleName':'altern_ligne_2'},
        '3':{'CharStyleName':'altern_ligne_3'},
        '4':{'CharStyleName':'altern_ligne_4'}
        }

styles_lignes = 'altern_ligne_'

######################################################################################
# Création des styles de caractères nécessaires à l'application
######################################################################################
def createCharacterStyles(xModel, style_nom, style_forme):
    """ Création des styles de caractères nécessaires à l'application """
    charStyles = xModel.getStyleFamilies().getByName('CharacterStyles')

    try:
        #first create the default character style
        defaultcharstylename = style_nom['defaut']['CharStyleName']
        if len(defaultcharstylename) > 0 and not charStyles.hasByName(defaultcharstylename):
            tmp_style = xModel.createInstance('com.sun.star.style.CharacterStyle')    # create a char style
            tmp_style.setPropertiesToDefault( ('CharCaseMap','CharEscapement','CharEscapementHeight','CharPosture','CharUnderline','CharWeight') )
            charStyles.insertByName(defaultcharstylename, tmp_style)    # insert the style in the document
    except:
        pass

    # then create the other character styles
    for phon in style_nom.keys():
        charstylename = style_nom[phon]['CharStyleName']
        if len(charstylename) > 0 and not charStyles.hasByName(charstylename):
            charstylestruct = style_forme[phon]
            tmp_style = xModel.createInstance('com.sun.star.style.CharacterStyle')    # create a char style
            for kpv in charstylestruct.keys():
                tmp_style.setPropertyValue(kpv, charstylestruct[kpv])
            try:
                tmp_style.setParentStyle(defaultcharstylename)    # set parent charstyle
            except:
                pass
            charStyles.insertByName(charstylename, tmp_style)

def makeShape(oDrawDoc, cShapeClassName, oPosition=None, oSize=None):
    """Create a new shape of the specified class.
    Position and size arguments are optional.
    """
    oShape = oDrawDoc.createInstance(cShapeClassName)

    if oPosition != None:
        oShape.Position = oPosition
    if oSize != None:
        oShape.Size = oSize

    return oShape

def makeTextShape(oDrawDoc, oPosition=None, oSize=None):
    """Create a new TextShape with an optional position and size."""
    oShape = makeShape(oDrawDoc, "com.sun.star.drawing.TextShape", oPosition, oSize)
    oShape.TextHorizontalAdjust = 0
    oShape.TextVerticalAdjust = 0
    oShape.TextAutoGrowWidth = True
    oShape.TextAutoGrowHeight = True
    oShape.TextLeftDistance = 0
    oShape.TextRightDistance = 0
    oShape.TextUpperDistance = 0
    oShape.TextLowerDistance = 0
    return oShape

def makeSize(nWidth, nHeight):
    """Create a com.sun.star.awt.Size struct."""
    oSize = createUnoStruct("com.sun.star.awt.Size")
    oSize.Width = nWidth
    oSize.Height = nHeight
    return oSize

def makePoint(nX, nY):
    """Create a com.sun.star.awt.Point struct."""
    oPoint = createUnoStruct("com.sun.star.awt.Point")
    oPoint.X = nX
    oPoint.Y = nY
    return oPoint

######################################################################################
# Lecture d'un style de présentation dans le fichier .lirecouleur
######################################################################################
def handleStyle(styleName):
    """Lecture d'un style de présentation dans le fichier .lirecouleur"""
    if not(styleName in globals()):
        globals()[styleName] = {}

    # read the application data file content
    adata = readAppData()
    if not styleName in adata:
        return False

    # transfer the configuration data in the resulting dict
    for phonid in adata[styleName]:
        globals()[styleName][phonid] = adata[styleName][phonid]
    del adata

    return True

######################################################################################
# Récupération éventuelle des styles de caractères
######################################################################################
__memDocument__ = None
def importStylesLireCouleur(xModel):
    global __memDocument__
    if __memDocument__ == xModel:
        # on n'a pas changé de document donc pas besoin de recharger les styles
        return
    __memDocument__ = xModel

    try:
        """
            Importation des styles à partir d'un fichier odt
        """
        ''' chemin d'accès au fichier qui contient les styles à utiliser '''
        url = getLirecouleurTemplateURL()
        try:
            ppp = createUnoStruct("com.sun.star.beans.PropertyValue")
            ppp.Name = "OverwriteStyles" # on ne veut pas écraser les styles existants
            ppp.Value = False
            res = xModel.getStyleFamilies().loadStylesFromURL(url, (ppp,))
        except:
            pass
        createCharacterStyles(xModel, style_phon_perso, __style_phon_perso__)
        createCharacterStyles(xModel, style_phon_complexes, __style_phon_complexes__)
        createCharacterStyles(xModel, style_syll_dys, __style_syll_dys__)
        createCharacterStyles(xModel, styles_lignes_altern, __styles_lignes_altern__)

        if not handleStyle("style_syll_souligne"):
            try:
                ''' En désespoir de cause, on fait une copie du style de sauvegarde '''
                globals()["styles_syllabes"]["souligne"] = globals()["__style_syll_souligne__"]
                saveAppData("style_syll_souligne", globals()["__style_syll_souligne__"])
            except:
                pass
    except:
        pass

######################################################################################
# Gestionnaire d'événement de la boite de dialogue
######################################################################################
class MyActionListener(unohelper.Base, XActionListener):
    def __init__(self, controlContainer, checkListPhonemes, fieldCoul, fieldEsp, checkPoint,
                    selectTyp1Syll, selectTyp2Syll, selectLoc, fieldTemp):
        self.controlContainer = controlContainer
        self.checkListPhonemes = checkListPhonemes
        self.fieldCoul = fieldCoul
        self.fieldEsp = fieldEsp
        self.checkPoint = checkPoint
        self.selectTyp1Syll = selectTyp1Syll
        self.selectTyp2Syll = selectTyp2Syll
        self.selectLocale = selectLoc
        self.fieldTemp = fieldTemp

    def actionPerformed(self, actionEvent):
        global __style_phon_perso__

        selectphonemes = handleMaskPhonems()
        nbcouleurs = handleMaskAlternate()
        nbespaces = handleMaskSubspaces()
        tempFilename = handleMaskTemplate()

        selectphonemes['a'] = self.checkListPhonemes['checkA'].State
        selectphonemes['e'] = selectphonemes['e_comp'] = self.checkListPhonemes['checkE'].State
        selectphonemes['e^'] = selectphonemes['e^_comp'] = self.checkListPhonemes['checkEt'].State
        selectphonemes['q'] = self.checkListPhonemes['checkQ'].State
        selectphonemes['u'] = self.checkListPhonemes['checkU'].State
        selectphonemes['i'] = self.checkListPhonemes['checkI'].State
        selectphonemes['y'] = self.checkListPhonemes['checkY'].State
        selectphonemes['o'] = selectphonemes['o_comp'] = selectphonemes['o_ouvert'] = self.checkListPhonemes['checkO'].State

        selectphonemes['x'] = selectphonemes['x^'] = self.checkListPhonemes['checkEu'].State
        selectphonemes['a~'] = self.checkListPhonemes['checkAn'].State
        selectphonemes['e~'] = selectphonemes['x~'] = self.checkListPhonemes['checkIn'].State
        selectphonemes['o~'] = self.checkListPhonemes['checkOn'].State
        selectphonemes['w'] = selectphonemes['wa'] = selectphonemes['w5'] = self.checkListPhonemes['checkW'].State
        selectphonemes['j'] = self.checkListPhonemes['checkJ'].State

        selectphonemes['n'] = self.checkListPhonemes['checkN'].State
        selectphonemes['g~'] = self.checkListPhonemes['checkNg'].State
        selectphonemes['n~'] = self.checkListPhonemes['checkGn'].State

        selectphonemes['l'] = self.checkListPhonemes['checkL'].State
        selectphonemes['m'] = self.checkListPhonemes['checkM'].State
        selectphonemes['r'] = self.checkListPhonemes['checkR'].State

        selectphonemes['v'] = self.checkListPhonemes['checkV'].State
        selectphonemes['z'] = selectphonemes['z_s'] = self.checkListPhonemes['checkZ'].State
        selectphonemes['z^'] = selectphonemes['z^_g'] = self.checkListPhonemes['checkGe'].State

        selectphonemes['f'] = selectphonemes['f_ph'] = self.checkListPhonemes['checkF'].State
        selectphonemes['s'] = selectphonemes['s_c'] = selectphonemes['s_t'] = self.checkListPhonemes['checkS'].State
        selectphonemes['s^'] = self.checkListPhonemes['checkCh'].State

        selectphonemes['p'] = self.checkListPhonemes['checkP'].State
        selectphonemes['t'] = self.checkListPhonemes['checkT'].State
        selectphonemes['k'] = selectphonemes['k_qu'] = self.checkListPhonemes['checkK'].State

        selectphonemes['b'] = self.checkListPhonemes['checkB'].State
        selectphonemes['d'] = self.checkListPhonemes['checkD'].State
        selectphonemes['g'] = selectphonemes['g_u'] = self.checkListPhonemes['checkG'].State

        selectphonemes['ks'] = self.checkListPhonemes['checkKS'].State
        selectphonemes['gz'] = self.checkListPhonemes['checkGZ'].State

        selectphonemes['#'] = selectphonemes['q_caduc'] = self.checkListPhonemes['checkH'].State

        nbcouleurs = self.fieldCoul.getValue()
        nbespaces = self.fieldEsp.getValue()
        tempFilename = self.fieldTemp.getText()

        saveMaskPhonems(selectphonemes)
        saveMaskAlternate(int(nbcouleurs))
        saveMaskSubspaces(int(nbespaces))
        saveMaskPoint(self.checkPoint.getState())

        saveMaskSyllo(self.selectTyp1Syll.getSelectedItemPos(), self.selectTyp2Syll.getSelectedItemPos())
        saveMaskTemplate(tempFilename)
        saveMaskCountry(self.selectLocale.getSelectedItem())

        self.controlContainer.endExecute()

class MySetActionListener(unohelper.Base, XActionListener):
    def __init__(self, controlContainer, checkListPhonemes):
        self.controlContainer = controlContainer
        self.checkListPhonemes = checkListPhonemes

    def actionPerformed(self, actionEvent):
        listPhonemes = ['checkA', 'checkE', 'checkEt', 'checkQ', 'checkI',
                        'checkU', 'checkY', 'checkO', 'checkEu',
                        'checkAn', 'checkIn', 'checkOn', 'checkW',
                        'checkJ', 'checkN', 'checkNg', 'checkGn', 'checkB', 'checkD', 'checkG',
                        'checkL', 'checkM', 'checkR', 'checkV', 'checkZ', 'checkGe',
                        'checkF', 'checkS', 'checkCh', 'checkP', 'checkT', 'checkK',
                        'checkKS','checkGZ', 'checkH']
        for phon in listPhonemes:
            self.checkListPhonemes[phon].State = 1

class MyUnsetActionListener(unohelper.Base, XActionListener):
    def __init__(self, controlContainer, checkListPhonemes):
        self.controlContainer = controlContainer
        self.checkListPhonemes = checkListPhonemes

    def actionPerformed(self, actionEvent):
        listPhonemes = ['checkA', 'checkE', 'checkEt', 'checkQ', 'checkI',
                        'checkU', 'checkY', 'checkO', 'checkEu',
                        'checkAn', 'checkIn', 'checkOn', 'checkW',
                        'checkJ', 'checkN', 'checkNg', 'checkGn', 'checkB', 'checkD', 'checkG',
                        'checkL', 'checkM', 'checkR', 'checkV', 'checkZ', 'checkGe',
                        'checkF', 'checkS', 'checkCh', 'checkP', 'checkT', 'checkK',
                        'checkKS','checkGZ', 'checkH']
        for phon in listPhonemes:
            self.checkListPhonemes[phon].State = 0

class TemplateActionListener(unohelper.Base, XActionListener):
    def __init__(self, controlContainer, fieldTemp, xContext):
        self.controlContainer = controlContainer
        self.fieldTemp = fieldTemp
        self.xContext = xContext

    def actionPerformed(self, actionEvent):
        # Get the service manager
        smgr = self.xContext.ServiceManager

        # create the dialog model and set the properties
        oFilePicker = smgr.createInstanceWithContext("com.sun.star.ui.dialogs.FilePicker", self.xContext)
        #oFilePicker.DisplayDirectory = getUserDir()
        oFilePicker.appendFilter("Documents", "*.odt")
        oFilePicker.appendFilter("OTT", "*.ott")
        oFilePicker.CurrentFilter = "Documents"

        if oFilePicker.execute():
            sFiles = oFilePicker.getFiles()
            sFileURL = sFiles[0]
            self.fieldTemp.setText(sFileURL)

######################################################################################
# Création d'une checkbox (pour 1 phonème) dans la boite de dialogue
######################################################################################
def createCheckBox(dialogModel, px, py, name, index, label, etat, w=58):
    checkBP = dialogModel.createInstance("com.sun.star.awt.UnoControlCheckBoxModel")
    checkBP.PositionX = px
    checkBP.PositionY = py
    checkBP.Width  = w
    checkBP.Height = 10
    checkBP.Name = name
    checkBP.TabIndex = index
    checkBP.State = etat
    checkBP.Label = label
    return checkBP

######################################################################################
# Création d'une checkbox (pour 1 phonème) dans la boite de dialogue
######################################################################################
def createNumericField(dialogModel, px, py, name, index, val, w=20):
    checkNF = dialogModel.createInstance("com.sun.star.awt.UnoControlNumericFieldModel")
    checkNF.PositionX = px
    checkNF.PositionY = py
    checkNF.Width  = w
    checkNF.Height = 10
    checkNF.Name = name
    checkNF.TabIndex = index
    checkNF.Value = val
    checkNF.ValueMin = 2
    checkNF.ValueMax = 10
    checkNF.ValueStep = 1
    checkNF.Spin = True
    checkNF.DecimalAccuracy = 0
    return checkNF

######################################################################################
# Création d'une boite de dialogue pour sélectionner les phonèmes à visualiser
######################################################################################
class SelectPhonemes(unohelper.Base, XJobExecutor):
    """Ouvrir une fenêtre de dialogue pour sélectionner les phonèmes à visualiser."""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __creerSelectPhonemesDialog__(desktop.getCurrentComponent(), self.ctx)

def creerSelectPhonemesDialog( args=None ):
    """Ouvrir une fenêtre de dialogue pour sélectionner les phonèmes à visualiser."""
    __creerSelectPhonemesDialog__(XSCRIPTCONTEXT.getDocument(), XSCRIPTCONTEXT.getComponentContext())

def __creerSelectPhonemesDialog__(xDocument, xContext):
    __arret_dynsylldys__(xDocument)

    """Ouvrir une fenêtre de dialogue pour sélectionner les phonèmes à visualiser."""
    import array

    # i18n
    i18n()

    # get the service manager
    smgr = xContext.ServiceManager

    # read the already selected phonemes in the .lirecouleur file
    selectphonemes = handleMaskPhonems()

    # lecture de la période d'alternance de lignes dans le fichier .lirecouleur
    nbcouleurs = handleMaskAlternate()

    # lecture de la période d'alternance de lignes dans le fichier .lirecouleur
    nbespaces = handleMaskSubspaces()

    # lecture pour savoir s'il faut mettre un point sous les lettres muettes dans le fichier .lirecouleur
    selectpoint = handleMaskPoint()

    # lecture pour savoir comment il faut afficher les syllabes dans le fichier .lirecouleur
    selectsyllo = handleMaskSyllo()

    # lecture pour savoir  dans le fichier .lirecouleur
    select_locale = handleMaskCountry()

    # lecture de la période d'alternance de lignes dans le fichier .lirecouleur
    tempFileName = handleMaskTemplate()

    # create the dialog model and set the properties
    dialogModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogModel", xContext)

    dialogModel.PositionX = 100
    dialogModel.PositionY = 50
    dialogModel.Width = 180
    dialogModel.Height = 284
    dialogModel.Title = _("Configuration LireCouleur")

    # créer le label titre
    labelTitre = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    labelTitre.PositionX = 10
    labelTitre.PositionY = 2
    labelTitre.Width  = 130
    labelTitre.Height = 12
    labelTitre.Name = "labelTitre"
    labelTitre.TabIndex = 1
    labelTitre.Label = _(u("Cocher les phonèmes à mettre en évidence"))

    # créer les checkboxes des phonèmes
    i = 2
    checkA = createCheckBox(dialogModel, 10, 30, "checkA", i, u('[~a] ta'), selectphonemes['a'])
    i += 1
    checkQ = createCheckBox(dialogModel, 10, 40, "checkQ", i, u('[~e] le'), selectphonemes['q'])
    i += 1
    checkI = createCheckBox(dialogModel, 10, 50, "checkI", i, u('[~i] il'), selectphonemes['i'])
    i += 1
    checkY = createCheckBox(dialogModel, 10, 60, "checkY", i, u('[~y] tu'), selectphonemes['y'])
    i += 1

    checkU = createCheckBox(dialogModel, 70, 30, "checkU", i, u('[~u] fou'), selectphonemes['u'])
    i += 1
    checkE = createCheckBox(dialogModel, 70, 40, "checkE", i, u('[~é] né'), selectphonemes['e'])
    i += 1
    checkO = createCheckBox(dialogModel, 70, 50, "checkO", i, u('[~o] mot'), selectphonemes['o'])
    i += 1
    checkEt = createCheckBox(dialogModel, 70, 60, "checkEt", i, u('[~è] sel'), selectphonemes['e^'])
    i += 1
    checkAn = createCheckBox(dialogModel, 70, 70, "checkAn", i, u('[~an] grand'), selectphonemes['a~'])
    i += 1

    checkOn = createCheckBox(dialogModel, 130, 30, "checkOn", i, u('[~on] son'), selectphonemes['o~'])
    i += 1
    checkEu = createCheckBox(dialogModel, 130, 40, "checkEu", i, u('[~x] feu'), selectphonemes['x'])
    i += 1
    checkIn = createCheckBox(dialogModel, 130, 50, "checkIn", i, u('[~in] fin'), selectphonemes['e~'])
    i += 1
    checkW = createCheckBox(dialogModel, 130, 60, "checkW", i, u('[~w] noix'), selectphonemes['w'])
    i += 1
    checkJ = createCheckBox(dialogModel, 130, 70, "checkJ", i, u('[~j] fille'), selectphonemes['j'])
    i += 1

    checkNg = createCheckBox(dialogModel, 10, 75, "checkNg", i, u('[~ng] parking'), selectphonemes['g~'])
    i += 1
    checkGn = createCheckBox(dialogModel, 10, 85, "checkGn", i, u('[~gn] ligne'), selectphonemes['n~'])
    i += 1

    checkH = createCheckBox(dialogModel, 70, 85, "checkH", i, u('[#] lettres muettes, e caduc'), selectphonemes['#'], 88)
    i += 1

    checkR = createCheckBox(dialogModel, 130, 95, "checkR", i, u('[~r] rat'), selectphonemes['r'])
    i += 1
    checkL = createCheckBox(dialogModel, 10, 105, "checkL", i, u('[~l] ville'), selectphonemes['l'])
    i += 1
    checkM = createCheckBox(dialogModel, 70, 105, "checkM", i, u('[~m] mami'), selectphonemes['m'])
    i += 1
    checkN = createCheckBox(dialogModel, 130, 105, "checkN", i, u('[~n] âne'), selectphonemes['n'])
    i += 1

    checkV = createCheckBox(dialogModel, 10, 115, "checkV", i, u('[~v] vélo'), selectphonemes['v'])
    i += 1
    checkZ = createCheckBox(dialogModel, 70, 115, "checkZ", i, u('[~z] zoo'), selectphonemes['z'])
    i += 1
    checkGe = createCheckBox(dialogModel, 130, 115, "checkGe", i, u('[~ge] jupe'), selectphonemes['z^'])
    i += 1

    checkF = createCheckBox(dialogModel, 10, 125, "checkF", i, u('[~f] effacer'), selectphonemes['f'])
    i += 1
    checkS = createCheckBox(dialogModel, 70, 125, "checkS", i, u('[~s] scie'), selectphonemes['s'])
    i += 1
    checkCh = createCheckBox(dialogModel, 130, 125, "checkCh", i, u('[c~h] chat'), selectphonemes['s^'])
    i += 1

    checkP = createCheckBox(dialogModel, 10, 135, "checkP", i, u('[~p] papa'), selectphonemes['p'])
    i += 1
    checkT = createCheckBox(dialogModel, 70, 135, "checkT", i, u('[~t] tortue'), selectphonemes['t'])
    i += 1
    checkK = createCheckBox(dialogModel, 130, 135, "checkK", i, u('[~k] coq'), selectphonemes['k'])
    i += 1

    checkB = createCheckBox(dialogModel, 10, 145, "checkB", i, u('[~b] bébé'), selectphonemes['b'])
    i += 1
    checkD = createCheckBox(dialogModel, 70, 145, "checkD", i, u('[~d] dindon'), selectphonemes['d'])
    i += 1
    checkG = createCheckBox(dialogModel, 130, 145, "checkG", i, u('[~g] gare'), selectphonemes['g'])
    i += 1

    checkKS = createCheckBox(dialogModel, 70, 155, "checkKS", i, u('[ks] ksi'), selectphonemes['ks'])
    i += 1
    checkGZ = createCheckBox(dialogModel, 130, 155, "checkGZ", i, u('[gz] exact'), selectphonemes['gz'])
    i += 1

    labelListLocale = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    labelListLocale.PositionX = 10
    labelListLocale.PositionY = checkKS.PositionY+checkKS.Height+2
    labelListLocale.Width  = 50
    labelListLocale.Height = checkKS.Height
    labelListLocale.Name = "labelListLocale"
    labelListLocale.TabIndex = 1
    labelListLocale.Label = "Configuration : "

    listLocale = dialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")
    listLocale.PositionX = labelListLocale.PositionX+labelListLocale.Width
    listLocale.PositionY = labelListLocale.PositionY
    listLocale.Width  = 50
    listLocale.Height  = checkKS.Height
    listLocale.Name = "listLocale"
    listLocale.TabIndex = 1
    listLocale.Dropdown = True
    listLocale.MultiSelection = False
    listLocale.StringItemList = ("fr", "fr_CA", )
    if select_locale in listLocale.StringItemList:
        listLocale.SelectedItems = (listLocale.StringItemList.index(select_locale),)
    else:
        listLocale.SelectedItems = (0,)

    checkListPhonemes = {'checkA':None, 'checkE':None, 'checkEt':None, 'checkQ':None, 'checkI':None,
                        'checkU':None, 'checkY':None, 'checkO':None, 'checkEu':None,
                        'checkAn':None, 'checkIn':None, 'checkOn':None, 'checkW':None,
                        'checkJ':None, 'checkCh':None, 'checkN':None, 'checkNg':None, 'checkGn':None,
                        'checkL':None, 'checkM':None, 'checkR':None,
                        'checkV':None, 'checkZ':None, 'checkGe':None,
                        'checkF':None, 'checkS':None, 'checkCh':None,
                        'checkP':None, 'checkT':None, 'checkK':None,
                        'checkB':None, 'checkD':None, 'checkG':None,
                        'checkKS':None, 'checkGZ':None, 'checkH':None}

    # create the button model and set the properties
    buttonModel = dialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")

    buttonModel.PositionX = 65
    buttonModel.Width = 50
    buttonModel.Height = 14
    buttonModel.PositionY  = dialogModel.Height-buttonModel.Height-2
    buttonModel.Name = "myButtonName"
    buttonModel.TabIndex = 0
    buttonModel.Label = _(u("Valider"))

    # create the button model and set the properties
    setAllModel = dialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    setAllModel.PositionX = 25
    setAllModel.PositionY  = 12
    setAllModel.Width = 60
    setAllModel.Height = 14
    setAllModel.Name = "setAllButtonName"
    setAllModel.TabIndex = 0
    setAllModel.Label = _(u("Tout sélectionner"))

    unsetAllModel = dialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    unsetAllModel.PositionX = 87
    unsetAllModel.PositionY  = 12
    unsetAllModel.Width = 60
    unsetAllModel.Height = 14
    unsetAllModel.Name = "unsetAllButtonName"
    unsetAllModel.TabIndex = 0
    unsetAllModel.Label = _(u("Tout désélectionner"))

    sep1 = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedLineModel")
    sep1.PositionX = 2
    sep1.PositionY = listLocale.PositionY+listLocale.Height+2
    sep1.Width  = dialogModel.Width - 4
    sep1.Height  = 5
    sep1.Name = "sep1"
    sep1.TabIndex = 1

    labelCoul = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    labelCoul.PositionX = 10
    labelCoul.PositionY = sep1.PositionY+sep1.Height+2
    labelCoul.Width  = 145
    labelCoul.Height = 12
    labelCoul.Name = "labelCoul"
    labelCoul.TabIndex = 1
    labelCoul.Label = _(u("Période d'alternance des couleurs (lignes, syllabes) :"))
    fieldCoul = createNumericField(dialogModel, labelCoul.PositionX+labelCoul.Width, labelCoul.PositionY, "fieldCoul", 0, nbcouleurs)

    labelEsp = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    labelEsp.PositionX = 10
    labelEsp.PositionY = fieldCoul.PositionY+fieldCoul.Height
    labelEsp.Width  = 105
    labelEsp.Height = 12
    labelEsp.Name = "labelEsp"
    labelEsp.TabIndex = 1
    labelEsp.Label = _(u("Nombre d'espaces entre deux mots :"))
    fieldEsp = createNumericField(dialogModel, labelEsp.PositionX+labelEsp.Width, labelEsp.PositionY, "fieldEsp", 0, nbespaces)

    sep2 = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedLineModel")
    sep2.PositionX = sep1.PositionX
    sep2.PositionY = labelEsp.PositionY+labelEsp.Height
    sep2.Width  = sep1.Width
    sep2.Height  = sep1.Height
    sep2.Name = "sep2"
    sep2.TabIndex = 1

    checkPoint = createCheckBox(dialogModel, 10, sep2.PositionY+sep2.Height, "checkPoint", 0,
                    _(u("Placer un point sous les lettres muettes")), selectpoint, dialogModel.Width-10)

    labelRadio = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    labelRadio.PositionX = 10
    labelRadio.PositionY = checkPoint.PositionY+checkPoint.Height+2
    labelRadio.Width  = dialogModel.Width-100-12
    labelRadio.Height = 10
    labelRadio.Name = "labelRadio"
    labelRadio.TabIndex = 1
    labelRadio.Label = _(u("Souligner les syllabes"))

    listTyp1Syll = dialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")
    listTyp1Syll.PositionX = labelRadio.PositionX+labelRadio.Width
    listTyp1Syll.PositionY = labelRadio.PositionY-2
    listTyp1Syll.Width  = 50
    listTyp1Syll.Height  = 12
    listTyp1Syll.Name = "listTyp1Syll"
    listTyp1Syll.TabIndex = 1
    listTyp1Syll.Dropdown = True
    listTyp1Syll.MultiSelection = False
    listTyp1Syll.StringItemList = ("LireCouleur", "standard", )
    if selectsyllo[0] in [0, 1]:
        listTyp1Syll.SelectedItems = (selectsyllo[0],)
    else:
        listTyp1Syll.SelectedItems = (0,)

    listTyp2Syll = dialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")
    listTyp2Syll.PositionX = listTyp1Syll.PositionX+listTyp1Syll.Width
    listTyp2Syll.PositionY = listTyp1Syll.PositionY
    listTyp2Syll.Width  = 50
    listTyp2Syll.Height  = listTyp1Syll.Height
    listTyp2Syll.Name = "listTyp2Syll"
    listTyp2Syll.TabIndex = 1
    listTyp2Syll.Dropdown = True
    listTyp2Syll.MultiSelection = False
    listTyp2Syll.StringItemList = ( _(u("écrites")), _(u("orales")) )
    if selectsyllo[1] in [0, 1]:
        listTyp2Syll.SelectedItems = (selectsyllo[1],)
    else:
        listTyp2Syll.SelectedItems = (0,)

    sep3 = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedLineModel")
    sep3.PositionX = sep1.PositionX
    sep3.PositionY = labelRadio.PositionY+labelRadio.Height+2
    sep3.Width  = sep1.Width
    sep3.Height  = sep1.Height
    sep3.Name = "sep3"
    sep3.TabIndex = 1

    labelTemp = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    labelTemp.PositionX = 10
    labelTemp.PositionY = sep3.PositionY+sep3.Height
    labelTemp.Width  = dialogModel.Width-12
    labelTemp.Height = 10
    labelTemp.Name = "labelTemp"
    labelTemp.TabIndex = 1
    labelTemp.Label = _(u("Nom du fichier modèle :"))

    fieldTemp = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel")
    fieldTemp.PositionX = 10
    fieldTemp.PositionY  = labelTemp.PositionY+labelTemp.Height
    fieldTemp.Width = dialogModel.Width-42
    fieldTemp.Height = 14
    fieldTemp.Name = "fieldTemp"
    fieldTemp.TabIndex = 0

    buttTemp = dialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    buttTemp.PositionX = fieldTemp.PositionX+fieldTemp.Width+2
    buttTemp.PositionY  = fieldTemp.PositionY
    buttTemp.Width = dialogModel.Width-buttTemp.PositionX-2
    buttTemp.Height = fieldTemp.Height
    buttTemp.Name = "buttTemp"
    buttTemp.TabIndex = 0
    buttTemp.Label = "..."

    # insert the control models into the dialog model
    dialogModel.insertByName("setAllButtonName", setAllModel)
    dialogModel.insertByName("unsetAllButtonName", unsetAllModel)
    dialogModel.insertByName("myButtonName", buttonModel)
    dialogModel.insertByName("labelTitre", labelTitre)

    dialogModel.insertByName("labelCoul", labelCoul)
    dialogModel.insertByName("fieldCoul", fieldCoul)

    dialogModel.insertByName("labelEsp", labelEsp)
    dialogModel.insertByName("fieldEsp", fieldEsp)

    dialogModel.insertByName("sep1", sep1)
    dialogModel.insertByName("sep2", sep2)
    dialogModel.insertByName("sep3", sep3)
    dialogModel.insertByName("checkA", checkA)
    dialogModel.insertByName("checkE", checkE)
    dialogModel.insertByName("checkEt", checkEt)
    dialogModel.insertByName("checkQ", checkQ)
    dialogModel.insertByName("checkI", checkI)
    dialogModel.insertByName("checkU", checkU)
    dialogModel.insertByName("checkY", checkY)
    dialogModel.insertByName("checkO", checkO)
    dialogModel.insertByName("checkEu", checkEu)
    dialogModel.insertByName("checkAn", checkAn)
    dialogModel.insertByName("checkIn", checkIn)
    dialogModel.insertByName("checkOn", checkOn)
    dialogModel.insertByName("checkW", checkW)
    dialogModel.insertByName("checkJ", checkJ)
    dialogModel.insertByName("checkN", checkN)
    dialogModel.insertByName("checkNg", checkNg)
    dialogModel.insertByName("checkGn", checkGn)
    dialogModel.insertByName("checkH", checkH)

    dialogModel.insertByName("checkL", checkL)
    dialogModel.insertByName("checkM", checkM)
    dialogModel.insertByName("checkR", checkR)

    dialogModel.insertByName("checkV", checkV)
    dialogModel.insertByName("checkZ", checkZ)
    dialogModel.insertByName("checkGe", checkGe)

    dialogModel.insertByName("checkF", checkF)
    dialogModel.insertByName("checkS", checkS)
    dialogModel.insertByName("checkCh", checkCh)

    dialogModel.insertByName("checkP", checkP)
    dialogModel.insertByName("checkT", checkT)
    dialogModel.insertByName("checkK", checkK)

    dialogModel.insertByName("checkB", checkB)
    dialogModel.insertByName("checkD", checkD)
    dialogModel.insertByName("checkG", checkG)

    dialogModel.insertByName("checkKS", checkKS)
    dialogModel.insertByName("checkGZ", checkGZ)

    dialogModel.insertByName("checkPoint", checkPoint)
    dialogModel.insertByName(labelListLocale.Name, labelListLocale)
    dialogModel.insertByName(listLocale.Name, listLocale)

    dialogModel.insertByName("labelTemp", labelTemp)
    dialogModel.insertByName("fieldTemp", fieldTemp)
    dialogModel.insertByName("buttTemp", buttTemp)

    dialogModel.insertByName(labelRadio.Name, labelRadio)
    dialogModel.insertByName(listTyp1Syll.Name, listTyp1Syll)
    dialogModel.insertByName(listTyp2Syll.Name, listTyp2Syll)

    # create the dialog control and set the model
    controlContainer = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", xContext);
    controlContainer.setModel(dialogModel);

    # add the action listener
    for k in checkListPhonemes:
        checkListPhonemes[k] = controlContainer.getControl(k)
    controlContainer.getControl("myButtonName").addActionListener(MyActionListener(controlContainer, checkListPhonemes,
                                controlContainer.getControl("fieldCoul"),
                                controlContainer.getControl("fieldEsp"),
                                controlContainer.getControl("checkPoint"),
                                controlContainer.getControl(listTyp1Syll.Name),
                                controlContainer.getControl(listTyp2Syll.Name),
                                controlContainer.getControl(listLocale.Name),
                                controlContainer.getControl("fieldTemp")))
    controlContainer.getControl("setAllButtonName").addActionListener(MySetActionListener(controlContainer, checkListPhonemes))
    controlContainer.getControl("unsetAllButtonName").addActionListener(MyUnsetActionListener(controlContainer, checkListPhonemes))
    controlContainer.getControl("buttTemp").addActionListener(TemplateActionListener(controlContainer, controlContainer.getControl("fieldTemp"), xContext))

    if len(tempFileName) > 0:
        controlContainer.getControl("fieldTemp").setText(tempFileName)

    # create a peer
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.ExtToolkit", xContext)

    controlContainer.setVisible(False);
    controlContainer.createPeer(toolkit, None);

    # execute it
    controlContainer.execute()

    # dispose the dialog
    controlContainer.dispose()

######################################################################################
# Création d'une boite de dialogue pour gérer le dictionnaire des décodages spéciaux
######################################################################################
def checkMethodParameter(interface_name, method_name, param_index, param_type):
    """ Check the method has specific type parameter at the specific position. """
    cr = createUnoService("com.sun.star.reflection.CoreReflection")
    try:
        idl = cr.forName(interface_name)
        m = idl.getMethod(method_name)
        if m:
            info = m.getParameterInfos()[param_index]
            return info.aType.getName() == param_type
    except:
        pass
    return False

def MsgBox(parent, toolkit=None, message="message", title="", message_type="errorbox", buttons=BUTTONS_OK):
    """ Show message in message box. """
    if toolkit is None:
        toolkit = parent.getToolkit()
    older_imple = checkMethodParameter(
        "com.sun.star.awt.XMessageBoxFactory",
        "createMessageBox", 1, "com.sun.star.awt.Rectangle")

    if older_imple:
        msgboxdial = toolkit.createMessageBox(parent, Rectangle(), message_type, buttons, title, message)
    else:
        msgboxdial = toolkit.createMessageBox(parent, message_type, buttons, title, message)
    n = msgboxdial.execute()
    msgboxdial.dispose()
    return n

class DictListActionListener(unohelper.Base, XActionListener):
    """Gestionnaire d'événement : double-clic sur un élément de la liste du dico de décodage"""
    def __init__(self, listdict, field1, field2, field3):
        self.listdict = listdict
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def actionPerformed(self, actionEvent):
        key = self.listdict.getSelectedItem()
        self.field1.setText(key)
        entry = getLCDictEntry(key)
        self.field2.setText(entry[0])
        self.field3.setText(entry[1])

class DictAddActionListener(unohelper.Base, XActionListener):
    """Gestionnaire d'événement : ajout d'une entrée dans le dico de décodage"""
    def __init__(self, listdict, field1, field2, field3, parent, toolkit=None):
        self.listdict = listdict
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.parent = parent
        self.toolkit = toolkit

    def actionPerformed(self, actionEvent):
        # existe déjà ?
        key = self.field1.getText().strip().lower()
        phon = self.field2.getText().strip()
        syll = self.field3.getText().strip()

        ctrl = ''.join([ph.split('.')[0] for ph in re.split('/', phon)])
        if len(ctrl) > 0 and key != ctrl:
            # les phonèmes ne redonnent pas le mot utilisé comme clé d'index
            ctrl = '/'.join([ph.split('.')[0] for ph in re.split('/', phon)])
            MsgBox(self.parent, self.toolkit, _(u("Phonèmes"))+' : '+key+' <=> '+ctrl+' ... incorrect')
            return

        ctrl = ''.join(syll.split('/'))
        if len(ctrl) > 0 and key != ctrl:
            # les syllabes ne redonnent pas le mot utilisé comme clé d'index
            MsgBox(self.parent, self.toolkit, _(u("Syllabes"))+' : '+key+' <=> '+syll+' ... incorrect')
            return

        deja_la = False
        try:
            deja_la = key in self.listdict.StringItemList
        except:
            pass

        if not deja_la:
            self.listdict.insertItemText(len(self.listdict.StringItemList), key)
        setLCDictEntry(key, phon, syll)

class DictRemActionListener(unohelper.Base, XActionListener):
    """Gestionnaire d'événement : suppression d'une entrée dans le dico de décodage"""
    def __init__(self, controlContainer, listdict):
        self.controlContainer = controlContainer
        self.listdict = listdict
        self.listdictControl = controlContainer.getControl(listdict.Name)

    def actionPerformed(self, actionEvent):
        if self.listdictControl.getSelectedItemPos() >= 0:
            delLCDictEntry(self.listdictControl.getSelectedItem())
            self.listdict.removeItem(self.listdictControl.getSelectedItemPos())

class GestionnaireDictionaire(unohelper.Base, XJobExecutor):
    """Ouvrir une fenêtre de dialogue pour gérer le dictionnaire des décodages spéciaux."""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __gererDictionnaireDialog__(desktop.getCurrentComponent(), self.ctx)

def gererDictionnaireDialog( args=None ):
    """Ouvrir une fenêtre de dialogue pour gérer le dictionnaire des décodages spéciaux."""
    __gererDictionnaireDialog__(XSCRIPTCONTEXT.getDocument(), XSCRIPTCONTEXT.getComponentContext())

def __gererDictionnaireDialog__(xDocument, xContext):
    __arret_dynsylldys__(xDocument)

    """Ouvrir une fenêtre de dialogue pour gérer le dictionnaire des décodages spéciaux."""
    # i18n
    i18n()

    # charge le dictionnaire si cela n'est pas encore fait
    loadLCDict(getLirecouleurDictionary())

    # get the service manager
    smgr = xContext.ServiceManager

    # create the dialog model and set the properties
    dialogModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogModel", xContext)

    dialogModel.PositionX = 100
    dialogModel.PositionY = 50
    dialogModel.Width = 300
    dialogModel.Height = 150
    dialogModel.Title = _(u("Dictionnaire LireCouleur"))

    buttAdd = dialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    buttAdd.Width = 20
    buttAdd.Height = 20
    buttAdd.PositionX = dialogModel.Width/2-buttAdd.Width-2
    buttAdd.PositionY  = dialogModel.Height-2-buttAdd.Height
    buttAdd.Name = "buttAdd"
    buttAdd.TabIndex = 0
    buttAdd.Label = "+"

    buttRem = dialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    buttRem.Width = 20
    buttRem.Height = 20
    buttRem.PositionX = dialogModel.Width/2+2
    buttRem.PositionY  = buttAdd.PositionY
    buttRem.Name = "buttRem"
    buttRem.TabIndex = 0
    buttRem.Label = "-"

    sep = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedLineModel")
    sep.PositionX = 5
    sep.PositionY = buttAdd.PositionY-40
    sep.Width  = dialogModel.Width-2*sep.PositionX
    sep.Height  = 10
    sep.Name = "sep"
    sep.TabIndex = 1

    label1 = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    label1.PositionX = 2
    label1.PositionY = sep.PositionY+sep.Height
    label1.Width  = 70
    label1.Height = 10
    label1.Name = "label1"
    label1.TabIndex = 1
    label1.Label = _(u("Entrée dictionnaire"))

    label2 = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    label2.PositionX = label1.PositionX+label1.Width+2
    label2.PositionY = label1.PositionY
    label2.Width  = 130
    label2.Height = 10
    label2.Name = "label2"
    label2.TabIndex = 1
    label2.Label = _(u("Phonèmes"))

    label3 = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    label3.PositionX = label2.PositionX+label2.Width+2
    label3.PositionY = label1.PositionY
    label3.Width  = dialogModel.Width-2-label3.PositionX
    label3.Height = 10
    label3.Name = "label3"
    label3.TabIndex = 1
    label3.Label = _(u("Syllabes"))

    field1 = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel")
    field1.PositionX = label1.PositionX
    field1.PositionY  = label1.PositionY+label1.Height
    field1.Width = label1.Width
    field1.Height = 14
    field1.Name = "field1"
    field1.TabIndex = 0

    field2 = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel")
    field2.PositionX = label2.PositionX
    field2.PositionY  = label2.PositionY+label2.Height
    field2.Width = label2.Width
    field2.Height = 14
    field2.Name = "field2"
    field2.TabIndex = 0

    field3 = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel")
    field3.PositionX = label3.PositionX
    field3.PositionY  = label3.PositionY+label3.Height
    field3.Width = label3.Width
    field3.Height = 14
    field3.Name = "field3"
    field3.TabIndex = 0

    listdic = dialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")
    listdic.PositionX = 2
    listdic.PositionY = 2
    listdic.Width  = dialogModel.Width-2-listdic.PositionX
    listdic.Height  = sep.PositionY-listdic.PositionY
    listdic.Name = "listdic"
    listdic.TabIndex = 1
    listdic.Dropdown = False
    listdic.MultiSelection = False
    listdic.StringItemList = tuple(getLCDictKeys())

    dialogModel.insertByName(label1.Name, label1)
    dialogModel.insertByName(label2.Name, label2)
    dialogModel.insertByName(label3.Name, label3)
    dialogModel.insertByName(field1.Name, field1)
    dialogModel.insertByName(field2.Name, field2)
    dialogModel.insertByName(field3.Name, field3)
    dialogModel.insertByName(sep.Name, sep)
    dialogModel.insertByName(buttAdd.Name, buttAdd)
    dialogModel.insertByName(buttRem.Name, buttRem)
    dialogModel.insertByName(listdic.Name, listdic)

    # create the dialog control and set the model
    controlContainer = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", xContext);
    controlContainer.setModel(dialogModel)

    # create a peer
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.ExtToolkit", xContext)

    controlContainer.getControl(listdic.Name).addActionListener(DictListActionListener(
            controlContainer.getControl(listdic.Name),
            controlContainer.getControl(field1.Name),
            controlContainer.getControl(field2.Name),
            controlContainer.getControl(field3.Name)))
    oParentWin = xDocument.getCurrentController().getFrame().getContainerWindow()
    controlContainer.getControl(buttAdd.Name).addActionListener(DictAddActionListener(
            listdic,
            controlContainer.getControl(field1.Name),
            controlContainer.getControl(field2.Name),
            controlContainer.getControl(field3.Name),
            oParentWin,
            toolkit))
    controlContainer.getControl(buttRem.Name).addActionListener(DictRemActionListener(controlContainer, listdic))

    controlContainer.setVisible(False);
    controlContainer.createPeer(toolkit, None);

    # execute it
    controlContainer.execute()

    # dispose the dialog
    controlContainer.dispose()

######################################################################################
# Place un point sous une lettre muette
######################################################################################
def marquePoint(xDocument, txt_phon, cursor):
    from com.sun.star.text.TextContentAnchorType import AT_CHARACTER
    from com.sun.star.text.WrapTextMode import THROUGHT
    from com.sun.star.text.RelOrientation import CHAR
    from com.sun.star.text.HoriOrientation import LEFT
    from com.sun.star.text.VertOrientation import CHAR_BOTTOM

    xText = cursor.getText()
    oWindow = xDocument.getCurrentController().getFrame().getContainerWindow()

    xViewCursorSupplier = xDocument.getCurrentController()
    xTextViewCursor = xViewCursorSupplier.getViewCursor()
    xTextViewCursor.gotoRange(cursor, False) # remet le curseur physique au début (du mot)
    x0 = xTextViewCursor.Position.X

    hh = cursor.getPropertyValue("CharHeight")

    # déplace le curseur physique pour calculer la longueur de la cuvette à dessiner
    xTextViewCursor.goRight(len(txt_phon), False)
    x1 = xTextViewCursor.Position.X
    if x1 < x0:
        xTextViewCursor.goLeft(len(txt_phon), False)
        xTextViewCursor.gotoEndOfLine(False)
        x1 = xTextViewCursor.Position.X
    ll = x1 - x0 # longueur de la place

    # définition de l'arc de cercle (cuvette)
    sz = makeSize(hh*8, hh*8)
    oShape = makeShape(xDocument, "com.sun.star.drawing.EllipseShape")
    oShape.Title= '__l_muette__'
    oShape.LineWidth = hh
    oShape.Size = sz

    # ces lignes sont à placer AVANT le "insertTextContent" pour que la forme soit bien configurée
    oShape.AnchorType = AT_CHARACTER # com.sun.star.text.TextContentAnchorType.AT_CHARACTER
    oShape.HoriOrient = LEFT # com.sun.star.text.HoriOrientation.LEFT
    oShape.LeftMargin = (ll-sz.Width)/2
    oShape.HoriOrientRelation = CHAR # com.sun.star.text.RelOrientation.CHAR
    oShape.VertOrient = CHAR_BOTTOM # com.sun.star.text.VertOrientation.CHAR_BOTTOM
    oShape.VertOrientRelation = CHAR # com.sun.star.text.RelOrientation.CHAR

    # insertion de la forme dans le texte à la position du curseur
    xText.insertTextContent(cursor, oShape, False)
    cursor = deplacerADroite(txt_phon, cursor)

    # cette ligne est à placer APRÈS le "insertTextContent" qui écrase la propriété
    oShape.TextWrap = THROUGHT

    oShape.FillColor = 0x00888888
    oShape.LineStyle = 0

    return cursor

###################################################################################
# Applique un style de caractères donné
###################################################################################
def setStyle(styl, ooocursor):
    for kpv in styl:
        try:
            ooocursor.setPropertyValue(kpv, styl[kpv])
        except:
            pass

###################################################################################
# Insertion d'une chaîne de caractères selon un style donné. Retourne la position
# suivante à laquelle insérer sous la forme d'un curseur
###################################################################################
def deplacerADroite(texte, ooocursor):
    try:
        ooocursor.goRight(len(texte), False)
    except:
        pass

    return ooocursor

###################################################################################
# Insertion d'une chaîne de caractères selon un style donné. Retourne la position
# suivante à laquelle insérer sous la forme d'un curseur
###################################################################################
def formaterTexte(texte, ooocursor, style, choix_styl):
    lgr_texte = len(texte)

    # coloriage du phonème courant
    try:
        ncurs = ooocursor.getText().createTextCursorByRange(ooocursor)
        ncurs.goRight(lgr_texte, True)
        if choix_styl == "defaut":
            ncurs.setPropertyToDefault("CharStyleName")
            ncurs.setPropertyToDefault("ParaLineSpacing")
            ncurs.setPropertyToDefault("CharKerning")
            ncurs.setPropertyToDefault("CharHeight")
            ncurs.setPropertyToDefault("CharBackColor")
            #ncurs.setAllPropertiesToDefault()
        elif choix_styl == "noir":
            ncurs.setPropertyToDefault("CharStyleName")
            ncurs.setPropertyToDefault("CharBackColor")
        else:
            setStyle(style[choix_styl], ncurs)
        del ncurs
    except:
        pass

    # déplacer le curseur après le phonème courant
    return deplacerADroite(texte, ooocursor)

###################################################################################
# Transcode les phonèmes en couleurs selon le style choisi
###################################################################################
def code_phonemes(xDocument, phonemes, style, cursor, selecteurphonemes=None, point_lmuette=False):
    stylphon = ''
    nb_phon = len(phonemes)
    i_phon = range(nb_phon)

    cur = cursor
    for i in i_phon:
        phon = phonemes[i]

        if len(phon) > 0:
            stylphon = phon[0]
            txt_phon = phon[1]

            if len(stylphon) == 0:
                cur = deplacerADroite(txt_phon, cur)
            else:
                # voir si le phonème est sélectionné ou non pour affichage
                try:
                    if selecteurphonemes[stylphon] == 0:
                        stylphon = ''
                except:
                    stylphon = ''

                # insertion du texte
                if len(stylphon) == 0:
                    # pas de style : déplacer simplement le curseur
                    cur = deplacerADroite(txt_phon, cur)
                else:
                    if stylphon in styles_phonemes[style]:
                        # appliquer le style demandé
                        cur = formaterTexte(txt_phon, cur, styles_phonemes[style], stylphon)
                        if stylphon == '#' and point_lmuette and xDocument.supportsService("com.sun.star.text.TextDocument"):
                            cur.goLeft(len(txt_phon), False)
                            cur = marquePoint(xDocument, txt_phon, cur)
                    else:
                        # style non défini : appliquer le style par défaut
                        cur = formaterTexte(txt_phon, cur, styles_phonemes[style], '')

    return cur

###################################################################################
# Transcode les syllabes selon le style choisi
###################################################################################
def code_syllabes(xDocument, syllabes, isyl, style, cursor, nb_altern=3):
    import math
    from com.sun.star.text.TextContentAnchorType import AT_CHARACTER
    from com.sun.star.text.WrapTextMode import THROUGHT
    from com.sun.star.text.RelOrientation import CHAR
    from com.sun.star.text.HoriOrientation import LEFT
    from com.sun.star.text.VertOrientation import CHAR_BOTTOM
    from com.sun.star.drawing.FillStyle import NONE
    from com.sun.star.drawing.CircleKind import ARC

    sz_syllabes = len(syllabes)
    nisyl = isyl

    if style == 'souligne' and xDocument.supportsService("com.sun.star.text.TextDocument"):
        try:
            """
                Traitement par ajout de formes coupes en arc de cercle pour indiquer les syllabes
            """
            #if sz_syllabes < 2:
                #return deplacerADroite(syllabes[0], cursor), nisyl

            xText = cursor.getText()
            oWindow = xDocument.getCurrentController().getFrame().getContainerWindow()
            mot = pretraitement_texte(''.join(syllabes).lower())

            xViewCursorSupplier = xDocument.getCurrentController()
            xTextViewCursor = xViewCursorSupplier.getViewCursor()
            xTextViewCursor.gotoRange(cursor, False) # remet le curseur physique au début (du mot)
            x1 = xTextViewCursor.Position.X

            hh = cursor.getPropertyValue("CharHeight")
            for j in range(sz_syllabes):
                # déplace le curseur physique pour calculer la longueur de la cuvette à dessiner
                x0 = x1
                xTextViewCursor.goRight(len(syllabes[j]), False)
                x1 = xTextViewCursor.Position.X
                if x1 < x0:
                    xTextViewCursor.goLeft(len(syllabes[j]), False)
                    xTextViewCursor.gotoEndOfLine(False)
                    x1 = xTextViewCursor.Position.X
                ll = x1 - x0 # longueur de la cuvette

                # définition de l'arc de cercle (cuvette)
                sz = makeSize(ll, min(hh*25, 600))
                oShape = makeShape(xDocument, "com.sun.star.drawing.EllipseShape")
                oShape.Title= '__'+mot+'__'
                #oShape.FillStyle = uno.getConstantByName("com.sun.star.drawing.FillStyle.NONE")
                # Bug https://bugs.freedesktop.org/show_bug.cgi?id=66031
                # uno.getConstantByName no longer works for enum members
                oShape.FillStyle = NONE
                #oShape.CircleKind = uno.getConstantByName("com.sun.star.drawing.CircleKind.ARC")
                # Bug https://bugs.freedesktop.org/show_bug.cgi?id=66031
                # uno.getConstantByName no longer works for enum members
                oShape.CircleKind = ARC
                oShape.CircleStartAngle = -6*math.pi*1000
                oShape.CircleEndAngle = 0
                oShape.LineWidth = hh
                oShape.Size = sz

                # ces lignes sont à placer AVANT le "insertTextContent" pour que la forme soit bien configurée
                oShape.AnchorType = AT_CHARACTER # com.sun.star.text.TextContentAnchorType.AT_CHARACTER
                oShape.HoriOrient = LEFT # com.sun.star.text.HoriOrientation.LEFT
                oShape.HoriOrientPosition = 0
                oShape.HoriOrientRelation = CHAR # com.sun.star.text.RelOrientation.CHAR
                oShape.VertOrient = CHAR_BOTTOM # com.sun.star.text.VertOrientation.CHAR_BOTTOM
                oShape.VertOrientPosition = 0
                oShape.VertOrientRelation = CHAR # com.sun.star.text.RelOrientation.CHAR

                # insertion de la forme dans le texte à la position du curseur
                xText.insertTextContent(cursor, oShape, False)
                cursor = deplacerADroite(syllabes[j], cursor)

                # cette ligne est à placer APRÈS le "insertTextContent" qui écrase la propriété
                oShape.TextWrap = THROUGHT

            return cursor, nisyl
        except:
            pass

    """
        Traitement par coloriage des syllabes (affectation d'un style de caractère)
    """
    for j in range(sz_syllabes):
        cursor = formaterTexte(syllabes[j], cursor, styles_syllabes[style], str(nisyl+1))
        nisyl += 1
        nisyl = nisyl%nb_altern

    return cursor, nisyl

###################################################################################
# Récupère le textRange correspondant au mot sous le curseur ou à la sélection
###################################################################################
def getXCellTextRange(xDocument, xCursor):
    xTextRanges = []
    if xCursor.supportsService("com.sun.star.text.TextTableCursor"):
        cellRangeName = xCursor.getRangeName()
        #print(cellRangeName)
        startColumn = cellRangeName.split(':')[0][0]
        endColumn = cellRangeName.split(':')[1][0]
        startRow = cellRangeName.split(':')[0][1]
        endRow = cellRangeName.split(':')[1][1]
        oTable = xDocument.getCurrentController().getViewCursor().TextTable #########
        for col in range(ord(startColumn)-64, ord(endColumn)-63):
            for row in range(int(startRow), int(endRow)+1):
                cellName = chr(col+64)+str(row)
                cell = oTable.getCellByName(cellName)
                try:
                    xTextRanges.append(cell.getText().createTextCursorByRange(cell))
                except:
                    pass
    return xTextRanges

def extraitMots(xCursor):
    """
        Extrait les mots d'un curseur de texte
    """
    lWordCursors = []
    xText = xCursor.getText() ## get the XText interface
    xtr_p = xText.createTextCursorByRange(xCursor)

    xtr_p.collapseToStart()
    xtr_p.gotoEndOfWord(True)
    while xtr_p.getText().compareRegionEnds(xtr_p, xCursor) > 0:
        # mot par mot
        if not xtr_p.isCollapsed():
            lWordCursors.append(xText.createTextCursorByRange(xtr_p))
        if not xtr_p.gotoNextWord(False):
            break
        xtr_p.gotoEndOfWord(True)

    # dernier morceau de mot
    if not xtr_p.isCollapsed():
        lWordCursors.append(xText.createTextCursorByRange(xtr_p))
    del xtr_p
    return lWordCursors

def segmenteParagraphe(xCursor):
    """
        Segmente un paragraphe en mots et non mots
    """
    lCursors = []
    xText = xCursor.getText() ## get the XText interface
    xtr_p = xText.createTextCursorByRange(xCursor)

    xtr_p.collapseToStart()
    xtr_p.gotoEndOfWord(True)
    while xtr_p.getText().compareRegionEnds(xtr_p, xCursor) > 0:
        # mot par mot
        if not xtr_p.isCollapsed():
            lCursors.append(xText.createTextCursorByRange(xtr_p))
        xtr_p.collapseToEnd()
        if not xtr_p.gotoNextWord(True):
            break
        if not xtr_p.isCollapsed():
            lCursors.append(xText.createTextCursorByRange(xtr_p))
        xtr_p.collapseToEnd()
        xtr_p.gotoEndOfWord(True)

    # dernier morceau de mot
    if not xtr_p.isCollapsed():
        lCursors.append(xText.createTextCursorByRange(xtr_p))
    del xtr_p
    return lCursors

def getXTextRange(xDocument, mode=0):
    """
        Récupère le textRange correspondant au mot sous le curseur ou à la sélection
        mode = 0 : récupère le bloc de texte sélectionné
        mode = 1 : récupère le bloc segmenté en paragraphes
        mode = 2 : récupère le bloc segmenté en phrases
        mode = autre : récupère le bloc segmenté en unités de traitement les plus petites possibles
    """

    if not xDocument.supportsService("com.sun.star.text.TextDocument"):
        return []

    # Importer les styles de coloriage de texte
    importStylesLireCouleur(xDocument)

    #the writer controller impl supports the css.view.XSelectionSupplier interface
    xSelectionSupplier = xDocument.getCurrentController()
    xIndexAccess = xSelectionSupplier.getSelection()

    if xIndexAccess.supportsService("com.sun.star.text.TextTableCursor"):
        return getXCellTextRange(xDocument, xIndexAccess)

    xTextRanges = []
    count = 0
    try:
        count = xIndexAccess.getCount()
    except:
        return None

    xTextRange = xIndexAccess.getByIndex(0)
    theString = xTextRange.getString()
    xText = xTextRange.getText() ## get the XText interface

    if len(theString)==0:
        # pas de texte sélectionné, il faut chercher le mot positionné sous le curseur
        try:
            xWordCursor = xText.createTextCursorByRange(xTextRange)
            if not xWordCursor.isStartOfWord():
                xWordCursor.gotoStartOfWord(False)
            xWordCursor.gotoEndOfWord(True)
            xTextRanges.append(xWordCursor)
        except:
            pass
        return xTextRanges

    # Premier cas : lecture globale de tout ce qui a été sélectionné
    xtr_p = xText.createTextCursorByRange(xTextRange)
    if mode == 0:
        # récupération du bloc de texte sélectionné
        xTextRanges.append(xtr_p)
        return xTextRanges

    xtr_p.collapseToStart()
    if not xtr_p.isStartOfWord():
        xtr_p.gotoStartOfWord(False)
    xtr_p.gotoEndOfParagraph(True)

    # Deuxième cas : lecture paragraphe par paragraphe
    if mode == 1 or xtr_p.getText().compareRegionEnds(xtr_p, xTextRange) > 0:
        while xtr_p.getText().compareRegionEnds(xtr_p, xTextRange) > 0:
            # paragraphe par paragraphe
            if not xtr_p.isCollapsed():
                xTextRanges.append(xText.createTextCursorByRange(xtr_p))
            if not xtr_p.gotoNextParagraph(False):
                break
            xtr_p.gotoEndOfParagraph(True)

        # dernier morceau de paragraphe
        xtr_p.gotoRange(xTextRange, False)
        xtr_p.collapseToEnd()
        if not xtr_p.isEndOfWord():
            xtr_p.gotoEndOfWord(False)
        xtr_p.gotoStartOfParagraph(True)
        if xtr_p.getText().compareRegionStarts(xtr_p, xTextRange) > 0:
            xTextRanges.append(xText.createTextCursorByRange(xTextRange))
        else:
            if not xtr_p.isCollapsed():
                xTextRanges.append(xText.createTextCursorByRange(xtr_p))
        del xtr_p
        return xTextRanges

    # Troisième cas : lecture phrase par phrase
    xtr_p.collapseToStart()
    xtr_p.gotoEndOfSentence(True)
    if mode == 2 or xtr_p.getText().compareRegionEnds(xtr_p, xTextRange) > 0:
        # fin de phrase avant fin de sélection : on procède phrase par phrase
        while xtr_p.getText().compareRegionEnds(xtr_p, xTextRange) > 0:
            # phrase par phrase
            if not xtr_p.isCollapsed():
                xTextRanges.append(xText.createTextCursorByRange(xtr_p))
            if not xtr_p.gotoNextSentence(False):
                break
            xtr_p.gotoEndOfSentence(True)
        
        # dernier morceau de phrase
        xtr_p.gotoRange(xTextRange, False)
        xtr_p.collapseToEnd()
        if not xtr_p.isEndOfWord():
            xtr_p.gotoEndOfWord(False)
        xtr_p.collapseToEnd()
        xtr_p.gotoStartOfSentence(True)
        if not xtr_p.isCollapsed():
            xTextRanges.append(xText.createTextCursorByRange(xtr_p))
        del xtr_p
        return xTextRanges

    # Quatrième cas : lecture mot par mot
    xtr_p.collapseToStart()
    xtr_p.gotoEndOfWord(True)
    while xtr_p.getText().compareRegionEnds(xtr_p, xTextRange) > 0:
        # mot par mot
        if not xtr_p.isCollapsed():
            xTextRanges.append(xText.createTextCursorByRange(xtr_p))
        if not xtr_p.gotoNextWord(False):
            break
        xtr_p.gotoEndOfWord(True)

    # dernier morceau de mot
    if not xtr_p.isCollapsed():
        xTextRanges.append(xText.createTextCursorByRange(xtr_p))
    del xtr_p

    return xTextRanges

#########################################################################################################
#########################################################################################################
###                                       FONCTIONS D'INTERFACE
#########################################################################################################
#########################################################################################################

###################################################################################
# Remet un paragraphe dans son style d'origine en espaçant les mots
###################################################################################
def colorier_defaut(paragraphe, cursor, style, choix):
    # placer le curseur au début de la zone de traitement
    cursor.collapseToStart()
    cursor2 = cursor.getText().createTextCursorByRange(cursor)

    # suppressions et remplacements de caractères perturbateurs
    paragraphe = nettoyeur_caracteres(paragraphe)

    # code le coloriage du paragraphe
    curs = formaterTexte(paragraphe, cursor, styles_phonemes[style], choix)

    # supprimer les espaces dupliqués
    if (choix == 'defaut'):
        # replacer le curseur au début de la zone de traitement
        curs = cursor2

        i = 0
        while i < len(paragraphe):
            j = i
            if (paragraphe[i] == ' '):
                k = 0
                while (i < len(paragraphe)) and (paragraphe[i] == ' '):
                    i += 1
                    k += 1
                curs = deplacerADroite(paragraphe[j:j+1], curs)
                if k > 1:
                    # il y a plusieurs espaces à remplacer par un seul
                    ncurs = curs.getText().createTextCursorByRange(curs)
                    ncurs.goRight(k-1, True)
                    ncurs.setString("")
                    del ncurs
            else:
                while (i < len(paragraphe)) and (paragraphe[i] != ' '):
                    i += 1
                curs = deplacerADroite(paragraphe[j:i], curs)
    del cursor2

###################################################################################
# Change le style des majuscules de début de phrase et de la ponctuation de fin de phrase
###################################################################################
def colorier_phrase(texte, cursor, style):
    # caractères de ponctuation qui marquent une fin de phrase
    ponct_fin_phrase = u('.!?…')

    # placer le curseur au début de la zone de traitement
    cursor.collapseToStart()

    # suppressions et remplacements de caractères perturbateurs
    utexte = u(texte) # codage unicode
    paragraphe = nettoyeur_caracteres(utexte).replace('-', ' ')

    # code le coloriage du paragraphe
    curs = cursor
    i = 0
    while i < len(paragraphe):
        j = i
        # parcours jusqu'à la prochaine majuscule ou une marque de ponctuation de fin de phrase
        while (i < len(paragraphe)) and (not (paragraphe[i].isupper() or (ponct_fin_phrase.find(paragraphe[i]) >= 0))):
            i += 1
        curs = deplacerADroite(paragraphe[j:i], curs)

        if paragraphe[i].isupper():
            j = i
            # on a trouvé une majuscule
            while (i < len(paragraphe)) and (not paragraphe[i].isspace()):
                i += 1
            if paragraphe[j:i].istitle():
                # Mot qui commence par une majuscule
                curs = formaterTexte(paragraphe[j], curs, styles_phonemes[style], 'Majuscule')
                j += 1
                i = j

            # parcours jusqu'à une marque de ponctuation de fin de phrase
            while (i < len(paragraphe)) and (ponct_fin_phrase.find(paragraphe[i]) < 0):
                i += 1
            curs = deplacerADroite(paragraphe[j:i], curs)

        if paragraphe[i] in ponct_fin_phrase:
            j = i
            while (i < len(paragraphe)) and (paragraphe[i] in ponct_fin_phrase):
                i += 1
            curs = formaterTexte(paragraphe[j:i], curs, styles_phonemes[style], 'Ponctuation')

###################################################################################
# Conversion d'un paragraphe en mettant ses phonèmes en couleur
###################################################################################
def colorier_phonemes_style(xDocument, paragraphe, cursor, style):
    # chargement du dictionnaire de décodage
    loadLCDict(getLirecouleurDictionary())

    # récupération de l'information sur le marquage des lettres muettes par des points
    point_lmuette = handleMaskPoint()

    # récup du masque des phonèmes à afficher
    selecteurphonemes = handleMaskPhonems()

    lMots = extraitMots(cursor)
    for curMot in lMots:
        # suppressions et remplacements de caractères perturbateurs
        paragraphe = nettoyeur_caracteres(curMot.getString())

        # traite le paragraphe en phonèmes
        pp = generer_paragraphe_phonemes(paragraphe)

        # code le coloriage du paragraphe
        curs = curMot
        curs.collapseToStart()
        for umot in pp:
            if isinstance(umot, list):
                # recodage du mot en couleurs
                curs = code_phonemes(xDocument, umot, style, curs, selecteurphonemes, point_lmuette)
            else:
                # passage de la portion de texte non traitée (ponctuation, espaces...)
                curs = deplacerADroite(umot, curs)

        # ménage
        del pp
    del lMots

###################################################################################
# Conversion d'un paragraphe en mettant les lettres muettes en évidence
###################################################################################
def colorier_lettres_muettes(xDocument, paragraphe, cursor, style):
    # chargement du dictionnaire de décodage
    loadLCDict(getLirecouleurDictionary())

    # récupération de l'information sur le marquage des lettres muettes par des points
    point_lmuette = handleMaskPoint()

    # récup du masque des phonèmes à afficher : uniquement les lettres muettes
    selecteurphonemes = {'#':1, 'verb_3p':1}

    lMots = extraitMots(cursor)
    for curMot in lMots:
        # suppressions et remplacements de caractères perturbateurs
        paragraphe = nettoyeur_caracteres(curMot.getString())

        # traite le paragraphe en phonèmes
        pp = generer_paragraphe_phonemes(paragraphe)

        # code le coloriage du paragraphe
        curs = curMot
        curs.collapseToStart()
        for umot in pp:
            if isinstance(umot, list):
                # recodage du mot en couleurs
                curs = code_phonemes(xDocument, umot, style, curs, selecteurphonemes, point_lmuette)
            else:
                # passage de la portion de texte non traitée (ponctuation, espaces...)
                curs = deplacerADroite(umot, curs)

        # ménage
        del pp
    del lMots

###################################################################################
# Marque les liaisons dans un paragraphe
###################################################################################
def colorier_liaisons(texte, cursor, style, forcer=False):
    # segmente le texte en portions mots / non mots
    pp = segmenteParagraphe(cursor)
    
    # code le coloriage du paragraphe
    l_pp = len(pp)
    if l_pp < 2:
        return

    xText = pp[0].getText()
    mot_prec = u(pp[0].getString())
    mot_prec = re.sub(u('[\'´’]'), '@', mot_prec.lower())
    umot = u(pp[1].getString())
    umot = re.sub(u('[\'´’]'), '@', umot.lower())
    mot_suiv = ""
    for i_mot in range(1,l_pp-1):
        mot_suiv = u(pp[i_mot+1].getString())
        mot_suiv = re.sub(u('[\'´’]'), '@', mot_suiv.lower())
        format_liaison = False

        if len(umot.strip()) == 0:
            if forcer or teste_liaison(mot_prec, mot_suiv):
                # formatage de la liaison
                curs = pp[i_mot]
                curs.collapseToStart()
                curs = formaterTexte(umot, curs, styles_phonemes[style], 'liaison')
                format_liaison = True
                
                # formater la dernière lettre du mot précédent comme lettre non muette
                cur_p = xText.createTextCursorByRange(pp[i_mot-1])
                cur_p.collapseToEnd()
                cur_p.goLeft(1, True)
                if cur_p.getPropertyValue("CharStyleName") == "phon_muet":
                    try:
                        cur_p.setPropertyToDefault("CharStyleName")
                    except:
                        pass
                del cur_p

        if not format_liaison:
            # mot : déplacement à droite
            curs = xText.createTextCursorByRange(pp[i_mot])
            curs = deplacerADroite(umot, curs)
            del curs

        mot_prec = umot
        umot = mot_suiv
    del pp

###################################################################################
# Conversion d'un paragraphe en mettant ses syllabes en évidence
###################################################################################
def colorier_syllabes_style(xDocument, paragraphe, cursor, style, nb_altern):
    # chargement du dictionnaire de décodage
    loadLCDict(getLirecouleurDictionary())

    # récupération de l'information sur le choix entre syllabes orales ou syllabes écrites
    choix_syllo = handleMaskSyllo()

    # placer le curseur au début de la zone de traitement
    cursor.collapseToStart()

    # suppressions et remplacements de caractères perturbateurs
    paragraphe = nettoyeur_caracteres(paragraphe)

    # traite le paragraphe en phonèmes
    pp = generer_paragraphe_phonemes(paragraphe)

    # recompose les syllabes
    ps = generer_paragraphe_syllabes(pp, choix_syllo)

    # code le coloriage du paragraphe
    curs = cursor
    isyl = 0
    for i in range(len(ps)):
        try:
            if isinstance(ps[i], list):
                # recodage du mot en couleurs
                curs, isyl = code_syllabes(xDocument, ps[i], isyl, style, curs, nb_altern)
            else:
                # passage de la portion de texte non traitée (ponctuation, espaces...)
                curs = deplacerADroite(ps[i], curs)
        except:
            # passage de la portion de texte non traitée (ponctuation, espaces...)
            curs = deplacerADroite(ps[i], curs)

    # ménage
    del ps
    del pp

###################################################################################
# Colorie les lettres B, D, P, Q pour éviter les confusions
###################################################################################
def colorier_bdpq(paragraphe, cursor, style):
    # placer le curseur au début de la zone de traitement
    cursor.collapseToStart()

    # suppression des \r qui engendrent des décalages de codage sous W*
    paragraphe = paragraphe.replace('\r', '')

    # code le coloriage du paragraphe
    ensemble_confus = ['b','d','p','q']
    curs = cursor
    i = 0
    while i < len(paragraphe):
        j = i
        if paragraphe[i] in ensemble_confus:
            while (i < len(paragraphe)) and (paragraphe[i] == paragraphe[j]):
                i += 1
            curs = formaterTexte(paragraphe[j:i], curs, styles_phonemes[style], 'lettre_'+paragraphe[j])
        else:
            while (i < len(paragraphe)) and not(paragraphe[i] in ensemble_confus):
                i += 1
            curs = deplacerADroite(paragraphe[j:i], curs)

###################################################################################
# Colorie les consonnes et les voyelles
###################################################################################
def colorier_consonnes_voyelles(paragraphe, cursor, style):
    # placer le curseur au début de la zone de traitement
    cursor.collapseToStart()

    # suppression des \r qui engendrent des décalages de codage sous W*
    paragraphe = paragraphe.replace('\r', '')

    # code le coloriage du paragraphe
    e_consonnes = []
    for lettre in ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']:
        e_consonnes.append(lettre)
        e_consonnes.append(lettre.upper())
    e_voyelles = []
    for lettre in ['a','e','i','o','u','y',u('é'),u('è'),u('ë'),u('ê'),u('à'),u('â'),u('ä'),u('î'),u('î'),u('ù'),u('û'),u('ö'),u('ô')]:
        e_voyelles.append(lettre)
        e_voyelles.append(lettre.upper())

    curs = cursor
    i = 0
    while i < len(paragraphe):
        j = i
        if paragraphe[i] in e_consonnes:
            while (i < len(paragraphe)) and (paragraphe[i] in e_consonnes):
                i += 1
            curs = formaterTexte(paragraphe[j:i], curs, styles_phonemes[style], 'consonne')
        elif paragraphe[i] in e_voyelles:
            while (i < len(paragraphe)) and (paragraphe[i] in e_voyelles):
                i += 1
            curs = formaterTexte(paragraphe[j:i], curs, styles_phonemes[style], 'voyelle')
        else:
            while (i < len(paragraphe)) and not(paragraphe[i] in e_consonnes) and not(paragraphe[i] in e_voyelles):
                i += 1
            curs = deplacerADroite(paragraphe[j:i], curs)

###################################################################################
# Suppression des arcs de marquage des syllabes pur le paragraphe sélectionné
###################################################################################
def supprimer_arcs_syllabes(xDocument, texte, cursor):
    if xDocument.supportsService("com.sun.star.drawing.DrawingDocument"):
        oDrawDocCtrl = xDocument.getCurrentController()
        oDrawPage = oDrawDocCtrl.getCurrentPage()
    else:
        oDrawPage = xDocument.DrawPage

    ultexte = pretraitement_texte(texte)
    mots = ['__'+x+'__' for x in ultexte.split()] # extraire des étiquettes des mots"

    shapesup=[]
    nNumShapes = oDrawPage.getCount()
    for x in range (nNumShapes): # toutes les formes de la page
        oShape = oDrawPage.getByIndex(x)
        if oShape.Title in mots:
            shapesup.append(oShape)

    for oShape in shapesup:
        oDrawPage.remove(oShape)
    del shapesup

###################################################################################
# Suppression des points sous les lettres muettes pour la page en cours
###################################################################################
def supprimer_point_l_muettes(xDocument):
    oDrawPage = xDocument.DrawPage

    shapesup=[]
    nNumShapes = oDrawPage.getCount()
    for x in range (nNumShapes): # toutes les formes de la page
        oShape = oDrawPage.getByIndex(x)
        if oShape.Title == '__l_muette__':
            shapesup.append(oShape)

    for oShape in shapesup:
        oDrawPage.remove(oShape)
    del shapesup

#########################################################################################################
#########################################################################################################
#
#    À partir de là, le code ne fait que déclarer les points d'entrées dans l'extension.
#    Pour chaque type de traitement, on a successivement :
#        - une classe, nécessaire comme point d'entrée dans l'extension
#        - une fonction, nécessaire comme point d'entrée sous forme de macro simple
#        - la fonction qui extrait le texte et lance le traitement
#
#                                    @@@@@@@@@@@@@@@@@@@@@@
#
#########################################################################################################
#########################################################################################################

###################################################################################
# Élimine tout style de caractère
###################################################################################
class StyleDefaut(unohelper.Base, XJobExecutor):
    """Applique le style par défaut à la sélection"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_defaut__(desktop.getCurrentComponent())

def lirecouleur_defaut( args=None ):
    """Applique le style par défaut à la sélection"""
    __lirecouleur_defaut__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_defaut__(xDocument, choix='defaut'):
    __arret_dynsylldys__(xDocument)

    """Applique le style par défaut à la sélection"""
    try:
        xTextRange = getXTextRange(xDocument, mode=0)
        if xTextRange == None:
            return False
        for xtr in xTextRange:
            theString = xtr.getString()

            colorier_defaut(theString, xtr, 'perso', choix)
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Recode le texte sélectionné en noir
###################################################################################
class StyleNoir(unohelper.Base, XJobExecutor):
    """Recode le texte sélectionné en noir"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_defaut__(desktop.getCurrentComponent(), 'noir')

def lirecouleur_noir( args=None ):
    """Recode le texte sélectionné en noir"""
    __lirecouleur_defaut__(XSCRIPTCONTEXT.getDocument(), 'noir')

###################################################################################
# Espace les mots de la sélection en dupliquant les espaces
###################################################################################
class StyleEspace(unohelper.Base, XJobExecutor):
    """Espace les mots de la sélection"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_espace__(desktop.getCurrentComponent())

def lirecouleur_espace( args=None ):
    """Espace les mots de la sélection"""
    __lirecouleur_espace__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_espace__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Espace les mots de la sélection"""
    try:
        xTextRange = getXTextRange(xDocument, mode=0)
        if xTextRange == None:
            return False

        # lecture du nombre d'espaces pour remplacer un espace standard
        nb_sub_espaces = handleMaskSubspaces()
        sub_espaces = ''.join([' ' for i in range(nb_sub_espaces)])

        for xtr in xTextRange:
            paragraphe = xtr.getString()

            # placer le curseur au début de la zone de traitement
            xtr.collapseToStart()
            curs = xtr

            # suppressions et remplacements de caractères perturbateurs
            paragraphe = nettoyeur_caracteres(paragraphe)

            # code la duplication des espaces
            i = 0
            while i < len(paragraphe):
                j = i
                if (paragraphe[i] == ' '):
                    k = 0
                    while (i < len(paragraphe)) and (paragraphe[i] == ' '):
                        i += 1
                        k += 1

                    if k != nb_sub_espaces:
                        # il y n'y a pas le bon nombre d'espaces
                        ncurs = curs.getText().createTextCursorByRange(curs)
                        ncurs.goRight(k, True)
                        ncurs.setString(sub_espaces)
                        ncurs.collapseToEnd()
                        del curs
                        curs = ncurs
                    else:
                        curs.goRight(k, False)
                else:
                    while (i < len(paragraphe)) and (paragraphe[i] != ' '):
                        i += 1
                    curs = deplacerADroite(paragraphe[j:i], curs)
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Espace les mots de la sélection en dupliquant les espaces
###################################################################################
class StyleSepareMots(unohelper.Base, XJobExecutor):
    """Sépare les mots de la sélection en coloriant les espaces"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_separe_mots__(desktop.getCurrentComponent())

def lirecouleur_separe_mots( args=None ):
    """Sépare les mots de la sélection en coloriant les espaces"""
    __lirecouleur_separe_mots__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_separe_mots__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Sépare les mots de la sélection en coloriant les espaces"""
    xSelectionSupplier = xDocument.getCurrentController()
    xIndexAccess = xSelectionSupplier.getSelection()
    xTextRange = xIndexAccess.getByIndex(0)
    if xTextRange is None or len(xTextRange.getString()) == 0:
        return

    # Importer les styles de coloriage de texte
    importStylesLireCouleur(xDocument)
    stylEspace = styles_phonemes['perso']['espace']

    xText = xTextRange.getText()
    xWordCursor = xText.createTextCursorByRange(xTextRange)
    if not xWordCursor.isEndOfWord():
        xWordCursor.gotoEndOfWord(False)
                
    while xText.compareRegionEnds(xWordCursor, xTextRange) >= 0:
        # mot par mot
        if not xWordCursor.gotoNextWord(True):
            break
        setStyle(stylEspace, xWordCursor)

        xWordCursor.gotoEndOfWord(False)

    return True

###################################################################################
# Espace les mots de la sélection en dupliquant les espaces
###################################################################################
class StyleCouleurMots(unohelper.Base, XJobExecutor):
    """Colorie les mots en alternant les couleurs (comme syll_dys)"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_couleur_mots__(desktop.getCurrentComponent())

def lirecouleur_couleur_mots( args=None ):
    """Colorie les mots en alternant les couleurs (comme syll_dys)"""
    __lirecouleur_couleur_mots__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_couleur_mots__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Colorie les mots en alternant les couleurs (comme syll_dys)"""
    xSelectionSupplier = xDocument.getCurrentController()
    xIndexAccess = xSelectionSupplier.getSelection()
    xTextRange = xIndexAccess.getByIndex(0)
    if xTextRange is None or len(xTextRange.getString()) == 0:
        return

    # Importer les styles de coloriage de texte
    importStylesLireCouleur(xDocument)

    # récup de la période d'alternance des couleurs
    nb_altern = handleMaskAlternate()

    xText = xTextRange.getText()
    xWordCursor = xText.createTextCursorByRange(xTextRange)
    if not xWordCursor.isStartOfWord():
        xWordCursor.gotoStartOfWord(False)
    xWordCursor.collapseToStart();
    
    imot = 0
    while xText.compareRegionEnds(xWordCursor, xTextRange) >= 0:
        # mot par mot
        xWordCursor.gotoEndOfWord(True)
        setStyle(styles_syllabes['dys'][str(imot+1)], xWordCursor)

        imot += 1
        imot = imot%nb_altern

        # mot suivant
        if not xWordCursor.gotoNextWord(False):
            break

    return True

###################################################################################
# Espace les lignes de la sélection
###################################################################################
class StylePara(unohelper.Base, XJobExecutor):
    """Espace les lignes de la sélection"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_espace_lignes__(desktop.getCurrentComponent())

def lirecouleur_espace_lignes( args=None ):
    """Espace les lignes de la sélection"""
    __lirecouleur_espace_lignes__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_espace_lignes__(xDocument):
    __arret_dynsylldys__(xDocument)

    try:
        xTextRange = getXTextRange(xDocument, mode=0)
        if xTextRange == None:
            return False
        
        for xtr in xTextRange:
            args = xtr.getPropertyValue('ParaLineSpacing')
            args.Height += 10
            xtr.setPropertyValue('ParaLineSpacing', args)
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Espace les lignes et les mots de la sélection
###################################################################################
class StyleLarge(unohelper.Base, XJobExecutor):
    """Espace les lignes et les mots de la sélection"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_large__(desktop.getCurrentComponent())

def lirecouleur_large( args=None ):
    """Espace les lignes et les mots de la sélection"""
    __lirecouleur_large__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_large__(xDocument):
    __arret_dynsylldys__(xDocument)

    # espacement des mots
    __lirecouleur_espace__(xDocument)

    try:
        xTextRange = getXTextRange(xDocument, mode=0)
        if xTextRange == None:
            return False
        
        for xtr in xTextRange:
            # double interligne
            args = xtr.getPropertyValue('ParaLineSpacing')
            args.Height = 200
            xtr.setPropertyValue('ParaLineSpacing', args)

            # espacement des caractères normal
            xtr.setPropertyValue('CharKerning', 100)

            # taille de caractères : 16 points minimum
            args = xtr.getPropertyValue('CharHeight')
            if (args < 16.0):
                xtr.setPropertyValue('CharHeight', 16.0)
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Espace les lignes de la sélection ainsi que les caractères
###################################################################################
class StyleExtraLarge(unohelper.Base, XJobExecutor):
    """Espace les lignes de la sélection ainsi que les caractères"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_extra_large__(desktop.getCurrentComponent())

def lirecouleur_extra_large( args=None ):
    """Espace les lignes de la sélection ainsi que les caractères"""
    __lirecouleur_extra_large__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_extra_large__(xDocument):
    __arret_dynsylldys__(xDocument)

    # espacement des mots
    __lirecouleur_large__(xDocument)

    try:
        xTextRange = getXTextRange(xDocument, mode=0)
        if xTextRange == None:
            return False
        
        for xtr in xTextRange:
            # espacement des caractères
            args = xtr.getPropertyValue('CharKerning')
            if (args < 200):
                xtr.setPropertyValue('CharKerning', 200)

        del xTextRange
    except:
        return False
    return True

###################################################################################
# Marque les phonèmes sous forme de couleurs en fonction des styles du document
###################################################################################
class StylePhonemes(unohelper.Base, XJobExecutor):
    """Colorie les phonèmes en couleurs arc en ciel"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_phonemes__(desktop.getCurrentComponent())

def lirecouleur_phonemes( args=None ):
    """Colorie les phonèmes en couleurs arc en ciel"""
    __lirecouleur_phonemes__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_phonemes__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Colorie les phonèmes en couleurs arc en ciel"""

    __lirecouleur_defaut__(xDocument, 'noir')

    xTextRange = getXTextRange(xDocument, mode=3)
    if xTextRange == None:
        return False

    try:
        for xtr in xTextRange:
            theString = xtr.getString()
            colorier_phonemes_style(xDocument, theString, xtr, 'perso')
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Marque les phonèmes sous forme de couleurs en fonction des styles du document
###################################################################################
class StylePhonemesComplexes(unohelper.Base, XJobExecutor):
    """Colorie les phonèmes complexes"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_phonemes_complexes__(desktop.getCurrentComponent())

def lirecouleur_phonemes_complexes( args=None ):
    """Colorie les phonèmes complexes"""
    __lirecouleur_phonemes_complexes__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_phonemes_complexes__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Colorie les phonèmes complexes"""

    xTextRange = getXTextRange(xDocument, mode=3)
    if xTextRange == None:
        return False

    try:
        for xtr in xTextRange:
            theString = xtr.getString()

            colorier_phonemes_style(xDocument, theString, xtr, 'complexes')
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Marque les syllabes sous forme de ponts.
###################################################################################
class StyleSyllabes(unohelper.Base, XJobExecutor):
    """Mise en évidence des syllabes soulignées"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_syllabes__(desktop.getCurrentComponent(),  "souligne")

def lirecouleur_syllabes( args=None ):
    """Mise en évidence des syllabes soulignées"""
    __lirecouleur_syllabes__(XSCRIPTCONTEXT.getDocument(), 'souligne')

###################################################################################
# Marque les syllabes en alternant les couleurs
###################################################################################
class StyleSyllDys(unohelper.Base, XJobExecutor):
    """Mise en évidence des syllabes -- dyslexiques"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_syllabes__(desktop.getCurrentComponent(), "dys")
        __lirecouleur_dynsylldys__(desktop.getCurrentComponent())

def lirecouleur_sylldys( args=None ):
    """Mise en évidence des syllabes -- dyslexiques"""
    xDocument = XSCRIPTCONTEXT.getDocument()

    __lirecouleur_syllabes__(xDocument, 'dys')
    __lirecouleur_dynsylldys__(xDocument)

def __lirecouleur_syllabes__(xDocument, style = 'souligne'):
    __arret_dynsylldys__(xDocument)

    """Mise en évidence des syllabes soulignées"""
    try:
        xTextRange = getXTextRange(xDocument, mode=1)
        if xTextRange == None:
            return False

        # Importer les styles de coloriage de texte
        importStylesLireCouleur(xDocument)

        # récup de la période d'alternance des couleurs
        nb_altern = handleMaskAlternate()

        for xtr in xTextRange:
            theString = xtr.getString()
            colorier_syllabes_style(xDocument, theString, xtr, style, nb_altern)
        del xTextRange
    except:
        return False
    return __lirecouleur_l_muettes__(xDocument)

###################################################################################
# Supprime les arcs sous les syllabes dans le texte sélectionné.
###################################################################################
class SupprimerSyllabes(unohelper.Base, XJobExecutor):
    """Supprime les formes ajoutées sur la page pour marquer les syllabes"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_suppr_syllabes__(desktop.getCurrentComponent())

def lirecouleur_suppr_syllabes( args=None ):
    """Supprime les cuvettes qui marquent les liaisons"""
    __lirecouleur_suppr_syllabes__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_suppr_syllabes__(xDocument):
    __arret_dynsylldys__(xDocument)

    try:
        xTextRange = getXTextRange(xDocument, mode=3)
        if xTextRange == None:
            return False
        for xtr in xTextRange:
            theString = xtr.getString()
            supprimer_arcs_syllabes(xDocument, theString, xtr)
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Ne marque que les lettres muettes dans le texte sélectionné.
###################################################################################
class StyleLMuettes(unohelper.Base, XJobExecutor):
    """Met uniquement en évidence les lettres muettes"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_l_muettes__(desktop.getCurrentComponent())

def lirecouleur_l_muettes( args=None ):
    """Met uniquement en évidence les lettres muettes"""
    __lirecouleur_l_muettes__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_l_muettes__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Met uniquement en évidence les lettres muettes"""
    try:
        xTextRange = getXTextRange(xDocument, mode=1)
        if xTextRange == None:
            return False

        for xtr in xTextRange:
            theString = xtr.getString()
            colorier_lettres_muettes(xDocument, theString, xtr, 'perso')

        del xTextRange
    except:
        return False
    return True

###################################################################################
# Formatte toute la sélection comme phonème muet
###################################################################################
class StylePhonMuet(unohelper.Base, XJobExecutor):
    """Formate la sélection comme phonème muet"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_phon_muet__(desktop.getCurrentComponent())

def lirecouleur_phon_muet( args=None ):
    """Formate la sélection comme phonème muet"""
    __lirecouleur_phon_muet__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_phon_muet__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Met uniquement en évidence les lettres muettes"""
    try:
        # Importer les styles de coloriage de texte
        importStylesLireCouleur(xDocument)

        #the writer controller impl supports the css.view.XSelectionSupplier interface
        xSelectionSupplier = xDocument.getCurrentController()
        xIndexAccess = xSelectionSupplier.getSelection()
        xTextRange = xIndexAccess.getByIndex(0)
    
        if xTextRange == None or len(xTextRange.getString()) == 0:
            return False

        # récupération de l'information sur le marquage des lettres muettes par des points
        point_lmuette = handleMaskPoint()

        xtr = xTextRange.getText().createTextCursorByRange(xTextRange)
        theString = xtr.getString()
        xtr.collapseToStart()
        xtr = formaterTexte(theString, xtr, styles_phonemes['perso'], '#')
        if point_lmuette and xDocument.supportsService("com.sun.star.text.TextDocument"):
            xtr.goLeft(len(theString), False)
            xtr = marquePoint(xDocument, theString, xtr)

        del xtr
    except:
        return False
    return True

###################################################################################
# Supprime d'éventuels points sous les lettres muettes.
###################################################################################
class SupprimerPoints(unohelper.Base, XJobExecutor):
    """Supprime les formes ajoutées sur la page pour marquer les lettres muettes"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_suppr_points__(desktop.getCurrentComponent())

def lirecouleur_suppr_points( args=None ):
    """Supprime les points ajoutés sous les lettres muettes"""
    __lirecouleur_suppr_points__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_suppr_points__(xDocument):
    __arret_dynsylldys__(xDocument)

    try:
        supprimer_point_l_muettes(xDocument)
    except:
        return False
    return True

###################################################################################
# Colorie les majuscules de début de phrase et les point de fin de phrase.
###################################################################################
class StylePhrase(unohelper.Base, XJobExecutor):
    """Marque les majuscules de début de phrase et les points de fin de phrase."""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_phrase__(desktop.getCurrentComponent())

def lirecouleur_phrase( args=None ):
    """Marque les majuscules de début de phrase et les points de fin de phrase."""
    __lirecouleur_phrase__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_phrase__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Marque les majuscules de début de phrase et les points de fin de phrase."""
    try:
        xTextRange = getXTextRange(xDocument, mode=2)
        if xTextRange == None:
            return False
        for xtr in xTextRange:
            theString = xtr.getString()
            colorier_phrase(theString, xtr, 'perso')
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Marque les liaisons dans le texte sélectionné.
###################################################################################
class StyleLiaisons(unohelper.Base, XJobExecutor):
    """Mise en évidence des liaisons"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_liaisons__(desktop.getCurrentComponent())

def lirecouleur_liaisons( args=None ):
    """Mise en évidence des liaisons"""
    __lirecouleur_liaisons__(XSCRIPTCONTEXT.getDocument())

class StyleLiaisonsForcees(unohelper.Base, XJobExecutor):
    """Forcer la mise en évidence des liaisons (mode enseignant)"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_liaisons__(desktop.getCurrentComponent(), forcer=True)

def lirecouleur_liaisons_forcees( args=None ):
    """Mise en évidence des liaisons"""
    __lirecouleur_liaisons__(XSCRIPTCONTEXT.getDocument(), forcer=True)

def __lirecouleur_liaisons__(xDocument, forcer=False):
    __arret_dynsylldys__(xDocument)

    """Mise en évidence des liaisons"""
    xTextRange = getXTextRange(xDocument, mode=1)
    if xTextRange == None:
        return False
    for xtr in xTextRange:
        try:
            theString = xtr.getString()
            colorier_liaisons(theString, xtr, 'perso', forcer)
        except:
            pass
    del xTextRange
    return True

###################################################################################
# Colorie les lettres b, d, p, q pour éviter des confusions.
###################################################################################
class ConfusionBDPQ(unohelper.Base, XJobExecutor):
    """Colorie les lettre B, D, P, Q pour éviter les confusions"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_bdpq__(desktop.getCurrentComponent())

def lirecouleur_bdpq( args=None ):
    """Colorie les lettres B, D, P, Q pour éviter les confusions"""
    __lirecouleur_bdpq__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_bdpq__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Colorie les lettres B, D, P, Q pour éviter les confusions"""
    try:
        xTextRange = getXTextRange(xDocument, mode=1)
        if xTextRange == None:
            return False
        for xtr in xTextRange:
            theString = xtr.getString()

            colorier_bdpq(theString, xtr, 'perso')
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Colorie les consonnes et les voyelles.
###################################################################################
class ConsonneVoyelle(unohelper.Base, XJobExecutor):
    """Colorie les consonnes et les voyelles"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_consonne_voyelle__(desktop.getCurrentComponent())

def lirecouleur_consonne_voyelle( args=None ):
    """Colorie les consonnes et les voyelles"""
    __lirecouleur_consonne_voyelle__(XSCRIPTCONTEXT.getDocument())

def __lirecouleur_consonne_voyelle__(xDocument):
    __arret_dynsylldys__(xDocument)

    """Colorie les consonnes et les voyelles"""
    try:
        xTextRange = getXTextRange(xDocument, mode=1)
        if xTextRange == None:
            return False
        for xtr in xTextRange:
            theString = xtr.getString()

            colorier_consonnes_voyelles(theString, xtr, 'complexes')
        del xTextRange
    except:
        return False
    return True

###################################################################################
# Colorie les lignes avec une alternance de couleurs.
###################################################################################
class StyleLignesAlternees(unohelper.Base, XJobExecutor):
    """Alterne les styles pour les lignes du document"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        __lirecouleur_lignes__(desktop.getCurrentComponent())

def __lirecouleur_lignes__(xDocument):
    __arret_dynsylldys__(xDocument)

    #the writer controller impl supports the css.view.XSelectionSupplier interface
    xSelectionSupplier = xDocument.getCurrentController()
    xIndexAccess = xSelectionSupplier.getSelection()
    xTextRange = xIndexAccess.getByIndex(0)
    if xTextRange is None or len(xTextRange.getString()) == 0:
        return

    # Importer les styles de coloriage de texte
    importStylesLireCouleur(xDocument)

    # récup de la période d'alternance des couleurs
    nb_altern = handleMaskAlternate()

    xText = xTextRange.getText()
    xtr = xText.createTextCursorByRange(xTextRange)
    xtr_p = xSelectionSupplier.getViewCursor()
    xtr_p.gotoRange(xTextRange, False)
    xtr_p.gotoStartOfLine(False)
    stylignes = [dict([['CharStyleName',styles_lignes+str(i)]]) for i in range(1,nb_altern+1)]
    nligne = 0

    while xText.compareRegionEnds(xtr_p, xTextRange) >= 0:
        # paragraphe par paragraphe
        xtr.gotoEndOfParagraph(False)
        while xText.compareRegionEnds(xtr_p, xtr) >= 0:
            # ligne par ligne
            xtr_p.gotoEndOfLine(True)
            setStyle(stylignes[nligne], xtr_p)
            ll = u(xtr_p.getString())

            if len(ll.encode('UTF-8')) > 0:
                nligne = (nligne + 1) % nb_altern

            xtr_p.collapseToStart()
            if not xtr_p.goDown(1, False):
                del xtr
                return True
        if not xtr.gotoNextParagraph(False):
            del xtr
            return True
    return True

def lirecouleur_lignes( args=None ):
    """Alterne les styles pour les lignes du document -- dyslexiques"""
    __lirecouleur_lignes__(XSCRIPTCONTEXT.getDocument())

"""
    Création d'un nouveau document LireCouleur
"""
class NewLireCouleurDocument(unohelper.Base, XJobExecutor):
    """Création d'un nouveau document LireCouleur"""
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        __new_lirecouleur_document__(self.ctx)

def new_lirecouleur_document(args=None):
    __new_lirecouleur_document__(uno.getComponentContext())

def __new_lirecouleur_document__(ctx):
    __arret_dynsylldys__(xDocument)

    url = getLirecouleurTemplateURL()
    try:
        desktop = createUnoService('com.sun.star.frame.Desktop', ctx)
        if url.endswith('.odt'):
            ppp = createUnoStruct("com.sun.star.beans.PropertyValue")
            ppp.Name = "AsTemplate" # le fichier va servir de modèle
            ppp.Value = True
            monDocument = desktop.loadComponentFromURL(url, "_blank", 0, (ppp,))
        else:
            monDocument = desktop.loadComponentFromURL(url, "_blank", 0, ())
        return
    except:
        pass

    try:
        monDocument = desktop.loadComponentFromURL('private:factory/swriter', "_blank", 0, ())
    except:
        pass

###################################################################################
# Lit le passage courant sous le curseur
###################################################################################
class Lire():
    """Lit la syllabe courante sous le curseur"""
    def __init__(self, xDocument, applic, nb_altern, choix_syllo):
        self.xDocument = xDocument
        self.xController = self.xDocument.getCurrentController()
        self.curseurMot = None
        self.ps = None
        self.isyl = 0
        self.jsyl = 0
        self.nb_altern = nb_altern
        self.choix_syllo = choix_syllo
        self.applic = applic
        
    def debutMot(self, xtr):
        if not self.curseurMot is None:
            # remise en place de la couleur d'arrière plan de la syllabe
            self.curseurMot.setPropertyToDefault('CharBackColor')
            del self.curseurMot
            del self.ps
        
        self.curseurMot = xtr.getText().createTextCursorByRange(xtr)
        self.curseurMot.collapseToStart()
        xtr.gotoEndOfWord(True)
        mot = xtr.getString()

        # suppressions et remplacements de caractères perturbateurs
        mot = nettoyeur_caracteres(mot)

        # traite le paragraphe en phonèmes
        pp = generer_paragraphe_phonemes(mot)

        # recompose les syllabes
        self.ps = generer_paragraphe_syllabes(pp, self.choix_syllo)[0]
        del pp
        
        # surligner la première syllabe
        self.isyl = 0
        psyl = len(self.ps[self.isyl])

        #ncurs = xtr.getText().createTextCursorByRange(xtr)
        self.curseurMot.goRight(psyl, True)
        self.curseurMot.setPropertyValue('CharBackColor', 0x00ffff00)
        self.xController.getViewCursor().gotoRange(self.curseurMot, False)
        self.xController.getViewCursor().collapseToEnd()
        if self.applic:
            #in order to patch an openoffice bug
            self.xController.getViewCursor().goLeft(1, False)
        colorier_lettres_muettes(self.xDocument, self.ps[self.isyl], self.curseurMot, 'perso')

    def selection(self):
        # récupération du curseur physique
        xTextViewCursor = self.xController.getViewCursor()
        xtr = xTextViewCursor.getText().createTextCursorByRange(xTextViewCursor)

        if xtr.isEndOfWord():
            if not self.curseurMot is None:
                self.curseurMot.setPropertyToDefault('CharBackColor')
                setStyle(styles_syllabes['dys'][str(self.jsyl%self.nb_altern+1)], self.curseurMot)
                colorier_lettres_muettes(self.xDocument, self.ps[self.isyl], self.curseurMot, 'perso')
                self.jsyl += 1
                del self.curseurMot
                del self.ps
                self.curseurMot = None

            # passage au mot suivant
            xtr.gotoNextWord(False)
            xTextViewCursor.gotoRange(xtr, False)
            
        if xtr.isStartOfWord():
            self.debutMot(xtr)
        else:
            if not self.curseurMot is None:
                # passage à la syllabe suivante
                            
                # remise en place de la couleur d'arrière plan de la syllabe
                self.curseurMot.setPropertyToDefault('CharBackColor')
                setStyle(styles_syllabes['dys'][str(self.jsyl%self.nb_altern+1)], self.curseurMot)
                colorier_lettres_muettes(self.xDocument, self.ps[self.isyl], self.curseurMot, 'perso')
                self.curseurMot.collapseToEnd()

                self.isyl += 1
                self.jsyl += 1
                if self.isyl < len(self.ps):
                    psyl = len(self.ps[self.isyl])

                    # surligner la syllabe courante
                    self.curseurMot.goRight(psyl, True)
                    self.curseurMot.setPropertyValue('CharBackColor', 0x00ffff00)
                    xTextViewCursor.gotoRange(self.curseurMot, False)
                    xTextViewCursor.collapseToEnd()
                    if self.applic:
                        #in order to patch an openoffice bug
                        self.xController.getViewCursor().goLeft(1, False)
                    colorier_lettres_muettes(self.xDocument, self.ps[self.isyl], self.curseurMot, 'perso')
                else:
                    xtr.gotoEndOfWord(False)
                    xtr.gotoNextWord(False)
                    del self.curseurMot
                    self.curseurMot = None
                    del self.ps
                    xTextViewCursor.gotoRange(xtr, False)
                    xTextViewCursor.collapseToEnd()
                    if self.applic:
                        #in order to patch an openoffice bug
                        self.xController.getViewCursor().goLeft(1, False)
            else:
                # placement du curseur physique en cours de mot par l'utilisateur : passage au mot suivant
                xtr.gotoNextWord(False)
                xTextViewCursor.gotoRange(xtr, False)
                xTextViewCursor.collapseToEnd()
                if self.applic:
                    #in order to patch an openoffice bug
                    self.xController.getViewCursor().goLeft(1, False)

        del xtr

###################################################################################
# Classe de gestion des déplacements d'une syllabe à l'autre
###################################################################################
class LireCouleurHandler(unohelper.Base, XKeyHandler):
    enabled = True

    def __init__(self, xDocument, applic):
        self.xDocument = xDocument
        self.is_text_doc = self.xDocument.supportsService("com.sun.star.text.TextDocument")

        # Importer les styles de coloriage de texte
        importStylesLireCouleur(xDocument)

        # chargement du dictionnaire de décodage
        loadLCDict(getLirecouleurDictionary())

        # récup de la période d'alternance des couleurs
        nb_altern = handleMaskAlternate()

        # récupération de l'information sur le choix entre syllabes orales ou syllabes écrites
        choix_syllo = handleMaskSyllo()

        self.lit = Lire(self.xDocument, applic, nb_altern, choix_syllo)

    def keyPressed(self, event):
            if not(LireCouleurHandler.enabled and self.is_text_doc):
                return False
            ##if event.Modifiers == MOD2:
            if event.KeyCode == keyRight:
                # ALT + ->
                ##__deplacement__(self.xDocument, __lectureSuivant__)
                self.lit.selection()
                return True
            return False

    def keyReleased(self, event):
        return False
        
    def enable(self, val=True):
        LireCouleurHandler.enabled = val

###################################################################################
# Fonctions appelées pour le coloriage dynamique des syllabes
###################################################################################
def __lirecouleur_dynsylldys__(xDocument):
    """Mise en évidence des syllabes soulignées dynamiquement"""

    oConfigProvider = createUnoService('com.sun.star.configuration.ConfigurationProvider')
    ppp = createUnoStruct("com.sun.star.beans.PropertyValue")
    ppp.Name = "nodepath"
    ppp.Value = "/org.openoffice.Setup/Product"
    xConfig = oConfigProvider.createInstanceWithArguments("com.sun.star.configuration.ConfigurationAccess", (ppp,))
    # le bug à corriger apparaît sur Apache OpenOffice sous Linux (pas Windows) - Mac non testé
    applic = xConfig.getByName("ooName").lower().startswith('openoffice') and not sys.platform.startswith('win')

    try:
        global __memoKeys__
        __arret_dynsylldys__(xDocument)
        
        key = xDocument.RuntimeUID
        __memoKeys__[key] = {'doc':xDocument, 'handler':LireCouleurHandler(xDocument, applic)}

        # enable/disable the key handlers
        __memoKeys__[key]['handler'].enable(True)

        # register the key handlers
        xDocument.getCurrentController().addKeyHandler(__memoKeys__[key]['handler'])
    except:
        pass

def __arret_dynsylldys__(xDocument):
    """Arrêt de la mise en évidence des syllabes soulignées dynamiquement"""
    try:
        global __memoKeys__
        key = xDocument.RuntimeUID
        xDocument.getCurrentController().removeKeyHandler(__memoKeys__[key]['handler'])
        del __memoKeys__[key]['handler']
        __memoKeys__[key]['handler'] = None
        __memoKeys__[key]['doc'] = None
        
        xTextViewCursor = xDocument.getCurrentController().getViewCursor()
        curseur = xTextViewCursor.getText().createTextCursorByRange(xTextViewCursor)
        curseur.gotoStartOfWord(False)
        curseur.gotoEndOfWord(True)
        curseur.setPropertyToDefault('CharBackColor')
        del curseur
    except:
        pass

###################################################################################
# lists the scripts, that shall be visible inside OOo. Can be omitted.
###################################################################################
g_exportedScripts = lirecouleur_defaut, lirecouleur_espace, lirecouleur_phonemes, lirecouleur_syllabes, \
lirecouleur_sylldys, lirecouleur_l_muettes, creerSelectPhonemesDialog, lirecouleur_liaisons, \
lirecouleur_liaisons_forcees, lirecouleur_bdpq, lirecouleur_suppr_syllabes, lirecouleur_lignes, \
lirecouleur_phrase, lirecouleur_suppr_points, lirecouleur_phon_muet, lirecouleur_phonemes_complexes, \
new_lirecouleur_document, gererDictionnaireDialog, lirecouleur_espace_lignes, lirecouleur_consonne_voyelle, \
lirecouleur_large, lirecouleur_extra_large, lirecouleur_noir, lirecouleur_separe_mots, \
lirecouleur_couleur_mots,

# --- faked component, dummy to allow registration with unopkg, no functionality expected
g_ImplementationHelper = unohelper.ImplementationHelper()

g_ImplementationHelper.addImplementation( \
    StyleDefaut,'org.lirecouleur.StyleDefaut', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleNoir,'org.lirecouleur.StyleNoir', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleEspace,'org.lirecouleur.StyleEspace', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StylePhonemes,'org.lirecouleur.StylePhonemes', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleSyllabes,'org.lirecouleur.StyleSyllabes', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleSyllDys,'org.lirecouleur.StyleSyllDys', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleLMuettes,'org.lirecouleur.StyleLMuettes', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleLiaisons,'org.lirecouleur.StyleLiaisons', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleLiaisonsForcees,'org.lirecouleur.StyleLiaisonsForcees', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    ConfusionBDPQ,'org.lirecouleur.ConfusionBDPQ', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    ConsonneVoyelle,'org.lirecouleur.ConsonneVoyelle', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    SelectPhonemes,'org.lirecouleur.SelectPhonemes', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    SupprimerSyllabes,'org.lirecouleur.SupprimerSyllabes', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    SupprimerPoints,'org.lirecouleur.SupprimerPoints', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleLignesAlternees,'org.lirecouleur.StyleLignesAlternees', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StylePhrase,'org.lirecouleur.StylePhrase', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StylePhonMuet,'org.lirecouleur.StylePhonMuet', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StylePhonemesComplexes,'org.lirecouleur.StylePhonemesComplexes', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    NewLireCouleurDocument,'org.lirecouleur.NewLireCouleurDocument', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    GestionnaireDictionaire,'org.lirecouleur.GestionnaireDictionaire', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StylePara,'org.lirecouleur.StylePara', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleLarge,'org.lirecouleur.StyleLarge', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleExtraLarge,'org.lirecouleur.StyleExtraLarge', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleSepareMots,'org.lirecouleur.StyleSepareMots', \
    ('com.sun.star.task.Job',))

g_ImplementationHelper.addImplementation( \
    StyleCouleurMots,'org.lirecouleur.StyleCouleurMots', \
    ('com.sun.star.task.Job',))

