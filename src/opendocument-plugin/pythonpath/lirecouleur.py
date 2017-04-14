#!/usr/bin/env python
# -*- coding: UTF-8 -*-

###################################################################################
# Ensemble de fonctions de décodage de textes en chaînes de phonèmes et
# en syllabes.
#
# @author Marie-Pierre Brungard
# @version 3.5.2
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

import os
TYPE_ENTIER = (int)
try:
    # nécessaire pour Python 3
    from functools import reduce
    TYPE_ENTIER = (int, long)
except:
    pass
import string
import re
import logging
import sys
import codecs

# configuration du niveau de log (DEBUG = le plus bas niveau ; CRITICAL = le plus haut niveau)
#logging.basicConfig(level = logging.INFO, format="%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s : %(message)s")

"""
    Dictionnaire de décodage de mots particuliers
"""
__dico_deco__ = None


"""
    Correspondance entre le code SAMPA et le code LireCouleur
    référence : http://fr.wikipedia.org/wiki/Symboles_SAMPA_fran%C3%A7ais
"""
sampa2lc = {'p':'p', 'b':'b', 't':'t', 'd':'d', 'k':'k', 'g':'g', 'f':'f', 'v':'v',
's':'s', 'z':'z', 'S':'s^', 'Z':'g^', 'j':'j', 'm':'m', 'n':'n', 'J':'g~',
'N':'n~', 'l':'l', 'R':'r', 'w':'wa', 'H':'y', 'i':'i', 'e':'e', 'E':'e^',
'a':'a', 'A':'a', 'o':'o', 'O':'o_ouvert', 'u':'u', 'y':'y', '2':'x^', '9':'x',
'@':'q', 'e~':'e~', 'a~':'a~', 'o~':'o~', '9~':'x~', '#':'#'}

"""
    Constantes LireCouleur
"""
class ConstLireCouleur:
    # différentes configurations de marquage des syllabes
    SYLLABES_LC = 0
    SYLLABES_STD = 1
    SYLLABES_ORALES = 1
    SYLLABES_ECRITES = 0

    # prononciation différente entre l'Europe et le Canada
    MESTESSESLESDESCES = {'':'e_comp','fr':'e_comp','fr_CA':'e^_comp'}

#########################################################################################################
#########################################################################################################
#
#    Cette partie du code est destinée au traitement des informations de configuration de l'application
#
#                                    @@@@@@@@@@@@@@@@@@@@@@
#
#########################################################################################################
#########################################################################################################

######################################################################################
# Sauvegarde du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur
######################################################################################
def saveMaskPhonems(selectphonemes):
    """Sauvegarde du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur"""
    saveAppData('__phon_selector__', selectphonemes)

######################################################################################
# Lecture du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur
######################################################################################
def handleMaskPhonems():
    """Lecture du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur"""

    # construction du sélecteur de phonèmes par défaut : on affiche tout
    liste_phonemes = ['#', 'verb_3p']
    liste_phonemes.extend(syllaphon['v'])
    liste_phonemes.extend(syllaphon['c'])
    liste_phonemes.extend(syllaphon['s'])
    selectphonemes = dict([[x,1] for x in liste_phonemes])
    for k in syllaphon['c']:
        selectphonemes[k] = 0

    for k in ['o_comp','e_comp','e^_comp','a~','e~','x~','o~','x','x^','w','wa', 'w5']:
        selectphonemes[k] = 0

    # read the file content
    adata = readAppData()

    # transfer the configuration data in the resulting dict
    for phon in liste_phonemes:
        try:
            selectphonemes[phon] = adata['__phon_selector__'][phon]
        except:
            pass
    
    # considérer que la sélection des phonèmes 'voyelle' s'étend à 'yod'+'voyelle'
    for phon in ['a', 'a~', 'e', 'e^', 'e_comp', 'e^_comp', 'o', 'o~', 'i', 'e~', 'x', 'x^', 'u']:
        try:
            selectphonemes['j_'+phon] = selectphonemes[phon]
            selectphonemes['w_'+phon] = selectphonemes[phon]
        except:
            pass

    del liste_phonemes
    del adata
    return selectphonemes

######################################################################################
# Sauvegarde du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur
######################################################################################
def saveMaskColors(selectcouleurs):
    """Sauvegarde du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur"""
    saveAppData('__colors__', selectcouleurs)

######################################################################################
# Sauvegarde de l'info de marquage d'un point sous les lettres muettes
######################################################################################
def saveMaskPoint(selectpoint):
    """Sauvegarde de l'info sur le point sous les lettres muettes dans le fichier .lirecouleur"""
    saveAppData('__point__', selectpoint)

######################################################################################
# Lecture de l'info de marquage d'un point sous les lettres muettes
######################################################################################
def handleMaskPoint():
    """Lecture de l'info sur le point sous les lettres muettes dans le fichier .lirecouleur"""

    # par défaut on ne met pas de point
    point_lmuette = False

    # read the file content
    adata = readAppData()

    # lecture dans la structure du fichier
    try:
        point_lmuette = adata['__point__']
    except:
        pass

    return point_lmuette

######################################################################################
# Sauvegarde de l'info de marquage d'un point sous les lettres muettes
######################################################################################
def saveMaskSyllo(m_syll_1, m_syll_2):
    """Sauvegarde de l'info sur le choix entre syllabes orales ou écrites dans le fichier .lirecouleur"""
    saveAppData('__syllo__', m_syll_1+10*m_syll_2)

######################################################################################
# Lecture de l'info de marquage d'un point sous les lettres muettes
######################################################################################
def handleMaskSyllo():
    """Lecture de l'info sur le choix entre syllabes orales ou écrites dans le fichier .lirecouleur"""

    # par défaut on choisit les syllabes écrites en mode LireCouleur
    choix_syllo = ConstLireCouleur.SYLLABES_LC+10*ConstLireCouleur.SYLLABES_ECRITES

    # read the file content
    adata = readAppData()

    # lecture dans la structure du fichier
    try:
        choix_syllo = adata['__syllo__']
    except:
        pass

    if not isinstance(choix_syllo, TYPE_ENTIER):
        choix_syllo = ConstLireCouleur.SYLLABES_LC+10*ConstLireCouleur.SYLLABES_ECRITES

    return (choix_syllo%10, choix_syllo/10)

######################################################################################
# Lecture de l'info de marquage d'un point sous les lettres muettes
######################################################################################
def handleMaskDynSyllDys():
    """Lecture de l'info sur le choix d'affichage des syllabes dynamiquement ou non dans le fichier .lirecouleur"""

    # par défaut : faux
    choix_dynsylldys = False

    # read the file content
    adata = readAppData()

    # lecture dans la structure du fichier
    try:
        choix_dynsylldys = adata['__dynsylldys__']
    except:
        pass

    return choix_dynsylldys

######################################################################################
# Sauvegarde de l'info de marquage d'un point sous les lettres muettes
######################################################################################
def saveMaskDynSyllDys(selectdsd):
    """Sauvegarde de l'info sur l'affichage dynamique de syllanes dans le fichier .lirecouleur"""
    saveAppData('__dynsylldys__', selectdsd)

######################################################################################
# Lecture de l'info de configuration du pays
######################################################################################
def handleMaskCountry():
    """Lecture de l'info de configuration du pays dans le fichier .lirecouleur"""

    # par défaut on choisit 'fr'
    choix_country = 'fr'

    # read the file content
    adata = readAppData()

    # lecture dans la structure du fichier
    try:
        choix_country = adata['__locale__']
    except:
        pass

    return choix_country

######################################################################################
# Sauvegarde de l'info de configuration du pays
######################################################################################
def saveMaskCountry(loc):
    """Sauvegarde de l'info de configuration du pays dans le fichier .lirecouleur"""
    saveAppData('__locale__', loc)

######################################################################################
# Sauvegarde du nom du fichier modèle
######################################################################################
def saveMaskTemplate(filename):
    """Sauvegarde du nom du fichier modèle dans le fichier .lirecouleur"""
    saveAppData('__template__', filename)

######################################################################################
# Lecture du nom du fichier modèle
######################################################################################
def handleMaskTemplate():
    """Lecture du nom du fichier modèle dans le fichier .lirecouleur"""

    # par défaut on ne met pas de point
    temFilename = ""

    # read the file content
    adata = readAppData()

    # lecture dans la structure du fichier
    try:
        temFilename = adata['__template__']
    except:
        pass

    return temFilename

######################################################################################
# Sauvegarde du nombre de lignes sur lequel doit se faire l'alternance de couleurs
######################################################################################
def saveMaskAlternate(nblignes):
    """Sauvegarde du nombre de lignes sur lequel doit se faire l'alternance de couleurs
    dans le fichier .lirecouleur"""
    saveAppData('__alternate__', nblignes)

######################################################################################
# Lecture du nombre de lignes sur lequel doit se faire l'alternance de couleurs
######################################################################################
def handleMaskAlternate():
    """Lecture du nombre de lignes sur lequel doit se faire l'alternance de couleurs
    dans le fichier .lirecouleur"""

    # par défaut : 2 lignes
    nblignes = 2

    # read the file content
    adata = readAppData()

    # lecture dans la structure du fichier
    try:
        nblignes = adata['__alternate__']
    except:
        pass

    return nblignes

######################################################################################
# Sauvegarde du nombre d'espaces de substitution pour espacer les mots
######################################################################################
def saveMaskSubspaces(nbespaces):
    """Sauvegarde du nombre d'espaces de substitution pour espacer les mots dans le fichier .lirecouleur"""
    saveAppData('__space__', nbespaces)

######################################################################################
# Lecture du nombre d'espaces de substitution pour espacer les mots
######################################################################################
def handleMaskSubspaces():
    """Lecture du nombre d'espaces de substitution pour espacer les mots dans le fichier .lirecouleur"""

    # par défaut : 3 espaces
    nbespaces = 3

    # read the file content
    adata = readAppData()

    # lecture dans la structure du fichier
    try:
        nbespaces = adata['__space__']
    except:
        pass

    return nbespaces

######################################################################################
# Lecture du répertoire maison
######################################################################################
def getHomeDir():
    """Lecture du répertoire maison"""
    appdata = ""
    if 'APPDATA' in os.environ:
        appdata = os.environ.get('APPDATA')+os.sep
    elif 'HOME' in os.environ:
        appdata = os.environ.get('HOME')+os.sep
    return appdata

######################################################################################
# Sauvegarde du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur
######################################################################################
def readAppData():
    """Lecture des informations dans le fichier .lirecouleur"""
    appdata = getHomeDir()+'.lirecouleur'

    # get the configuration data
    adata = {}
    try:
        if os.path.isfile(appdata):
            fappdata = open(appdata)
            line = fappdata.read()
            fappdata.close()

            # eval gives the dict
            adata = eval(line)
    except:
        pass
    return adata

######################################################################################
# Sauvegarde du masque des phonèmes à mettre en évidence dans le fichier .lirecouleur
######################################################################################
def saveAppData(nappdata, dappdata):
    """Sauvegarde des informations dans le fichier .lirecouleur"""
    appdata = getHomeDir()+'.lirecouleur'

    # first read the data
    adata = readAppData()
    try:
        # then introduce the data in the dict
        adata[nappdata] = dappdata

        # and now save the whole dict
        f = open(appdata, 'w')
        f.write(str(adata))
        f.close()
    except:
        pass
    return

######################################################################################
# Classe de gestion du dictionnaire de décodage
######################################################################################
class LCDictionnary(dict):

    def __init__(self, filename=''):
        self.load(filename)

    def load(self, filename):
        self.fileName = filename
        if not os.path.isfile(filename):
            return
        ff = codecs.open(filename, "r", "utf_8_sig", errors="replace")
        for line in ff:
            if line.isspace():
                continue
            line=line.rstrip('\r\n')
            if not line.startswith('#'):
                temp=re.split('[;\t]', line)
                if len(temp) > 1:
                    self[temp[0]] = temp[1:]
                    if len(temp[1:]) < 2:
                        self[temp[0]].append('')
        ff.close()

    def save(self):
        if len(self.fileName) > 0:
            ff = codecs.open(self.fileName, "w", "utf_8_sig", errors="replace")
            for key in self.keys():
                line = key + ';' + self[key][0] + ';' + self[key][1] + '\n'
                ff.write(line)
            ff.close()

"""
    Initialisation du dictionnaire de décodage
"""
__dico_deco__ = LCDictionnary()

def loadLCDict(filename):
    global __dico_deco__

    __dico_deco__.load(filename)

def getLCDictKeys():
    return __dico_deco__.keys()

def getLCDictEntry(key):
    try:
        return __dico_deco__[key]
    except:
        return ['', '']

def delLCDictEntry(key):
    try:
        del __dico_deco__[key]
        __dico_deco__.save()
    except:
        pass

def setLCDictEntry(key, phon, syll):
    try:
        __dico_deco__[key] = [phon, syll]
        __dico_deco__.save()
    except:
        pass

#########################################################################################################
#########################################################################################################
#
#    Cette partie du code est destinée au traitement des textes pour en extraires des
#    phonèmes et des syllabes.
#
#                                    @@@@@@@@@@@@@@@@@@@@@@
#
#########################################################################################################
#########################################################################################################

# configuration du niveau de log (DEBUG = le plus bas niveau ; CRITICAL = le plus haut niveau)
#try:
#    flog = os.path.dirname(os.path.abspath(__file__))+os.sep+"lirecouleur.log"
#except:
#    flog = "lirecouleur.log"
#logging.basicConfig(level = logging.ERROR,
        #format="%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s : %(message)s",
        #filename = flog)

###################################################################################
# passage éventuel en unicode (sauf pour Python 3)
###################################################################################
def u(txt):
    try:
        return unicode(txt, 'utf-8')
    except:
        return txt

###################################################################################
# Liste des mots non correctement traités :
# agenda, consensus, référendum
###################################################################################

###################################################################################
# Les phonèmes sont codés en voyelles (v), consonnes (c) et semi-voyelles (s)
###################################################################################
syllaphon = {
    'v':['a','q','q_caduc','i','o','o_comp','o_ouvert','u','y','e','e_comp','e^',
    'e^_comp','a~','e~','x~','o~','x','x^','wa', 'w5'],
    'c':['p','t','k','b','d','g','f','f_ph','s','s^','v','z','z^','l','r','m','n',
    'k_qu','z^_g','g_u','s_c','s_t','z_s','ks','gz'],
    's':['j','g~','n~','w'],
    '#':['#','verb_3p']
}

#########################################################################################################
# Alphabet phonétique ascii : voir http://www.icp.inpg.fr/ICP/avtts/phon.fr.html
# Outil inestimable : http://www.lexique.org/moteur
#########################################################################################################

###################################################################################
# Ensemble de verbes qui se terminent par -ier // attention : pas d'accents !!
###################################################################################
verbes_ier = ['affilier','allier','allier','amnistier','amplifier','anesthesier','apparier',
'approprier','apprecier','asphyxier','associer','atrophier','authentifier','autographier',
'autopsier','balbutier','bonifier','beatifier','beneficier','betifier','calligraphier','calomnier',
'carier','cartographier','certifier','charrier','chier','choregraphier','chosifier','chatier',
'clarifier','classifier','cocufier','codifier','colorier','communier','conchier','concilier',
'confier','congedier','contrarier','copier','crier','crucifier','dactylographier',
'differencier','disgracier','disqualifier','dissocier','distancier','diversifier','domicilier',
'decrier','dedier','defier','deifier','delier','demarier','demultiplier','demystifier','denazifier',
'denier','deplier','deprecier','dequalifier',u('dévier'),'envier','estropier','excommunier',
'exemplifier','exfolier','expatrier','expier','exproprier','expedier','extasier','falsifier',
'fier','fluidifier','fortifier','frigorifier','fructifier','gazeifier','glorifier','gracier',
'gratifier','horrifier','humidifier','humilier','identifier','incendier','ingenier','initier',
'injurier','intensifier','inventorier','irradier','justifier','licencier','lier','liquefier',
'lubrifier','magnifier','maleficier','manier','marier','mendier','modifier','momifier','mortifier',
'multiplier','mystifier','mythifier','mefier','nier','notifier','negocier','obvier','officier',
'opacifier','orthographier','oublier','pacifier','palinodier','pallier','parier','parodier',
'personnifier','photocopier','photographier','plagier','planifier','plastifier','plier','polycopier',
'pontifier','prier','privilegier','psalmodier','publier','purifier','putrefier','pepier','petrifier',
'qualifier','quantifier','radier','radiographier','rallier','ramifier','rapatrier','rarefier',
'rassasier','ratifier','razzier','recopier','rectifier','relier','remanier','remarier',
'remercier','remedier','renier','renegocier','replier','republier','requalifier','revivifier',
'reverifier','rigidifier','reconcilier','recrier','reexpedier','refugier','repertorier','repudier',
'resilier','reunifier','reedifier','reetudier','sacrifier','salarier','sanctifier','scier',
'signifier','simplifier','skier','solidifier','soucier','spolier','specifier','statufier','strier',
'stupefier','supplicier','supplier','serier','terrifier','tonifier','trier','tumefier',
'typographier','telegraphier','unifier','varier','versifier','vicier','vitrifier','vivifier',
'verifier','echographier','ecrier','edifier','electrifier','emulsifier','epier','etudier']

###################################################################################
# Ensemble de verbes qui se terminent par -mer
###################################################################################
verbes_mer = ['abimer','acclamer','accoutumer','affamer','affirmer','aimer',
'alarmer','allumer','amalgamer','animer','armer','arrimer','assommer','assumer',
'blasphemer','blamer','bramer','brimer','calmer','camer','carmer','charmer',
'chloroformer','chomer','clamer','comprimer','confirmer','conformer','consommer',
'consumer','costumer','cramer','cremer','damer','diffamer','diplomer','decimer',
'declamer','decomprimer','deformer','degommer','denommer','deplumer','deprimer',
'deprogrammer','desaccoutumer','desarmer','desinformer','embaumer','embrumer',
'empaumer','enfermer','enflammer','enfumer','enrhumer','entamer','enthousiasmer',
'entraimer','envenimer','escrimer','estimer','exclamer','exhumer','exprimer',
'fantasmer','fermer','filmer','flemmer','former','frimer','fumer','gendarmer',
'germer','gommer','grammer','grimer','groumer','humer','imprimer','infirmer',
'informer','inhumer','intimer','lamer','limer','legitimer','mimer','mesestimer',
'nommer','opprimer','palmer','parfumer','parsemer','paumer','plumer','pommer',
'primer','proclamer','programmer','preformer','prenommer','presumer','pamer',
'perimer','rallumer','ramer','ranimer','refermer','reformer','refumer','remplumer',
'renfermer','renommer','rentamer','reprogrammer','ressemer','retransformer','rimer',
'rythmer','reaccoutumer','reaffirmer','reanimer','rearmer','reassumer','reclamer',
'reformer','reimprimer','reprimer','resumer','retamer','semer','slalomer','sommer',
'sublimer','supprimer','surestimer','surnommer','tramer','transformer',
'trimer','zoomer','ecremer','ecumer','elimer']

###################################################################################
# Ensemble de mots qui se terminent par -ent
###################################################################################
mots_ent = [u('absent'), u('abstinent'), u('accent'), u('accident'), u('adhérent'), u('adjacent'),
u('adolescent'), u('afférent'), u('agent'), u('ambivalent'), u('antécédent'), u('apparent'),
u('arborescent'), u('ardent'), u('ardent'), u('argent'), u('arpent'), u('astringent'), u('auvent'),
u('avent'), u('cent'), u('chiendent'), u('client'), u('coefficient'), u('cohérent'), u('dent'),
u('différent'), u('diligent'), u('dissident'), u('divergent'), u('dolent'), u('décadent'), u('décent'),
u('déficient'), u('déférent'), u('déliquescent'), u('détergent'), u('excipient'), u('fervent'), u('flatulent'),
u('fluorescent'), u('fréquent'), u('féculent'), u('gent'), u('gradient'), u('grandiloquent'),
u('immanent'), u('imminent'), u('impatient'), u('impertinent'), u('impotent'), u('imprudent'),
u('impudent'), u('impénitent'), u('incandescent'), u('incident'), u('incohérent'), u('incompétent'),
u('inconscient'), u('inconséquent'), u('incontinent'), u('inconvénient'), u('indifférent'), u('indigent'),
u('indolent'), u('indulgent'), u('indécent'), u('ingrédient'), u('inhérent'), u('inintelligent'),
u('innocent'), u('insolent'), u('intelligent'), u('interférent'), u('intermittent'), u('iridescent'),
u('lactescent'), u('latent'), u('lent'), u('luminescent'), u('malcontent'), u('mécontent'), u('occident'),
u('omnipotent'), u('omniprésent'), u('omniscient'), u('onguent'), u('opalescent'), u('opulent'),
u('orient'), u('paravent'), u('parent'), u('patent'), u('patient'), u('permanent'), u('pertinent'), u('phosphorescent'),
u('polyvalent'), u('pourcent'), u('proéminent'), u('prudent'), u('précédent'), u('présent'),
u('prévalent'), u('pschent'), u('purulent'), u('putrescent'), u('pénitent'), u('quotient'),
u('relent'), u('récent'), u('récipient'), u('récurrent'), u('référent'), u('régent'), u('rémanent'),
u('réticent'), u('sanguinolent'), u('sergent'), u('serpent'), u('somnolent'), u('souvent'),
u('spumescent'), u('strident'), u('subconscient'), u('subséquent'), u('succulent'), u('tangent'),
u('torrent'), u('transparent'), u('trident'), u('truculent'), u('tumescent'), u('turbulent'),
u('turgescent'), u('urgent'), u('vent'), u('ventripotent'), u('violent'), u('virulent'), u('effervescent'),
u('efficient'), u('effluent'), u('engoulevent'), u('entregent'), u('escient'), u('event'),
u('excédent'), u('expédient'), u('éloquent'), u('éminent'), u('émollient'), u('évanescent'), u('évent')]

verbes_enter = [u('absenter'),u('accidenter'),u('agrémenter'),u('alimenter'),u('apparenter'),
u('cimenter'),u('contenter'),u('complimenter'),u('bonimenter'),u('documenter'),u('patienter'),
u('parlementer'),u('ornementer'),u('supplémenter'),u('argenter'),u('éventer'),u('supplémenter'),
u('tourmenter'),u('violenter'),u('arpenter'),u('serpenter'),u('coefficienter'), u('argumenter'),
u('présenter')]

###################################################################################
# Règle spécifique de traitement des successions de lettres finales 'ient'
#     sert à savoir si la séquence 'ient' se prononce [i][#] ou [j][e~]
###################################################################################
def regle_ient(mot, pos_mot):
    m = re.match(u('[bcçdfghjklnmpqrstvwxz]ient'), mot[-5:])
    if m == None or (pos_mot < len(mot[:-4])):
        # le mot ne se termine pas par 'ient' (précédé d'une consonne)
        # ou alors on est en train d'étudier une lettre avant la terminaison en 'ient'
        return False

    # il faut savoir si le mot est un verbe dont l'infinitif se termine par 'ier' ou non
    pseudo_infinitif = mot[:-2]+'r'
    if pseudo_infinitif in verbes_ier:
        logging.info("func regle_ient : "+mot+" ("+pseudo_infinitif+")")
        return True
    pseudo_infinitif = texte_sans_accent(pseudo_infinitif)
    if len(pseudo_infinitif) > 1 and pseudo_infinitif[1] == '@':
        # mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
        pseudo_infinitif = pseudo_infinitif[2:]
    if pseudo_infinitif in verbes_ier:
        logging.info("func regle_ient : "+mot+" ("+pseudo_infinitif+")")
        return True
    return False

###################################################################################
# Règle spécifique de traitement des successions de lettres '*ent'
#     sert à savoir si le mot figure dans les mots qui se prononcent a~ à la fin
###################################################################################
def regle_mots_ent(mot, pos_mot):
    m = re.match('^[bcdfghjklmnpqrstvwxz]ent(s?)$', mot)
    if m != None:
        logging.info(u("func regle_mots_ent : ")+mot+u(" -- mot commencant par une consonne et terminé par 'ent'"))
        return True

    # il faut savoir si le mot figure dans la liste des adverbes ou des noms répertoriés
    comparateur = mot
    if mot[-1] == 's':
        comparateur = mot[:-1]
    if pos_mot+2 < len(comparateur):
        return False

    if len(comparateur) > 1 and comparateur[1] == '@':
        # mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
        comparateur = comparateur[2:]

    # comparaison directe avec la liste de mots où le 'ent' final se prononce [a~]
    if comparateur in mots_ent:
        logging.info(u("func regle_mots_ent : ")+mot+u(" -- mot répertorié"))
        return True

    # comparaison avec la liste de verbes qui se terminent par 'enter'
    pseudo_verbe = comparateur+'er'
    if pseudo_verbe in verbes_enter:
        logging.info(u("func regle_mots_ent : ")+mot+u(" -- verbe 'enter'"))
        return True

    return False

###################################################################################
# Règle spécifique de traitement des successions de lettres 'ment'
#     sert à savoir si le mot figure dans les mots qui se prononcent a~ à la fin
###################################################################################
def regle_ment(mot, pos_mot):
    m = re.match('ment', mot[-4:])
    if m == None or (pos_mot < len(mot[:-3])):
        # le mot ne se termine pas par 'ment'
        # ou alors on est en train d'étudier une lettre avant la terminaison en 'ment'
        return False

    # il faut savoir si le mot figure dans la liste des verbes terminés par -mer
    pseudo_infinitif = texte_sans_accent(mot[:-2]+'r')
    if len(pseudo_infinitif) > 1 and pseudo_infinitif[1] == '@':
        # mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
        pseudo_infinitif = pseudo_infinitif[2:]
    if pseudo_infinitif in verbes_mer:
        return False

    # dernier test : le verbe dormir (ils/elles dorment)
    if len(mot) > 6:
        if re.match('dorment', mot[-7:]) != None:
            return False
    logging.info(u("func regle_ment : ")+mot+" ("+pseudo_infinitif+")")
    return True

def regle_verbe_mer(mot, pos_mot):
    """L'inverse de la règle ci-dessus ou presque"""
    m = re.match('ment', mot[-4:])
    if m == None or (pos_mot < len(mot[:-3])):
        # le mot ne se termine pas par 'ment'
        # ou alors on est en train d'étudier une lettre avant la terminaison en 'ment'
        return False

    return not regle_ment(mot, pos_mot)

###################################################################################
# Règle spécifique de traitement des successions de lettres finales 'er'
#     sert à savoir si le mot figure dans la liste des exceptions
###################################################################################
def regle_er(mot, pos_mot):
    # prendre le mot au singulier uniquement
    m_sing = mot
    if mot[-1] == 's':
        m_sing = mot[:-1]

    if len(m_sing) > 1 and m_sing[1] == '@':
        # mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
        m_sing = m_sing[2:]

    # tester la terminaison
    m = re.match('er', m_sing[-2:])
    if m == None or (pos_mot < len(m_sing[:-2])):
        # le mot ne se termine pas par 'er'
        # ou alors on est en train d'étudier une lettre avant la terminaison en 'er'
        return False

    # il faut savoir si le mot figure dans la liste des exceptions
    exceptions_final_er = ['amer', 'cher', 'hier', 'mer', 'coroner', 'charter', 'cracker',
    'chester', 'doppler', 'cascher', 'bulldozer', 'cancer', 'carter', 'geyser', 'cocker', 'pullover',
    'alter', 'aster', 'fer', 'ver', 'diver', 'perver', 'enfer', 'traver', 'univer', 'cuiller', 'container', 'cutter',
    u('révolver'), 'super', 'master']
    if m_sing in exceptions_final_er:
        logging.info(u("func regle_er : ")+mot+u(" -- le mot n'est pas une exception comme 'amer' ou 'cher'"))
        return True
    return False

###################################################################################
# Règle spécifique de traitement des noms communs qui se terminent par 'ai'
#   Dans les verbes terminés par 'ai', le phonème est 'é'
#   Dans les noms communs terminés par 'ai', le phonème est 'ê'
###################################################################################
def regle_nc_ai_final(mot, pos_mot):
    possibles = ['balai', 'brai', 'chai', u('déblai'), u('délai'), 'essai', 'frai', 'geai', 'lai', 'mai',
                'minerai', 'papegai', 'quai', 'rai', 'remblai']

    m_seul = mot
    if len(m_seul) > 1 and m_seul[1] == '@':
        # mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
        m_seul = m_seul[2:]

    if m_seul in possibles:
        res = (pos_mot == len(mot)-1)
        logging.info(u("func regle_nc_ai_final : ")+mot+" -- "+str(res))
        return res
    return False

###################################################################################
# Règle spécifique de traitement des successions de lettres 'eu('
#     Sert à savoir si le mot est le verbe avoir conjugué (passé simple, participe
#   passé ou subjonctif imparfait
###################################################################################
def regle_avoir(mot, pos_mot):
    possibles = ['eu', 'eue', 'eues',
                'eus', 'eut', u('eûmes'), u('eûtes'), 'eurent',
                'eusse', 'eusses', u('eût'), 'eussions', 'eussiez', 'eussent']
    if mot in possibles:
        res = (pos_mot < 2)
        logging.info(u("func regle_avoir : ")+mot+" -- "+str(res))
        return res
    return False

###################################################################################
# Règle spécifique de traitement des mots qui se terminent par "us".
# Pour un certain nombre de ces mots, le 's' final se prononce.
###################################################################################
def regle_s_final(mot, pos_mot):
    mots_s_final = ['abribus','airbus','autobus','bibliobus','bus','nimbus','gibus',
    'microbus','minibus','mortibus','omnibus','oribus', u('pédibus'), 'quibus', 'rasibus',
    u('rébus'),'syllabus','trolleybus','virus','antivirus','anus','asparagus', u('médius'),
    'autofocus','focus','benedictus','bonus','campus','cirrus','citrus',
    'collapsus','consensus','corpus','crochus','crocus',u('crésus'),'cubitus',u('humérus'),
    'diplodocus','eucalyptus','erectus','hypothalamus','mordicus','mucus','stratus',
    'nimbostratus','nodus','modus','opus','ours','papyrus','plexus','plus','processus','prospectus',
    'lapsus','prunus','quitus',u('rétrovirus'),'sanctus','sinus','solidus','liquidus',
    'stimulus','stradivarius','terminus','tonus','tumulus',u('utérus'),'versus',u('détritus'),
    'ratus',
    'couscous', 'burnous', 'tous',
    'anis','bis','anubis',
    'albatros','albinos','calvados','craignos',u('mérinos'),u('rhinocéros'),'tranquillos',
    u('tétanos'),'os',
    'alias','atlas',u('hélas'),'madras','sensas','tapas','trias','vasistas','hypocras',
    'gambas','as',
    'biceps','quadriceps','chips','relaps','forceps','schnaps','laps','oups','triceps','princeps',u('tricératops')]

    m_seul = mot
    if len(m_seul) > 1 and m_seul[1] == '@':
        # mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
        m_seul = m_seul[2:]

    if m_seul in mots_s_final:
        logging.info(u("func regle_s_final : ")+m_seul+u(" -- mot avec un 's' final qui se prononce"))
        return True
    return False

###################################################################################
# Règle spécifique de traitement des mots qui se terminent par la lettre "t" prononcée.
###################################################################################
def regle_t_final(mot, pos_mot):
    mots_t_final = ['accessit','cet','but','diktat','kumquat','prurit','affidavit','dot','rut','audit',
    'exeat','magnificat','satisfecit','azimut','exit','mat','scorbut','brut',
    'fiat','mazout','sinciput','cajeput','granit','net','internet','transat','sept',
    'chut','huit','obit','transit',u('coït'),'incipit','occiput','ut','comput',
    u('introït'),'pat','zut',u('déficit'),'inuit',u('prétérit'),
    'gadget','kilt','kit','scout','fret']

    # prendre le mot au singulier uniquement
    m_sing = mot
    if mot[-1] == 's':
        m_sing = mot[:-1]

    if len(m_sing) > 1 and m_sing[1] == '@':
        # mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
        m_sing = m_sing[2:]

    if m_sing in mots_t_final:
        logging.info(u("func regle_t_final : ")+mot+u(" -- mot avec un 't' final qui se prononce"))
        return True
    return False


###################################################################################
# Règle spécifique de traitement de quelques mots qui se terminent par 'tien' et
# dans lesquels le 't' se prononce [t]
###################################################################################
def regle_tien(mot, pos_mot):
    # prendre le mot au singulier uniquement
    m_sing = mot
    if m_sing[-1] == 's':
        m_sing = mot[:-1]

    # tester la terminaison
    m = re.match('tien', m_sing[-4:])
    if m == None or (pos_mot < len(m_sing[:-4])):
        # le mot ne se termine pas par 'tien'
        # ou alors on est en train d'étudier une lettre avant la terminaison en 'tien'
        return False

    # il faut savoir si le mot figure dans la liste des exceptions
    exceptions_final_tien = [u('chrétien'), u('entretien'), u('kantien'),u('proustien'),u('soutien')]
    if m_sing in exceptions_final_tien:
        logging.info(u("func regle_tien : ")+mot+u(" -- mot où le 't' de 'tien' se prononce 't'"))
        return True
    return False

###################################################################################
# Ensemble des règles d'extraction des phonèmes
# '*' signifie 'suivi par n'importe quelle lettre
# '@' signifie 'dernière lettre du mot
#
# format de l'automate:
#        'lettre': [[règles l'ordre où elles doivent être déclenchées],[liste des règles]]
#
#     ATTENTION. Il faut faire attention à l'ordre de précédence des règles. Plusieurs règles peuvent
#    en effet s'appliquer pour une même succession de lettres. Il faut ranger les règles de la plus
#    spécifique à la plus générale.
#
# format d'une règle :
#        'nom_de_la_regle': [motif, phoneme, pas]
#
#    motif : il s'agit d'une expression régulière qui sert à tester les successions de lettres qui suivent
#        la lettre en cours de traitement dans le mot et les successions de lettres qui précèdent la lettre
#        en cours de traitement.
#    phoneme : le nom du phonème codé selon le format ascii décrit dans
#        http://www.icp.inpg.fr/ICP/avtts/phon.fr.html
#    pas : le nombre de lettres à lire à partir de la lettre courante si le motif a été reconnu
#        dans le mot de part et d'autre de la lettre en cours de traitement.
#
###################################################################################
autom = {
    'a' : [['u','il','in','nc_ai_fin','ai_fin','i','n','m','nm','y_except','y'],
            {'n':[{'+':u(r"n[bcçdfgjklmpqrstvwxz]")},'a~',2],
            'm':[{'+':u(r"m[mbp]")},'a~',2], ## règle du m devant m, b, p
            'nm':[{'+':r"n(s?)$"},'a~',2],
            'y_except':[{'-':r"(^b|cob|cip)",'+':r"y"},'a',1], ## exception : baye, cobaye
            'y':[{'+':r"y"},'e^_comp',1],
            'u':[{'+':r"u"},'o_comp',2],
            'il':[{'+':r"il($|l)"},'a',1],
            'in':[{'+':u(r"i[nm]([bcçdfghjklnmpqrstvwxz]|$)")},'e~',3], ## toute succession 'ain' 'aim' suivie d'une consonne ou d'une fin de mot
            'nc_ai_fin':[regle_nc_ai_final,'e^_comp',2],
            'ai_fin':[{'+':r"i$"},'e_comp',2],
            'i':[{'+':u(r"[iî]")},'e^_comp',2],
            '*':[{},'a',1]}],
    u('â') : [[],
            {'*':[{},'a',1]}],
    u('à') : [[],
            {'*':[{},'a',1]}],
    'b' : [['b','plomb'],
            {'b':[{'+':r"b"},'b',2],
            'plomb':[{'-':r"plom",'+':r"(s?)$"},'#',1], ## le "b" à la fin de plomb ne se prononce pas
            '*':[{},'b',1]}],
    'c' : [['eiy','choeur_1','choeur_2','chor','psycho','brachio','cheo','chest','chiro','chlo_chlam','chr',
            'h','erc_orc','cisole','c_muet_fin','onc_donc','nc_muet_fin','_spect','_inct','cciey','cc','apostrophe'],
            {'choeur_1':[{'+':r"hoe"},'k',2],
            'choeur_2':[{'+':u(r"hœ")},'k',2],
            'chor':[{'+':r"hor"},'k',2], ## tous les "choral, choriste"... exceptions non traitées : chorizo, maillechort
            'psycho':[{'-':r"psy",'+':r"ho"},'k',2], ## tous les "psycho" quelque chose
            'brachio':[{'-':r"bra",'+':r"hio"},'k',2], ## brachiosaure, brachiocéphale
            'cheo':[{'+':u(r"héo")},'k',2], ## archéo..., trachéo...
            'chest':[{'+':r"hest"},'k',2], ## orchestre et les mots de la même famille
            'chiro':[{'+':r"hiro[p|m]"},'k',2], ## chiroptère, chiromancie
            'chlo_chlam':[{'+':r"hl(o|am)"},'k',2], ## chlorure, chlamyde
            'chr':[{'+':r"hr"},'k',2], ## de chrétien à synchronisé
            'h':[{'+':r"h"},'s^',2],
            'eiy':[{'+':u(r"[eiyéèêëîï]")},'s_c',1],
            'cisole':[{'+':r"$",'-':r"^"},'s_c',1], ## exemple : c'est
            'erc_orc':[{'-':r"[e|o]r",'+':r"(s?)$"},'#',1], ## clerc, porc,
            'c_muet_fin':[{'-':r"taba|accro",'+':r"(s?)$"},'#',1], ## exceptions traitées : tabac, accroc
            'onc_donc':[{'-':r"^on|^don"},'k',1], ## non exceptions traitées : onc, donc
            'nc_muet_fin':[{'-':r"n",'+':r"(s?)$"},'#',1], ## exceptions traitées : tous les mots terminés par *nc
            '_spect':[{'-':r"spe",'+':r"t(s?)$"},'#',1], ## respect, suspect, aspect
            '_inct':[{'-':r"in",'+':r"t(s?)$"},'#',1], ## instinct, succinct, distinct
            'cciey':[{'+':u(r"c[eiyéèêëîï]")},'k',1], ## accident, accepter, coccyx
            'cc':[{'+':r"c"},'k',2], ## accorder, accompagner
            'apostrophe':[{'+':r"(\'|\’)"},'s',2], ## apostrophe
            '*':[{},'k',1], '@':['','k',1]}],
 ## + tous les *nc sauf "onc" et "donc"
    u('ç') : [[],
            {'*':[{},'s',1]}],
    'd' : [['d','aujourdhui','disole','except','dmuet','apostrophe'],
            {'d':[{'+':r"d"},'d',2],
            'except':[{'-':u(r"(aï|oue)"), '+':r"(s?)$"},'d',1], ## aïd, caïd, oued
            'aujourdhui':[{'-':r"aujour"},'d',1], ## aujourd'hui
            'disole':[{'+':r"$",'-':r"^"},'d',1], ## exemple : d'abord
            'dmuet':[{'+':r"(s?)$"},'#',1], ## un d suivi éventuellement d'un s ex. : retards
            'apostrophe':[{'+':r"(\'|\’)"},'d',2], ## apostrophe
            '*':[{},'d',1]}],
    'e' : [['conj_v_ier','uient','ien','ien_2','een','except_en_1','except_en_2','_ent','clef','hier','adv_emment_fin',
            'ment','imparfait','verbe_3_pluriel','au',
            'avoir','monsieur','jeudi','jeu_','eur','eu','eu_accent_circ','in','eil','y','iy','ennemi','enn_debut_mot','dessus_dessous',
            'et','cet','t_final','eclm_final','est','drz_final','n','adv_emment_a','femme','lemme','em_gene','nm','tclesmesdes',
            'que_isole','que_gue_final','jtcnslemede','jean','ge','eoi','ex','ef','reqquechose','2consonnes','abbaye','e_muet','e_caduc','e_deb'],
            {'_ent':[regle_mots_ent,'a~',2], ## quelques mots (adverbes ou noms) terminés par ent
            'adv_emment_fin':[{'-':r"emm",'+':r"nt"},'a~',2], ## adverbe avec 'emment' => se termine par le son [a~]
            'ment':[regle_ment,'a~',2], ## on considère que les mots terminés par 'ment' se prononcent [a~] sauf s'il s'agit d'un verbe
            'imparfait':[{'-':r"ai",'+':r"nt$"},'verb_3p',3], ## imparfait à la 3ème personne du pluriel
            'verbe_3_pluriel':[{'+':r"nt$"},'q_caduc',1], ## normalement, pratiquement tout le temps verbe à la 3eme personne du pluriel
            'clef':[{'-':r"cl",'+':r"f"},'e_comp',2], ## une clef
            'hier':[regle_er,'e^_comp',1], ## encore des exceptions avec les mots terminés par 'er' prononcés 'R'
            'n':[{'+':u(r"n[bcçdfghjklmpqrstvwxz]")},'a~',2],
            'adv_emment_a':[{'+':r"mment"},'a',1], ## adverbe avec 'emment' => son [a]
            'eclm_final':[{'+':r"[clm](s?)$"},'e^_comp',1], ## donne le son [e^] et le l ou le c se prononcent (ex. : miel, sec)
            'femme':[{'-':r"f",'+':r"mm"},'a',1], ## femme et ses dérivés => son [a]
            'lemme':[{'-':r"l",'+':r"mm"},'e^_comp',1], ## lemme et ses dérivés => son [e^]
            'em_gene':[{'+':u(r"m[bcçdfghjklmnpqrstvwxz]")},'a~',2], ## 'em' cas général => son [a~]
            'uient':[{'-':r"ui",'+':r"nt$"},'#',3], ## enfuient, appuient, fuient, ennuient, essuient
            'conj_v_ier':[regle_ient,'#',3], ## verbe du 1er groupe terminé par 'ier' conjugué à la 3ème pers du pluriel
            'except_en_1':[{'-':u(r"exam|mino|édu"),'+':r"n(s?)$"},'e~',2], ## exceptions des mots où le 'en' final se prononce [e~] (héritage latin)
            'except_en_2':[{'-':u(r"[ao]ï"),'+':r"n(s?)$"},'e~',2], ## païen, hawaïen, tolstoïen
            'een':[{'-':u(r"é"),'+':r"n(s?)$"},'e~',2], ## les mots qui se terminent par 'éen'
            'ien':[{'-':r"[bcdlmrstvh]i",'+':u(r"n([bcçdfghjklpqrstvwxz]|$)")},'e~',2], ## certains mots avec 'ien' => son [e~]
            'ien_2':[{'-':r"ï",'+':u(r"n([bcçdfghjklpqrstvwxz]|$)")},'e~',2], ## certains mots avec 'ien' => son [e~]
            'nm':[{'+':r"[nm]$"},'a~',2],
            'drz_final':[{'+':r"[drz](s?)$"},'e_comp',2], ## e suivi d'un d,r ou z en fin de mot done le son [e]
            'que_isole':[{'-':r"^qu",'+':r"$"},'q',1], ## que isolé
            'que_gue_final':[{'-':r"[gq]u",'+':r"(s?)$"},'q_caduc',1], ## que ou gue final
            'jtcnslemede':[{'-':r"^[jtcnslmd]",'+':r"$"},'q',1], ## je, te, me, le, se, de, ne
            'tclesmesdes':[{'-':r"^[tcslmd]",'+':r"s$"},'e_comp', 2], ## mes, tes, ces, ses, les
            'in':[{'+':u(r"i[nm]([bcçdfghjklnmpqrstvwxz]|$)")},'e~',3], ## toute succession 'ein' 'eim' suivie d'une consonne ou d'une fin de mot
            'avoir':[regle_avoir,'y',2],
            'monsieur':[{'-':r"si",'+':r"ur"},'x^',2],
            'jeudi':[{'-':r"j",'+':r"udi"},'x^',2], ## jeudi
            'jeu_':[{'-':r"j",'+':r"u"},'x',2], ## tous les "jeu*" sauf jeudi
            'eur':[{'+':r"ur"},'x',2],
            'eu':[{'+':r"u"},'x',2],
            'eu_accent_circ':[{'+':u(r"û")},'x^',2],
            'est':[{'-':r"^",'+':r"st$"},'e^_comp',3],
            'et':[{'-':r"^",'+':r"t$"},'e_comp',2],
            'eil':[{'+':r"il"},'e^_comp',1],
            'y':[{'+':u(r"y[aeiouéèêààäôâ]")},'e^_comp',1],
            'iy':[{'+':r"[iy]"},'e^_comp',2],
            'cet':[{'-':r"^c",'+':r"[t]$"},'e^_comp',1], ## 'cet'
            't_final':[{'+':r"[t]$"},'e^_comp',2], ## donne le son [e^] et le t ne se prononce pas
            'au':[{'+':r"au"},'o_comp',3],
            'ennemi':[{'-':r"^",'+':r"nnemi"},'e^_comp',1], ## ennemi est l'exception ou 'enn' en début de mot se prononce 'èn' (cf. enn_debut_mot)
            'enn_debut_mot':[{'-':r"^",'+':r"nn"},'a~',2], ## 'enn' en début de mot se prononce 'en'
            'ex':[{'+':r"x"},'e^',1], ## e suivi d'un x se prononce è
            'ef':[{'+':r"[bf](s?)$"},'e^',1], ## e suivi d'un f ou d'un b en fin de mot se prononce è
            'reqquechose':[{'-':r"r",'+':u(r"[bcçdfghjklmnpqrstvwxz](h|l|r)")},'q',1], ## re-quelque chose : le e se prononce 'e'
            'dessus_dessous':[{'-':r"d",'+':r"ss(o?)us"},'q',1], ## dessus, dessous : 'e' = e
            '2consonnes':[{'+':u(r"[bcçdfghjklmnpqrstvwxz]{2}")},'e^_comp',1], ## e suivi de 2 consonnes se prononce è
            'e_deb':[{'-':r"^"},'q',1], ## par défaut, un 'e' en début de mot se prononce [q]
            'abbaye':[{'-':r"abbay",'+':r"(s?)$"},'#',1], ## ben oui...
            'e_muet':[{'-':u(r"[aeiouéèêà]"),'+':r"(s?)$"},'#',1], ## un e suivi éventuellement d'un 's' et précédé d'une voyelle ou d'un 'g' ex. : pie, geai
            'jean':[{'-':r"j",'+':r"an"},'#',1], ## jean
            'ge':[{'-':r"g",'+':u(r"[aouàäôâ]")},'#',1], ## un e précédé d'un 'g' et suivi d'une voyelle ex. : cageot
            'eoi':[{'+':r"oi"},'#',1], ## un e suivi de 'oi' ex. : asseoir
            'e_caduc':[{'-':u(r"[bcçdfghjklmnpqrstvwxzy]"),'+':r"(s?)$"},'q_caduc',1], ## un e suivi éventuellement d'un 's' et précédé d'une consonne ex. : correctes
            '*':[{},'q',1],
            '@':['','q_caduc',1]
            }],
    u('é') : [[],
            {'*':[{},'e',1]}],
    u('è') : [[],
            {'*':[{},'e^',1]}],
    u('ê') : [[],
            {'*':[{},'e^',1]}],
    u('ë') : [[],
            {'*':[{},'e^',1]}],
    'f' : [['f','oeufs'],
            {'f':[{'+':r"f"},'f',2],
             'oeufs':[{'-':u(r"(oeu|œu)"),'+':r"s"},'#',1], ## oeufs et boeufs
             '*':[{},'f',1]}],
    'g' : [['g','ao','eiy','aiguille','u_consonne','u','n','vingt','g_muet_oin',
            'g_muet_our','g_muet_an','g_muet_fin'],
            {'g':[{'+':r"g"},'g',2],
            'n':[{'+':r"n"},'n~',2],
            'ao':[{'+':r"a|o"},'g',1],
            'eiy':[{'+':u(r"[eéèêëïiy]")},'z^_g',1], ## un 'g' suivi de e,i,y se prononce [z^]
            'g_muet_oin':[{'-':r"oi(n?)"},'#',1], ## un 'g' précédé de 'oin' ou de 'oi' ne se prononce pas ; ex. : poing, doigt
            'g_muet_our':[{'-':r"ou(r)"},'#',1], ## un 'g' précédé de 'our' ou de 'ou(' ne se prononce pas ; ex. : bourg
            'g_muet_an':[{'-':r"(s|^ét|^r)an",'+':r"(s?)$"},'#',1], ## sang, rang, étang
            'g_muet_fin':[{'-':r"lon|haren"},'#',1], ## pour traiter les exceptions : long, hareng
            'aiguille':[{'-':r"ai",'+':r"u"},'g',1], ## encore une exception : aiguille et ses dérivés
            'vingt':[{'-':r"vin",'+':r"t"},'#',1], ## vingt
            'u_consonne':[{'+':u(r"u[bcçdfghjklmnpqrstvwxz]")},'g',1], ## gu suivi d'une consonne se prononce [g][y]
            'u':[{'+':r"u"},'g_u',2],
            '*':[{},'g',1]}],
    'h' : [[],
            {'*':[{},'#',1]}],
    'i' : [['ing','n','m','nm','prec_2cons','lldeb','vill','mill','tranquille',
            'ill','@ill','@il','ll','ui','ient_1','ient_2','ie','i_voyelle'],
            {'ing':[{'-':u(r"[bcçdfghjklmnpqrstvwxz]"),'+':r"ng$"},'i',1],
            'n':[{'+':u(r"n[bcçdfghjklmpqrstvwxz]")},'e~',2],
            'm':[{'+':u(r"m[bcçdfghjklnpqrstvwxz]")},'e~',2],
            'nm':[{'+':r"[n|m]$"},'e~',2],
            'prec_2cons':[{'-':r"[ptkcbdgfv][lr]"},'i',1], ## précédé de 2 consonnes (en position 3), doit apparaître comme [ij]
            'lldeb':[{'-':r"^",'+':r"ll"},'i',1],
            'vill':[{'-':r"v",'+':r"ll"},'i',1],
            'mill':[{'-':r"m",'+':r"ll"},'i',1],
            'tranquille':[{'-':r"tranqu",'+':r"ll"},'i',1],
            'ill':[{'+':r"ll",'-':u(r"[bcçdfghjklmnpqrstvwxz](u?)")},'i',1], ## précédé éventuellement d'un u et d'une consonne, donne le son [i]
            '@ill':[{'-':r"[aeo]",'+':r"ll"},'j',3], ## par défaut précédé d'une voyelle et suivi de 'll' donne le son [j]
            '@il':[{'-':r"[aeou]",'+':r"l(s?)$"},'j',2], ## par défaut précédé d'une voyelle et suivi de 'l' donne le son [j]
            'll':[{'+':r"ll"},'j',3], ## par défaut avec ll donne le son [j]
            'ui':[{'-':r"u",'+':r"ent"},'i',1], ## essuient, appuient
            'ient_1':[regle_ient,'i',1], ## règle spécifique pour différencier les verbes du premier groupe 3ème pers pluriel
            'ient_2':[{'+':r"ent(s)?$"},'j',1], ## si la règle précédente ne fonctionne pas
            'ie':[{'+':r"e(s)?$"},'i',1], ## mots terminés par -ie(s|nt)
            'i_voyelle':[{'+':u(r"[aäâeéèêëoôöuù]")},'j',1], ## i suivi d'une voyelle donne [j]
            '*':[{},'i',1]}],
    u('ï') : [['thai', 'aie'],
            {'thai':[{'-':r"t(h?)a"},'j',1], ## taï, thaï et dérivés
            'aie':[{'-':r"[ao]",'+':r"e"},'j',1], ## païen et autres
            '*':[{},'i',1]}],
    u('î') : [[],
            {'*':[{},'i',1]}],
    'j' : [[],
            {'*':[{},'z^',1]}],
    'k' : [[],
            {'*':[{},'k',1]}],
    'l' : [['vill','mill','tranquille','illdeb','ill','eil','ll','excep_il', 'apostrophe','lisole'],
            {'vill':[{'-':r"^vi",'+':r"l"},'l',2], ## ville, village etc. => son [l]
            'mill':[{'-':r"^mi",'+':r"l"},'l',2], ## mille, million, etc. => son [l]
            'tranquille':[{'-':r"tranqui",'+':r"l"},'l',2], ## tranquille => son [l]
            'illdeb':[{'-':r"^i",'+':r"l"},'l',2], ## 'ill' en début de mot = son [l] ; exemple : illustration
            'lisole':[{'+':r"$",'-':r"^"},'l',1], ## exemple : l'animal
            'ill':[{'-':r".i",'+':r"l"},'j',2], ## par défaut, 'ill' donne le son [j]
            'll':[{'+':r"l"},'l',2], ## à défaut de l'application d'une autre règle, 'll' donne le son [l]
            'excep_il':[{'-':r"fusi|outi|genti",'+':r"(s?)$"},'#',1], ## les exceptions trouvées ou le 'l' à la fin ne se prononce pas : fusil, gentil, outil
            'eil':[{'-':r"e(u?)i"},'j',1], ## les mots terminés en 'eil' ou 'ueil' => son [j]
            'apostrophe':[{'+':r"(\'|\’)"},'l',2], ## apostrophe
            '*':[{},'l',1]}],
    'm' : [['m','damn','tomn','misole','apostrophe'],
            {'m':[{'+':r"m"},'m',2],
            'damn':[{'-':r"da",'+':r"n"},'#',1], ## regle spécifique pour 'damné' et ses dérivés
            'tomn':[{'-':r"to",'+':r"n"},'#',1], ## regle spécifique pour 'automne' et ses dérivés
            '*':[{},'m',1],
            'misole':[{'+':r"$",'-':r"^"},'m',1], ## exemple : m'a
            'apostrophe':[{'+':r"(\'|\’)"},'m',2] ## apostrophe
            }],
    'n' : [['ing','n','ment','urent','irent','erent','ent','nisole','apostrophe'],
            {'n':[{'+':r"n"},'n',2],
            'ment':[regle_verbe_mer,'verb_3p',2], ## on considère que les verbent terminés par 'ment' se prononcent [#]
            'urent':[{'-':r"ure",'+':r"t$"},'verb_3p',2], ## verbes avec terminaisons en -urent
            'irent':[{'-':r"ire",'+':r"t$"},'verb_3p',2], ## verbes avec terminaisons en -irent
            'erent':[{'-':u(r"ère"),'+':r"t$"},'verb_3p',2], ## verbes avec terminaisons en -èrent
            'ent':[{'-':r"e",'+':r"t$"},'verb_3p',2],
            'ing':[{'-':r"i",'+':r"g$"},'g~',2],
            '*':[{},'n',1],
            'nisole':[{'+':r"$",'-':r"^"},'n',1], ## exemple : n'a
            'apostrophe':[{'+':r"(\'|\’)"},'n',2] ## apostrophe
            }],
    'o' : [['in','oignon','i','ouat','oui','oue','tomn','monsieur','n','m','nm','y1','y2','u','o','oe_0',
            'oe_1','oe_2', 'oe_3','voeux','oeufs','noeud','oeu_defaut','oe_defaut'],
            {'in':[{'+':r"i[nm]([bcçdfghjklnmpqrstvwxz]|$)"},'w_e~',3],
            'oignon':[{'-':r"^",'+':r"ignon"},'o',2],
            'i':[{'+':u(r"(i|î)")},'wa',2],
            'oue':[{'-':r"^",'+':u(r"ue")},'w_e^_comp',3], # ouest, oued
            'oui':[{'-':r"^",'+':u(r"ui")},'w_i',3], # oui
            'ouat':[{'+':u(r"uat")},'wa',3],
            'u':[{'+':u(r"[uwûù]")},'u',2], ## son [u] : clou, clown
            'tomn':[{'-':r"t",'+':r"mn"},'o',1], ## regle spécifique pour 'automne' et ses dérivés
            'monsieur':[{'-':r"m",'+':r"nsieur"},'q',2],
            'n':[{'+':u(r"n[bcçdfgjklmpqrstvwxz]")},'o~',2],
            'm':[{'+':u(r"m[bcçdfgjklpqrstvwxz]")},'o~',2], ## toute consonne sauf le m
            'nm':[{'+':r"[nm]$"},'o~',2],
            'y1':[{'+':r"y$"},'wa',2],
            'y2':[{'+':r"y"},'wa',1],
            'o':[{'+':r"o"},'o',2], ## exemple : zoo
            'voeux':[{'+':r"eux"},'x^',3], ## voeux
            'noeud':[{'+':r"eud"},'x^',3], ## noeud
            'oeufs':[{'+':r"eufs"},'x^',3], ## traite oeufs et boeufs
            'oeu_defaut':[{'+':r"eu"},'x',3], ## exemple : oeuf
            'oe_0':[{'+':u(r"ê")},'wa',2],
            'oe_1':[{'-':r"c",'+':r"e"},'o',1], ## exemple : coefficient
            'oe_2':[{'-':r"m",'+':r"e"},'wa',2], ## exemple : moelle
            'oe_3':[{'-':r"f",'+':r"e"},'e',2], ## exemple : foetus
            'oe_defaut':[{'+':r"e"},'x',2], ## exemple : oeil
            '*':[{},'o',1]}],
    u('œ') : [['voeux','oeufs','noeud'],
            {'voeux':[{'+':r"ux"},'x^',2], ## voeux
            'noeud':[{'+':r"ud"},'x^',2], ## noeud
            'oeufs':[{'+':r"ufs"},'x^',2], ## traite oeufs et boeufs
            '*':[{'+':r"u"},'x^',2]}],
    u('ô') : [[],
            {'*':[{},'o',1]}],
    u('ö') : [[],
            {'*':[{},'o',1]}],
    'p' : [['h','oup','drap','trop','sculpt','sirop','sgalop','rps','amp','compt','bapti','sept','p'],
            {'p':[{'+':r"p"},'p',2],
            'oup':[{'-':r"[cl]ou",'+':r"$"},'#',1], ## les exceptions avec un p muet en fin de mot : loup, coup
            'amp':[{'-':r"c(h?)am",'+':r"$"},'#',1], ## les exceptions avec un p muet en fin de mot : camp, champ
            'drap':[{'-':r"dra",'+':r"$"},'#',1], ## les exceptions avec un p muet en fin de mot : drap
            'trop':[{'-':r"tro",'+':r"$"},'#',1], ## les exceptions avec un p muet en fin de mot : trop
            'sculpt':[{'-':r"scul",'+':r"t"},'#',1], ## les exceptions avec un p muet : sculpter et les mots de la même famille
            'sirop':[{'-':r"siro",'+':r"$"},'#',1], ## les exceptions avec un p muet en fin de mot : sirop
            'sept':[{'-':r"^se",'+':r"t(s?)$"},'#',1], ## les exceptions avec un p muet en fin de mot : sept
            'sgalop':[{'-':r"[gs]alo",'+':r"$"},'#',1], ## les exceptions avec un p muet en fin de mot : galop
            'rps':[{'-':r"[rm]",'+':r"s$"},'#',1], ## les exceptions avec un p muet en fin de mot : corps, camp
            'compt':[{'-':r"com",'+':r"t"},'#',1], ## les exceptions avec un p muet : les mots en *compt*
            'bapti':[{'-':r"ba",'+':r"ti"},'#',1], ## les exceptions avec un p muet : les mots en *bapti*
            'h':[{'+':r"h"},'f_ph',2],
            '*':[{},'p',1]}],
    'q' : [['qu','k'],
            {'qu':[{'+':r"u[bcçdfgjklmnpqrstvwxz]"},'k',1],
            'k':[{'+':r"u"},'k_qu',2],
            '*':[{},'k',1]}],
    'r' : [['monsieur','messieurs','gars','r'],
            {'monsieur':[{'-':r"monsieu"},'#',1],
            'messieurs':[{'-':r"messieu"},'#',1],
            'r':[{'+':r"r"},'r',2],
            'gars':[{'+':r"s",'-':r"ga"},'#',2], ## gars
            '*':[{},'r',1]}],
    's' : [['sch','h','s_final','parasit','para','mars','s','z','sisole','smuet','apostrophe'],
            {'sch':[{'+':r"ch"},'s^',3], ## schlem
            'h':[{'+':r"h"},'s^',2],
            's_final':[regle_s_final,'s',1], ## quelques mots terminés par -us, -is, -os, -as
            'z':[{'-':u(r"[aeiyouéèàüûùëöêîô]"),'+':u(r"[aeiyouéèàüûùëöêîô]")},'z_s',1], ## un s entre 2 voyelles se prononce [z]
            'parasit':[{'-':r"para",'+':r"it"},'z_s',1], ## parasit*
            'para':[{'-':r"para"},'s',1], ## para quelque chose (parasol, parasismique, ...)
            's':[{'+':r"s"},'s',2], ## un s suivi d'un autre s se prononce [s]
            'sisole':[{'+':r"$",'-':r"^"},'s',1], ## exemple : s'approche
            'mars':[{'+':r"$",'-':r"mar"},'s',1], ## mars
            'smuet':[{'-':r"(e?)",'+':r"$"},'#',1], ## un s en fin de mot éventuellement précédé d'un e ex. : correctes
            'apostrophe':[{'+':r"(\'|\’)"},'s',2], ## apostrophe
            '*':[{},'s',1],
            '@':[{},'#',1]}],
    't' : [['t','tisole','except_tien','_tien','cratie','vingt','tion',
            'ourt','_inct','_spect','_ct','_est','t_final','tmuet','apostrophe'],
            {'t':[{'+':r"t"},'t',2],
            'except_tien':[regle_tien,'t',1], ## quelques mots où 'tien' se prononce [t]
            '_tien':[{'+':r"ien"},'s_t',1],
            'cratie':[{'-':r"cra",'+':r"ie"},'s_t',1],
            'vingt':[{'-':r"ving",'+':r"$"},'t',1], ## vingt mais pas vingts
            'tion':[{'+':r"ion"},'s_t',1],
            'tisole':[{'+':r"$",'-':r"^"},'t',1], ## exemple : demande-t-il
            'ourt':[{'-':r"(a|h|g)our",'+':r"$"},'t',1], ## exemple : yaourt, yoghourt, yogourt
            '_est':[{'-':r"es",'+':r"(s?)$"},'t',1], ## test, ouest, brest, west, zest, lest
            '_inct':[{'-':r"inc",'+':r"(s?)$"},'#',1], ## instinct, succinct, distinct
            '_spect':[{'-':r"spec",'+':r"(s?)$"},'#',1], ## respect, suspect, aspect
            '_ct':[{'-':r"c",'+':r"(s?)$"},'t',1], ## tous les autres mots terminés par 'ct'
            't_final':[regle_t_final,'t',1], ## quelques mots où le "t" final se prononce
            'tmuet':[{'+':r"(s?)$"},'#',1], ## un t suivi éventuellement d'un s ex. : marrants
            '*':[{},'t',1],
            'apostrophe':[{'+':r"(\'|\’)"},'t',2], ## apostrophe
            '@':[{},'#',1]}],
    'u' : [['um','n','nm','ueil'],
            {'um':[{'-':r"[^aefo]",'+':r"m$"},'o',1],
            'n':[{'+':u(r"n[bcçdfghjklmpqrstvwxz]")},'x~',2],
            'nm':[{'+':r"[nm]$"},'x~',2],
            'ueil':[{'+':r"eil"},'x',2], ## mots terminés en 'ueil' => son [x^]
            '*':[{},'y',1]}],
    u('û') : [[],
            {'*':[{},'y',1]}],
    u('ù') : [[],
            {'*':[{},'y',1]}],
    'v' : [[],
            {'*':[{},'v',1]}],
    'w' : [['wurt','wisig','wag','wa', 'wi'],
            {'wurt':[{'+':r"urt"},'v',1], # saucisse
            'wisig':[{'+':r"isig"},'v',1], # wisigoth
            'wag':[{'+':r"ag"},'v',1], # wagons et wagnérien
            'wa':[{'+':r"a"},'wa',2], # watt, wapiti, etc.
            'wi':[{'+':r"i"},'w_i',2], # kiwi
            '*':[{},'w',1]}],
    'x' : [['six_dix','gz_1','gz_2','gz_3','gz_4','gz_5','_aeox','fix','_ix'],
            {'six_dix':[{'-':r"(s|d)i"},'s_x',1],
            'gz_1':[{'-':r"^",'+':u(r"[aeiouéèàüëöêîôûù]")},'gz',1], ## mots qui commencent par un x suivi d'une voyelle
            'gz_2':[{'-':r"^(h?)e",'+':u(r"[aeiouéèàüëöêîôûù]")},'gz',1], ## mots qui commencent par un 'ex' ou 'hex' suivi d'une voyelle
            'gz_3':[{'-':r"^coe",'+':u(r"[aeiouéèàüëöêîôûù]")},'gz',1], ## mots qui commencent par un 'coex' suivi d'une voyelle
            'gz_4':[{'-':r"^ine",'+':u(r"[aeiouéèàüëöêîôûù]")},'gz',1], ## mots qui commencent par un 'inex' suivi d'une voyelle
            'gz_5':[{'-':u(r"^(p?)rée"),'+':u(r"[aeiouéèàüëöêîôûù]")},'gz',1], ## mots qui commencent par un 'réex' ou 'préex' suivi d'une voyelle
            '_aeox':[{'-':r"[aeo]"},'ks',1],
            'fix':[{'-':r"fi"},'ks',1],
            '_ix':[{'-':u(r"(remi|obéli|astéri|héli|phéni|féli)")},'ks',1],
            '*':[{},'ks',1],
            '@':[{},'#',1]}],
    'y' : [['m','n','nm','abbaye','y_voyelle'],
            {'y_voyelle':[{'+':u(r"[aeiouéèàüëöêîôûù]")},'j',1], ## y suivi d'une voyelle donne [j]
            'abbaye':[{'-':r"abba",'+':r"e"},'i', 1], ## abbaye... bien irrégulier
            'n':[{'+':u(r"n[bcçdfghjklmpqrstvwxz]")},'e~',2],
            'm':[{'+':r"m[mpb]"},'e~',2],
            'nm':[{'+':r"[n|m]$"},'e~',2],
            '*':[{},'i',1]}],
    'z' : [['riz', 'iz', 'gaz'],
            {'riz':[{'-':r"i",'+':r"$"},'#',1], ## y suivi d'une voyelle donne [j]
            'iz':[{'-':r"i",'+':r"$"},'z',1],
            'gaz':[{'-':r"a",'+':r"$"},'z',1],
            '*':[{},'z',1],
            '@':[{},'#',1]}],
    '\'' : [[],
            {'*':[{},'#',1],
            '@':[{},'#',1]}],
    '@' : [[],
            {'*':[{},'#',1],
            '@':[{},'#',1]}],
    '_' : [[],
            {'*':[{},'#',1],
            '@':[{},'#',1]}]
}

###################################################################################
# Élimine des caractères de la chaîne de caractères à traiter
###################################################################################
def nettoyeur_caracteres(paragraphe):
    # suppression des \r qui engendrent des décalages de codage sous W*
    nparagraphe = paragraphe.replace('\r', '')

    return nparagraphe

###################################################################################
# Élimine les caractères accentués et les remplace par des non accentués
###################################################################################
def texte_sans_accent(texte):
    utexte = u(texte) # codage unicode
    ultexte = utexte.lower() # tout mettre en minuscules

    ultexte = re.sub(u('[àäâ]'), 'a', ultexte)
    ultexte = re.sub(u('[éèêë]'), 'e', ultexte)
    ultexte = re.sub(u('[îï]'), 'i', ultexte)
    ultexte = re.sub(u('[ôö]'), 'o', ultexte)
    ultexte = re.sub(u('[ûù]'), 'u', ultexte)
    ultexte = re.sub(u('ç'), 'c', ultexte)
    ultexte = re.sub(u('œ'), 'e', ultexte)

    return ultexte

###################################################################################
# Élimine des caractères de la chaîne de caractères à traiter
###################################################################################
def pretraitement_texte(texte, substitut=' '):
    utexte = u(texte) # codage unicode
    ultexte = utexte.lower() # tout mettre en minuscules
    ultexte = re.sub(u('[\'´’]'), '@', ultexte) # remplace les apostrophes par des @
    ultexte = re.sub(u('[^a-zA-Z0-9@àäâéèêëîïôöûùçœ]'), ' ', ultexte) # ne garde que les caractères significatifs

    return ultexte

###################################################################################
# Teste l'application d'une règle
###################################################################################
def teste_regle(nom_regle, cle, mot, pos_mot):

    logging.debug ('mot : '+mot+'['+str(pos_mot-1)+'] lettre : '+mot[pos_mot-1]+' regle : '+nom_regle)
    if hasattr(cle, '__call__'):
        #la regle est une fonction spécifique
        #logging.debug(nom_regle, ' fonction');
        return cle(mot, pos_mot)

    #exemples : '+':'n|m' ou '-':'[aeiou]'
    trouve_s = True
    trouve_p = True

    if '+' in cle.keys():
        logging.debug(nom_regle+ ' cle + testee : '+cle['+'])
        logging.debug (mot, pos_mot)
        #il faut lire les lettres qui suivent
        #recherche le modèle demandé au début de la suite du mot
        pattern = re.compile(cle['+'])
        res = pattern.match(mot, pos_mot)
        trouve_s = ((res != None) and (res.start() == pos_mot))
    
    if '-' in cle.keys():
        logging.debug(nom_regle+ ' cle - testee : '+cle['-']);
        trouve_p = False
        pattern = re.compile(cle['-'])
        #teste si la condition inclut le début du mot ou seulement les lettres qui précèdent
        if (cle['-'][0] == '^'):
            #le ^ signifie 'début de chaîne' et non 'tout sauf'
            if (len(cle['-']) == 1):
                #on vérifie que le début de mot est vide
                trouve_p = (pos_mot == 1)
            else:
                #le début du mot doit correspondre au pattern
                res = pattern.match(mot, 0, pos_mot)
                if (res != None):
                    trouve_p = (res.end()-res.start()+1 == pos_mot)
        else :
            k = pos_mot-2
            while ((k > -1) and (not trouve_p)):
                logging.debug (mot, k, pos_mot)
                #il faut lire les lettres qui précèdent
                #recherche le modèle demandé à la fin du début du mot
                res = pattern.match(mot, k, pos_mot)
                if (res != None):
                    #print (res.end(), res.start())
                    trouve_p = (res.end()-res.start()+1 == pos_mot-k)
                k -= 1

    return (trouve_p and trouve_s)

###################################################################################
# Décodage d'un mot sous la forme d'une suite de phonèmes
###################################################################################
def extraire_phonemes(mot, para=None, p_para=0):
    p_mot = 0
    codage = []
    if para is None:
        para = mot

    logging.info('--------------------'+mot+'--------------------')
    if mot in __dico_deco__.keys():
        if len(__dico_deco__[mot][0].strip()) > 0:
            """ Le mot est dans le dictionnaire et le décodage doit être fait en conséquence """
            smot = re.split('/', __dico_deco__[mot][0].strip())
            i = 0
            while p_mot < len(mot) and i < len(smot):
                lsmot = smot[i].split('.') # séparer graphème effectif et graphème correspondant au phonème souhaité
                phon = lsmot[0]
                if len(lsmot) > 1 and len(lsmot[1]) > 0:
                    phon = lsmot[1]
                try:
                    # est-ce que le phonème est codé en direct ?
                    phoneme = re.findall('\[(.*)\]', phon)
                    if len(phoneme) > 0:
                        # oui
                        try:
                            codage.append((sampa2lc[phoneme[0]],lsmot[0]))
                        except:
                            codage.append((phoneme[0],lsmot[0]))
                    else:
                        # non : on le décode à partir des lettres
                        phoneme = extraire_phonemes(phon)
                        if len(phoneme[0][0]) > 0:
                            codage.append((phoneme[0][0],lsmot[0]))
                        else:
                            codage.append((phon,lsmot[0]))

                except:
                    codage.append((phon,lsmot[0]))
                p_mot += len(lsmot[0])
                i += 1

    """ Le mot n'est dans le dictionnaire et le décodage est standard """
    while p_mot < len(mot):
        # On teste d'application des règles de composition des sons
        lettre = mot[p_mot]
        logging.debug ('lettre : '+lettre)

        trouve = False
        if lettre in autom:
            aut = autom[lettre][1]
            logging.debug (u('liste des règles : ')+str(aut))
            i = 0
            while (not trouve) and (i < len(autom[lettre][0])):
                k = autom[lettre][0][i]
                if teste_regle(k, aut[k][0], mot, p_mot+1):
                    phoneme = aut[k][1]
                    pas = aut[k][2]
                    codage.append((phoneme,para[p_para:p_para+pas]))
                    logging.info('phoneme:'+phoneme+' ; lettre(s) lue(s):'+para[p_para:p_para+pas])
                    p_mot += pas
                    p_para += pas
                    trouve = True
                i += 1
            logging.debug ('trouve:'+str(trouve)+' - '+str(codage))

            if (not trouve) and (p_mot == len(mot)-1) and ('@' in aut):
                if p_mot == len(mot)-1:
                    # c'est la dernière lettre du mot, il faut vérifier que ce n'est pas une lettre muette
                    phoneme = aut['@'][1]
                    pas = 1
                    codage.append((phoneme,lettre))
                    trouve = True
                    p_mot += 1
                    p_para += 1
                    logging.info('phoneme fin de mot:'+phoneme+' ; lettre lue:'+lettre)

            # rien trouvé donc on prend le phonème de base ('*')
            if not trouve:
                try:
                    phoneme = aut['*'][1]
                    pas = aut['*'][2]
                    codage.append((phoneme,para[p_para:p_para+pas]))
                    p_para += pas
                    p_mot += pas
                    logging.info('phoneme par defaut:'+phoneme+' ; lettre lue:'+lettre)
                except:
                    codage.append(('',lettre))
                    p_para += 1
                    p_mot += 1
                    logging.info('non phoneme ; caractere lu:'+lettre)
        else:
            codage.append(('',lettre))
            p_mot += 1
            p_para += 1
            logging.info('non phoneme ; caractere lu:'+lettre)

    logging.info('--------------------'+str(codage)+'--------------------')

    # post traitement pour associer yod + [an, in, en, on, a, é, etc.]
    codage = post_traitement_yod(codage)

    # post traitement pour différencier les o ouverts et les o fermés
    codage = post_traitement_o_ouvert_ferme(codage)

    # post traitement pour différencier les eu ouverts et les eu fermés
    codage = post_traitement_e_ouvert_ferme(codage)

    return codage

def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

###################################################################################
# Post traitement la constitution d'allophones des phonèmes avec yod
# référence : voir http://andre.thibault.pagesperso-orange.fr/PhonologieSemaine10.pdf (cours du 3 février 2016)
###################################################################################
def post_traitement_yod(pp):
    if not isinstance(pp, list) or len(pp) == 1:
        return pp

    phonemes = [x[0] for x in pp]
    if not 'j' in phonemes:
        # pas de 'yod' dans le mot
        return pp

    # recherche de tous les indices de phonèmes avec 'j'
    nb_ph = len(pp)-1
    i_j = all_indices('j', phonemes[:nb_ph+1])

    for i_ph in i_j:
        if i_ph >= nb_ph:
            # fin de mot (bizarre d'ailleurs !)
            return pp
        
        # phonème suivant
        phon_suivant = ['a', 'a~', 'e', 'e^', 'e_comp', 'e^_comp', 'o', 'o_comp', 'o~', 'e~', 'x', 'x^', 'u']
        if phonemes[i_ph+1] in phon_suivant and len(pp[i_ph][1]) == 1:
            pp[i_ph] = ('j_'+phonemes[i_ph+1], pp[i_ph][1]+pp[i_ph+1][1])
            if len(pp[i_ph+2:]) > 0:
                pp[i_ph+1:nb_ph] = pp[i_ph+2:nb_ph] # compactage de la chaîne de phonèmes
            else:
                del pp[nb_ph]
            nb_ph = len(pp)-1

    return pp

###################################################################################
# Post traitement pour déterminer si le son [o] est ouvert ou fermé
###################################################################################
def post_traitement_o_ouvert_ferme(pp):
    if not isinstance(pp, list) or len(pp) == 1:
        return pp

    phonemes = [x[0] for x in pp]
    if not 'o' in phonemes:
        # pas de 'o' dans le mot
        return pp

    # consonnes qui rendent possible un o ouvert en fin de mot
    consonnes_syllabe_fermee = ['p','k','b','d','g','f','f_ph','s^','l','r','m','n']

    # mots en 'osse' qui se prononcent avec un o ouvert
    mots_osse = [u('cabosse'), u('carabosse'), u('carrosse'), u('colosse'), u('molosse'), u('cosse'), u('crosse'), u('bosse'),
    u('brosse'), u('rhinocéros'), u('désosse'), u('fosse'), u('gosse'), u('molosse'), u('écosse'), u('rosse'), u('panosse')]

    # indice du dernier phonème prononcé
    nb_ph = len(phonemes)-1
    while nb_ph > 0 and phonemes[nb_ph] == "#":
        nb_ph -= 1

    # recherche de tous les indices de phonèmes avec 'o'
    i_o = all_indices('o', phonemes[:nb_ph+1])

    # reconstitution du mot sans les phonèmes muets à la fin
    mot = ''.join([x[1] for x in pp[:nb_ph+1]])

    if mot in mots_osse:
        # certains mots en 'osse' on un o ouvert
        i_ph_o = i_o[-1:][0]
        pp[i_ph_o] = ('o_ouvert', pp[i_ph_o][1])
        return pp

    for i_ph in i_o:
        if i_ph == nb_ph:
            # syllabe tonique ouverte (rien après ou phonème muet) en fin de mot : o fermé
            return pp

        if pp[i_ph][1] != u('ô'):
            if i_ph == nb_ph-2 and phonemes[i_ph+1] in consonnes_syllabe_fermee and phonemes[i_ph+2] == 'q_caduc':
                # syllabe tonique fermée (présence de consonne après) en fin de mot : o ouvert
                pp[i_ph] = ('o_ouvert', pp[i_ph][1])
            elif phonemes[i_ph+1] in ['r', 'z^_g', 'v']:
                # o ouvert lorsqu’il est suivi d’un [r] : or, cor, encore, dort, accord
                # o ouvert lorsqu’il est suivi d’un [z^_g] : loge, éloge, horloge
                # o ouvert lorsqu’il est suivi d’un [v] : ove, innove.
                pp[i_ph] = ('o_ouvert', pp[i_ph][1])
            elif (i_ph < nb_ph-2) and (phonemes[i_ph+1] in syllaphon['c']) and (phonemes[i_ph+2] in syllaphon['c']):
                # un o suivi de 2 consonnes est un o ouvert
                pp[i_ph] = ('o_ouvert', pp[i_ph][1])

    return pp

###################################################################################
# Post traitement pour déterminer si le son [e] est ouvert "e" ou fermé "eu"
###################################################################################
def post_traitement_e_ouvert_ferme(pp):
    if not isinstance(pp, list) or len(pp) == 1:
        return pp

    phonemes = [x[0] for x in pp]
    if not 'x' in phonemes:
        # pas de 'eu' dans le mot
        return pp

    # indice du dernier phonème prononcé
    nb_ph = len(phonemes)-1
    while nb_ph >= 1 and phonemes[nb_ph] == "#":
        nb_ph -= 1

    # recherche de tous les indices de phonèmes avec 'x' qui précèdent le dernier phonème prononcé
    i_x = all_indices('x', phonemes[:nb_ph+1])

    # on ne s'intéresse qu'au dernier phonème (pour les autres, on ne peut rien décider)
    i_ph = i_x[-1]

    if i_ph < nb_ph - 2:
        # le phonème n'est pas l'un des 3 derniers du mot : on ne peut rien décider
        return pp

    if i_ph == nb_ph:
        # le dernier phonème prononcé dans le mot est le 'eu' donc 'eu' fermé
        pp[i_ph] = ('x^', pp[i_ph][1])
        return pp

     # le phonème est l'avant dernier du mot (syllabe fermée)
    consonnes_son_eu_ferme = ['z','z_s','t']
    if phonemes[i_ph+1] in consonnes_son_eu_ferme and phonemes[nb_ph] == 'q_caduc':
        pp[i_ph] = ('x^', pp[i_ph][1])

    return pp

###################################################################################
# Recomposition des phonèmes en une suite de syllabes (utilitaire)
###################################################################################
def extraire_syllabes_util(phonemes, mode=(ConstLireCouleur.SYLLABES_LC, ConstLireCouleur.SYLLABES_ECRITES)):
    nb_phon = len(phonemes)
    if nb_phon < 2:
        return [range(nb_phon)], phonemes

    mot = ''.join([phonemes[i][1] for i in range(len(phonemes))])
    if mot in __dico_deco__.keys():
        if len(__dico_deco__[mot][1].strip()) > 0:
            """ Le mot est dans le dictionnaire et le décodage doit être fait en conséquence """
            smot = re.split('/', __dico_deco__[mot][1].strip())
            if ''.join(smot) == mot: # ultime vérification
                j = 0
                i = 0
                sylls = []
                while i < len(smot):
                    cur_syl = []
                    csyl = ''
                    while j < len(phonemes) and csyl != smot[i]:
                        cur_syl.append(j)
                        csyl = ''.join([phonemes[cur_syl[k]][1] for k in range(len(cur_syl))])
                        j += 1
                    # ajouter la syllabe à la liste
                    sylls.append(cur_syl)
                    i += 1

                # recomposer les syllabes avec les lettres
                lsylls = [''.join([phonemes[i][1] for i in sylls[j]]) for j in range(len(sylls))]

                # ménage
                del sylls

                logging.info('--------------------'+str(lsylls)+'--------------------')
                return lsylls, [ph for ph in phonemes]

    """ Le mot n'est dans le dictionnaire et le décodage est standard """
    nphonemes = []
    if mode[0] == ConstLireCouleur.SYLLABES_STD:
        # dupliquer les phonèmes qui comportent des consonnes doubles
        for i in range(nb_phon):
            phon = phonemes[i]
            if isinstance(phon, tuple):
                if (phon[0] in syllaphon['c'] or phon[0] in syllaphon['s']) and (len(phon[1]) > 1):
                    if phon[1][-1] == phon[1][-2]:
                        # consonne redoublée
                        nphonemes.append((phon[0], phon[1][:-1]))
                        nphonemes.append((phon[0], phon[1][-1]))
                    else:
                        nphonemes.append(phon)
                else:
                    nphonemes.append(phon)
            else:
                nphonemes.append(phon)
    else:
        nphonemes = [ph for ph in phonemes]
    nb_phon = len(nphonemes)

    logging.info('--------------------'+str(nphonemes)+'--------------------')
    # préparer la liste de syllabes
    sylph = []
    for i in range(nb_phon):
        phon = nphonemes[i]
        if isinstance(phon, tuple):
            if phon[0] in syllaphon['v']:
                sylph.append(('v',[i]))
            elif phon[0].startswith('j_') or phon[0].startswith('w_') or phon[0].startswith('y_'): # yod+voyelle, 'w'+voyelle, 'y'+voyelle sans diérèse
                sylph.append(('v',[i]))
            elif phon[0] in syllaphon['c']:
                sylph.append(('c',[i]))
            elif phon[0] in syllaphon['s']:
                sylph.append(('s',[i]))
            else:
                # c'est un phonème muet : '#'
                sylph.append(('#',[i]))

    # mixer les doubles phonèmes de consonnes qui incluent [l] et [r] ; ex. : bl, tr, cr, chr, pl
    i = 0
    while i < len(sylph)-1:
        if ((sylph[i][0] == 'c') and (sylph[i+1][0] == 'c')):
            # deux phonèmes consonnes se suivent
            phon0 = nphonemes[sylph[i][1][0]]
            phon1 = nphonemes[sylph[i+1][1][0]]
            if ((phon1[0] == 'l') or (phon1[0] == 'r')) and (phon0[0] in ['b','k','p','t','g','d','f','v']):
                # mixer les deux phonèmes puis raccourcir la chaîne
                sylph[i][1].extend(sylph[i+1][1])
                for j in range(i+1, len(sylph)-1):
                    sylph[j] = sylph[j+1]
                sylph.pop()
        i += 1
    logging.info(u("mixer doubles phonèmes consonnes (bl, tr, cr, etc.) :")+str(sylph))

    # mixer les doubles phonèmes [y] et [i], [u] et [i,e~,o~]
    i = 0
    while i < len(sylph)-1:
        if ((sylph[i][0] == 'v') and (sylph[i+1][0] == 'v')):
            # deux phonèmes voyelles se suivent
            phon1 = nphonemes[sylph[i][1][0]][0]
            phon2 = nphonemes[sylph[i+1][1][0]][0]
            if (phon1 == 'y' and phon2 == 'i') or (phon1 == 'u' and phon2 in ['i','e~','o~']):
                # mixer les deux phonèmes puis raccourcir la chaîne
                sylph[i][1].extend(sylph[i+1][1])
                for j in range(i+1, len(sylph)-1):
                    sylph[j] = sylph[j+1]
                sylph.pop()
        i += 1
    logging.info(u("mixer doubles phonèmes voyelles ([y] et [i], [u] et [i,e~,o~]) :")+str(sylph))

    # accrocher les lettres muettes aux lettres qui précèdent
    i = 0
    while i < len(sylph)-1:
        if sylph[i+1][0] == '#':
            # mixer les deux phonèmes puis raccourcir la chaîne
            sylph[i][1].extend(sylph[i+1][1])
            for j in range(i+1, len(sylph)-1):
                sylph[j] = sylph[j+1]
            sylph.pop()
        i += 1

    # construire les syllabes par association de phonèmes consonnes et voyelles
    sylls = []
    nb_sylph = len(sylph)
    i = j = 0
    while i < nb_sylph:
        # début de syllabe = tout ce qui n'est pas voyelle
        j = i
        while (i < nb_sylph) and (sylph[i][0] != 'v'):
            i += 1

        # inclure les voyelles
        if (i < nb_sylph) and (sylph[i][0] == 'v'):
            i += 1
            cur_syl = []
            for k in range(j,i):
                cur_syl.extend(sylph[k][1])
            j = i

            # ajouter la syllabe à la liste
            sylls.append(cur_syl)

        # la lettre qui suit est une consonne
        if i+1 < nb_sylph:
            lettre1 = nphonemes[sylph[i][1][-1]][1][-1]
            lettre2 = nphonemes[sylph[i+1][1][0]][1][0]
            if u('bcdfghjklmnpqrstvwxzç').find(lettre1) > -1 and u('bcdfghjklmnpqrstvwxzç').find(lettre2) > -1:
                # inclure cette consonne si elle est suivie d'une autre consonne
                cur_syl.extend(sylph[i][1])
                i += 1
                j = i

    # précaution de base : si pas de syllabes reconnues, on concatène simplement les phonèmes
    if len(sylls) == 0:
        return [range(nb_phon)], phonemes

    # il ne doit rester à la fin que les lettres muettes ou des consonnes qu'on ajoute à la dernière syllabe
    for k in range(j,nb_sylph):
        sylls[-1].extend(sylph[k][1])

    if mode[1] == ConstLireCouleur.SYLLABES_ORALES and len(sylls) > 1:
        # syllabes orales : si la dernière syllabe est finalisée par des lettres muettes ou un e caduc,
        # il faut la concaténer avec la syllabe précédente
        k = len(sylls[-1])-1
        while k > 0 and nphonemes[sylls[-1][k]][0] in ['#', 'verb_3p']:
            k -= 1
        if nphonemes[sylls[-1][k]][0] == 'q_caduc':
            # concaténer la dernière syllabe à l'avant-dernière
            sylls[-2].extend(sylls[-1])
            del sylls[-1]

    # ménage
    del sylph

    return sylls, nphonemes

###################################################################################
# Recomposition des phonèmes en une suite de syllabes
###################################################################################
def extraire_syllabes(phonemes, mode=(ConstLireCouleur.SYLLABES_LC, ConstLireCouleur.SYLLABES_ECRITES)):
    sylls, nphonemes = extraire_syllabes_util(phonemes, mode)

    # recomposer les syllabes avec les lettres
    lsylls = [''.join([nphonemes[i][1] for i in sylls[j]]) for j in range(len(sylls))]

    # ménage
    del sylls
    del nphonemes

    logging.info('--------------------'+str(lsylls)+'--------------------')
    return lsylls

###################################################################################
# Recherche une succession de phonèmes dans le mot traduit sous la forme de phonèmes
###################################################################################
def generer_masque_phonemes(phonemes, l_phon):
    mask = []
    if type(phonemes) == type(list):
        return mask

    i = 0
    nb_phon = len(phonemes)
    nb_l_phon = len(l_phon)
    while i < nb_phon:
        phon = phonemes[i][0].split('_')[0]
        if phon == l_phon[0]:
            j = 1
            k = i+1
            trouve = True
            while (k < nb_phon) and trouve and (j < nb_l_phon):
                phon = phonemes[k][0].split('_')[0]
                trouve = (phon == l_phon[j])
                j += 1
                k += 1
            if trouve and (j == nb_l_phon):
                # on est arrivé à la fin du pattern
                mask.extend([1 for u in range(nb_l_phon)])
                i += nb_l_phon
            else:
                # on n'a pas trouvé le pattern complet
                mask.append(0)
                i += 1
        else:
            mask.append(0)
            i += 1
    return mask


###################################################################################
# Recompose les phonèmes des mots d'un paragraphe en syllabes
###################################################################################
def generer_paragraphe_syllabes(pp, mode=(ConstLireCouleur.SYLLABES_LC, ConstLireCouleur.SYLLABES_ECRITES)):
    ps = []
    for umot in pp:
        if isinstance(umot, list):
            ps.append(extraire_syllabes(umot, mode))
        else:
            ps.append(umot)
    return ps

###################################################################################
# Recherche la succession de phonèmes demandée dans les mots du paragraphe
###################################################################################
def generer_masque_paragraphe_phonemes(pp, l_phon):
    pm = []
    for umot in pp:
        if isinstance(umot, list):
            pm.append(generer_masque_phonemes(umot, l_phon))
        else:
            pm.append([])
    return pm

###################################################################################
# Générateur d'un paragraphe de texte sous la forme de phonèmes
###################################################################################
def generer_paragraphe_phonemes(texte):
    """ Transformation d'un paragraphe en une liste de phonèmes """

    ##
    # Prétraitement
    ##
    ultexte = pretraitement_texte(texte)
    l_utexte = len(ultexte)
    mots = ultexte.split() # extraire les mots

    ##
    # Traitement
    ##
    pp = []
    p_texte = 0
    for umot in mots:
        # recherche de l'emplacement du nouveau mot à traiter
        pp_texte = ultexte.find(umot, p_texte)
        if pp_texte > p_texte:
            # ajoute au paragraphe la portion de texte non traitée (ponctuation, espaces...)
            pp.append(texte[p_texte:pp_texte])
        p_texte = pp_texte

        # décodage du mot en phonèmes
        phonemes = extraire_phonemes(umot, texte, p_texte)
        pp.append(phonemes)
        p_texte += len(umot)

    # ajouter le texte qui suit le dernier mot
    if p_texte < l_utexte:
        pp.append(texte[p_texte:])

    return pp

###################################################################################
# Teste s'il est ou non possible de faire une liaison vers ce mot
###################################################################################
def debut_mot_h_muet(mot):
    mots_h_muet = [u('habilet.'), u('habill.'), u('habit.'), u('haleine'), u('hallucination'),
    u('halt.re'), u('hebdomadaire'), u('hame.on'), u('harmonie'), u('héberge'), u('hébétude'), u('hécatombe'),
    u('hégémonie'), u('hémi.'), u('héritage'), u('herbe'), u('héréditaire'), u('hermine'),
    u('hermétique'), u('héroïne'), u('hésit.'), u('heure'), u('hippopotame'), u('hiver'), u('histoire'),
    u('homme'), u('hommage'), u('homonyme'), u('honn[ê|e]te'), u('honneur'), u('h[ô|o]tel'), u('h[ô|o]pita'),
    u('horizon'), u('horloge'),    u('horoscope'), u('horreur'), u('horripil.'), u('horticulteur'), u('hospice'),
    u('hostilité'), u('huile'), u('huissier'), u('hu[î|i]tre'), u('humanité'), u('humble'),
    u('humect.'), u('humeur'), u('humidité'), u('humus'), u('humili.'), u('hymne')]

    for pattern in mots_h_muet:
        if re.match(pattern, mot):
            return True
    return False

###################################################################################
# Teste s'il est ou non possible de faire une liaison vers ce mot
###################################################################################
def teste_liaison_vers_mot(mot):
    liaison_interdite = ['et', 'ou', 'onze', 'onzes', 'huit', 'huits']
    voyelles = u('^[aeiouyùüïîöôàèéêë]')

    if mot == "est-ce":
        return True
    if mot.find('-') >= 0: # risque d'inversion sujet verbe et liaison interdite ensuite
        return False
    if re.match(voyelles, mot[:1]) and not mot in liaison_interdite:
        return True
    return debut_mot_h_muet(mot)

###################################################################################
# Teste s'il y a ou non une liaison entre les 2 mots
###################################################################################
def teste_liaison(mot_prec, mot_suiv):
    determinants = ['un', u('qu@un'), 'des', 'les', 'cet', 'ces', 'mon', 'ton', 'son', 'mes', 'tes',
    'ses', 'nos', 'vos', 'leurs', 'aux', 'aucun', 'tout', 'quels', 'quelles', 'quelques',
    'deux', 'trois', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'vingt', 'cent',
    'cents', 'quel', 'quels', 'quelles', 'aucun', 'certains', 'quelques', 'toutes', 'aux']
    pronoms = ['on', 'nous', 'vous', 'ils', 'elles', 'on', 'chacun', 'autres', 'tous', 'nul',
    'certains', 'certaines', 'dont']
    verbe_etre = ['suis', 'es', 'est', 'sommes', u('êtes'), 'sont', u('étais'), u('était'), u('étaient'),
    u('étions'), u('étiez'), 'seras', 'serez', 'serons', 'seront', 'serais',
    'seriez', 'serions', 'fus', 'fut', u('fûmes'), u('fûtes'), 'furent', u('c@était'), 'c@est']
    adjectifs_anteposes = ['petit', 'petits', 'grand', 'grands', 'beaux', 'bel', 'belles', 'bon', 'bons', 'mal',
    'autres', 'braves', 'gros', 'grosses', 'jeunes', 'jolis', 'mauvais', 'mauvaises', u('mêmes'),
    'meilleur', 'meilleurs', 'meilleures', 'moindres', 'pires', 'vieux', 'vieil', 'vieilles']
    adverbes = [u('après'), 'hier', 'puis', 'soudain', u('tôt'), 'tard', 'toujours', 'souvent',
    'trop', u('très'), 'moins', 'plus', 'tant', 'tout', 'assez', 'bien', 'jamais', 'mieux', 'autant',
    'beaucoup']
    prepositions = ['par', 'pour', 'sans', 'avec', 'dans', 'sur', 'chez', 'durant', 'en', 'sous']
    divers = ['ont', 'faut', 'quant', 'quand', 'mais', 'donc', 'car']

    liaison_obligatoire = []
    for x in [determinants, pronoms, verbe_etre, adjectifs_anteposes, adverbes, prepositions, divers]:
        liaison_obligatoire.extend(x)

    liaison_interdite = ['tiens', 'pars', 'viens', 'vends', 'lis', 'dis', 'ris', 'perds', 'tonds', 'mets', u('allés')]

    if teste_liaison_vers_mot(mot_suiv):
        # mode aide où certaines liaisons obligatoires sont marquées
        if mot_prec in liaison_obligatoire:
            return True
        if mot_prec in verbe_etre:
            return True
        if mot_prec[-1] == 's' and not mot_prec in liaison_interdite and debut_mot_h_muet(mot_suiv):
            # liaison entre un mot a priori terminé par un 's' et un mot commenant par un h muet
            return True    

    return False

######################################################################################
#
######################################################################################
if __name__ == "__main__":
    loadLCDict('lirecouleur.dic')

    if len(sys.argv) == 3:
        print ('test de liaison')
        print (pretraitement_texte(u(sys.argv[1]))+ ' '+ pretraitement_texte(u(sys.argv[2]))+ ' : '+ str(teste_liaison(pretraitement_texte(u(sys.argv[1])), pretraitement_texte(u(sys.argv[2])))))
    else:
        for i in range(len(sys.argv)-1):
            message_test = u(sys.argv[i+1])
            print (u('test chaine de phonemes : ')+message_test)
            pp = generer_paragraphe_phonemes(message_test)
            print (message_test + ': '+ str(pp))
            print ('\n')
            print (u('test chaine de syllabes : ')+message_test)
            ps = generer_paragraphe_syllabes(pp)
            print (message_test + ': '+ str(ps))
            print ('\n')
            print (u('test chaine de syllabes orales : ')+message_test)
            ps = generer_paragraphe_syllabes(pp, (ConstLireCouleur.SYLLABES_LC, ConstLireCouleur.SYLLABES_ORALES))
            print (message_test + ': '+ str(ps))
            print ('\n')
            print (u('test chaine de syllabes ecrites : ')+message_test)
            ps = generer_paragraphe_syllabes(pp, (ConstLireCouleur.SYLLABES_STD, ConstLireCouleur.SYLLABES_ECRITES))
            print (message_test + ': '+ str(ps))
            print ('\n')
            print ('------------------------------')
