#!/usr/bin/env python
# -*- coding: UTF-8 -*-

###################################################################################
# Jeu de tests unitaires de LireCouleur. Les tests portent sur la génération de
# phonèmes et de syllabes. Chaque jeu de règle de lirecouleur.py fait l'objet
# d'un test de décodage en phonèmes. Le décodage en syllabes porte sur des mots
# réguliers et sur des mots irréguliers, avec vérification du décodage phonémique
# au préalable.
# 
# voir http://www.arkaline.fr/doku.php?id=logiciels:lirecouleur
#
# Copyright (c) 2014 by Marie-Pierre Brungard
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

import unittest
from lirecouleur import *

class TestSonsIsoles(unittest.TestCase):
	def setUp(self):
		self.voyelles = [[('a', 'a')], [('q', 'e')], [('i', 'i')], [('i', 'y')],
		[('o', 'o')], [('o_comp', 'au')], [('o_comp', 'eau')], [('y', 'u')], [('u', 'ou')],
		[('a~', 'en')], [('a~', 'an')], [('a~', 'am')], [('x~', 'un')],
		[('x~', 'um')], [('e~', 'in')], [('e~', 'im')], [('e', u('é'))], [('e_comp', 'er')],
		[('e_comp', 'ez')], [('e_comp', 'et')], [('e^', u('è'))], [('e^_comp', 'est')],
		[('e_comp', 'ai')], [('e^_comp', 'ei')], [('wa', 'oi')], [('w5', 'oin')]]
	
		self.consonnes = [[('b', 'b')], [('s_c', 'c')], [('d', 'd')], [('f', 'f')],
		[('g', 'g')], [('#', 'h')], [('i', 'i')], [('z^', 'j')], [('k', 'k')], [('l', 'l')],
		[('m', 'm')], [('n', 'n')], [('p', 'p')], [('k', 'q')], [('r', 'r')], [('s', 's')],
		[('t', 't')], [('v', 'v')], [('v', 'w')], [('#', 'x')], [('#', 'z')]]

	def test_sons_voyelles(self):
		nb_sons = len(self.voyelles)
		for i in range(nb_sons):
			son = self.voyelles[i][0][1]
			self.assertEqual(extraire_phonemes(son, son, 0), self.voyelles[i])

	def test_sons_consonnes(self):
		nb_sons = len(self.consonnes)
		for i in range(nb_sons):
			son = self.consonnes[i][0][1]
			self.assertEqual(extraire_phonemes(son, son, 0), self.consonnes[i])

class TestMotsRegleA(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('baye', [('b', 'b'), ('a', 'a'), ('j', 'y'), ('q_caduc', 'e')]),
		('cobaye', [('k', 'c'), ('o', 'o'), ('b', 'b'), ('a', 'a'), ('j', 'y'), ('q_caduc', 'e')]),
		('pays', [('p', 'p'), ('e^_comp', 'a'), ('i', 'y'), ('#', 's')]),
		('paysan', [('p', 'p'), ('e^_comp', 'a'), ('i', 'y'), ('z_s', 's'), ('a~', 'an')]),
		('paysanne', [('p', 'p'), ('e^_comp', 'a'), ('i', 'y'), ('z_s', 's'), ('a', 'a'), ('n', 'nn'), ('q_caduc', 'e')]),
		('taureau', [('t', 't'), ('o_comp', 'au'), ('r', 'r'), ('o_comp', 'eau')]),
		('ail', [('a', 'a'), ('j', 'il')]),
		('maille', [('m', 'm'), ('a', 'a'), ('j', 'ill'), ('q_caduc', 'e')]),
		('ainsi', [('e~', 'ain'), ('s', 's'), ('i', 'i')]),
		('capitaine', [('k', 'c'), ('a', 'a'), ('p', 'p'), ('i', 'i'), ('t', 't'), ('e^_comp', 'ai'), ('n', 'n'), ('q_caduc', 'e')]),
		('main', [('m', 'm'), ('e~', 'ain')]),
		('plaint', [('p', 'p'), ('l', 'l'), ('e~', 'ain'), ('#', 't')]),
		('vaincu', [('v', 'v'), ('e~', 'ain'), ('k', 'c'), ('y', 'u')]),
		('salade', [('s', 's'), ('a', 'a'), ('l', 'l'), ('a', 'a'), ('d', 'd'), ('q_caduc', 'e')]),
		('appât', [('a', 'a'), ('p', 'pp'), ('a', 'â'), ('#', 't')]),
		('déjà', [('d', 'd'), ('e', 'é'), ('z^', 'j'), ('a', 'à')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleB(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('bébé', [('b', 'b'), ('e', 'é'), ('b', 'b'), ('e', 'é')]),
		('rabbin', [('r', 'r'), ('a', 'a'), ('b', 'bb'), ('e~', 'in')]),
		('plomb', [('p', 'p'), ('l', 'l'), ('o~', 'om'), ('#', 'b')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleC(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('ce', [('s_c', 'c'), ('q', 'e')]),
		('ci', [('s_c', 'c'), ('i', 'i')]),
		('cygne', [('s_c', 'c'), ('i', 'y'), ('n~', 'gn'), ('q_caduc', 'e')]),
		('choeur', [('k', 'ch'), ('x', 'oeu'), ('r', 'r')]),
		('chorale', [('k', 'ch'), ('o_ouvert', 'o'), ('r', 'r'), ('a', 'a'), ('l', 'l'), ('q_caduc', 'e')]),
		('psychologue', [('p', 'p'), ('s', 's'), ('i', 'y'), ('k', 'ch'), ('o', 'o'), ('l', 'l'), ('o', 'o'), ('g_u', 'gu'), ('q_caduc', 'e')]),
		('brachiosaure', [('b', 'b'), ('r', 'r'), ('a', 'a'), ('k', 'ch'), ('j', 'i'), ('o', 'o'), ('z_s', 's'), ('o_comp', 'au'), ('r', 'r'), ('q_caduc', 'e')]),
		('chiroptère', [('k', 'ch'), ('i', 'i'), ('r', 'r'), ('o_ouvert', 'o'), ('p', 'p'), ('t', 't'), ('e^', 'è'), ('r', 'r'), ('q_caduc', 'e')]),
		('chrétien', [('k', 'ch'), ('r', 'r'), ('e', 'é'), ('t', 't'), ('j', 'i'), ('e~', 'en')]),
		('synchroniser', [('s', 's'), ('e~', 'yn'), ('k', 'ch'), ('r', 'r'), ('o', 'o'), ('n', 'n'), ('i', 'i'), ('z_s', 's'), ('e_comp', 'er')]),
		('chat', [('s^', 'ch'), ('a', 'a'), ('#', 't')]),
		('tabac', [('t', 't'), ('a', 'a'), ('b', 'b'), ('a', 'a'), ('#', 'c')]),
		('donc', [('d', 'd'), ('o~', 'on'), ('k', 'c')]),
		('blanc',  [('b', 'b'), ('l', 'l'), ('a~', 'an'), ('#', 'c')]),
		('tronc', [('t', 't'), ('r', 'r'), ('o~', 'on'), ('#', 'c')]),
		('bac', [('b', 'b'), ('a', 'a'), ('k', 'c')]),
		('maçon', [('m', 'm'), ('a', 'a'), ('s', 'ç'), ('o~', 'on')]),
		('archéologie', [('a', 'a'), ('r', 'r'), ('k', 'ch'), ('e', 'é'), ('o', 'o'), ('l', 'l'), ('o_ouvert', 'o'), ('z^_g', 'g'), ('i', 'i'), ('#', 'e')]),
		('chlorure', [('k', 'ch'), ('l', 'l'), ('o_ouvert', 'o'), ('r', 'r'), ('y', 'u'), ('r', 'r'), ('q_caduc', 'e')]),
		('orchestre', [('o_ouvert', 'o'), ('r', 'r'), ('k', 'ch'), ('e^_comp', 'e'), ('s', 's'), ('t', 't'), ('r', 'r'), ('q_caduc', 'e')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleD(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('rade', [('r', 'r'), ('a', 'a'), ('d', 'd'), ('q_caduc', 'e')]),
		('fond', [('f', 'f'), ('o~', 'on'), ('#', 'd')]),
		('retard', [('r', 'r'), ('q', 'e'), ('t', 't'), ('a', 'a'), ('r', 'r'), ('#', 'd')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleE(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('serpent', [('s', 's'), ('e^_comp', 'e'), ('r', 'r'), ('p', 'p'), ('a~', 'en'), ('#', 't')]),
		('apparemment', [('a', 'a'), ('p', 'pp'), ('a', 'a'), ('r', 'r'), ('a', 'e'), ('m', 'mm'), ('a~', 'en'), ('#', 't')]),
		('aiment', [('e^_comp', 'ai'), ('m', 'm'), ('q_caduc', 'e'), ('verb_3p', 'nt')]),
		('batiment', [('b', 'b'), ('a', 'a'), ('t', 't'), ('i', 'i'), ('m', 'm'), ('a~', 'en'), ('#', 't')]),
		('aimaient', [('e^_comp', 'ai'), ('m', 'm'), ('e^_comp', 'ai'), ('verb_3p', 'ent')]),
		('clef', [('k', 'c'), ('l', 'l'), ('e_comp', 'ef')]),
		('hier', [('#', 'h'), ('j', 'i'), ('e^_comp', 'e'), ('r', 'r')]),
		('femme', [('f', 'f'), ('a', 'e'), ('m', 'mm'), ('q_caduc', 'e')]),
		('lemme', [('l', 'l'), ('e^_comp', 'e'), ('m', 'mm'), ('q_caduc', 'e')]),
		('emmener', [('a~', 'em'), ('m', 'm'), ('q', 'e'), ('n', 'n'), ('e_comp', 'er')]),
		('copient', [('k', 'c'), ('o', 'o'), ('p', 'p'), ('i', 'i'), ('#', 'ent')]),
		('chien', [('s^', 'ch'), ('j', 'i'), ('e~', 'en')]),
		('aimez', [('e^_comp', 'ai'), ('m', 'm'), ('e_comp', 'ez')]),
		('aimer', [('e^_comp', 'ai'), ('m', 'm'), ('e_comp', 'er')]),
		('pied', [('p', 'p'), ('j', 'i'), ('e_comp', 'ed')]),
		('pique', [('p', 'p'), ('i', 'i'), ('k_qu', 'qu'), ('q_caduc', 'e')]),
		('figue', [('f', 'f'), ('i', 'i'), ('g_u', 'gu'), ('q_caduc', 'e')]),
		('je', [('z^', 'j'), ('q', 'e')]),
		('mes', [('m', 'm'), ('e_comp', 'es')]),
		('rein', [('r', 'r'), ('e~', 'ein')]),
		('eu', [('y', 'eu')]),
		('monsieur', [('m', 'm'), ('q', 'on'), ('s', 's'), ('j', 'i'), ('x^', 'eu'), ('#', 'r')]),
		('jeudi', [('z^', 'j'), ('x^', 'eu'), ('d', 'd'), ('i', 'i')]),
		('jeune', [('z^', 'j'), ('x', 'eu'), ('n', 'n'), ('q_caduc', 'e')]),
		('leur', [('l', 'l'), ('x', 'eu'), ('r', 'r')]),
		('eux', [('x^', 'eu'), ('#', 'x')]),
		('est', [('e^_comp', 'est')]),
		('et', [('e_comp', 'et')]),
		('soleil', [('s', 's'), ('o', 'o'), ('l', 'l'), ('e^_comp', 'e'), ('j', 'il')]),
		('geyser', [('z^_g', 'g'), ('e^_comp', 'ey'), ('z_s', 's'), ('e^_comp', 'e'), ('r', 'r')]),
		('miel', [('m', 'm'), ('j', 'i'), ('e^_comp', 'e'), ('l', 'l')]),
		('sec', [('s', 's'), ('e^_comp', 'e'), ('k', 'c')]),
		('ennemi', [('e^_comp', 'e'), ('n', 'nn'), ('q', 'e'), ('m', 'm'), ('i', 'i')]),
		('ennui', [('a~', 'en'), ('n', 'n'), ('y', 'u'), ('i', 'i')]),
		('escargot', [('e^_comp', 'e'), ('s', 's'), ('k', 'c'), ('a', 'a'), ('r', 'r'), ('g', 'g'), ('o', 'o'), ('#', 't')]),
		('abbaye', [('a', 'a'), ('b', 'bb'), ('e^_comp', 'a'), ('i', 'y'), ('#', 'e')]),
		('que', [('k_qu', 'qu'), ('q', 'e')]),
		('geai', [('z^_g', 'g'), ('#', 'e'), ('e^_comp', 'ai')]),
		('jean', [('z^', 'j'), ('#', 'e'), ('a~', 'an')]),
		('asseoir', [('a', 'a'), ('s', 'ss'), ('#', 'e'), ('wa', 'oi'), ('r', 'r')]),
		('correcte', [('k', 'c'), ('o_ouvert', 'o'), ('r', 'rr'), ('e^_comp', 'e'), ('k', 'c'), ('t', 't'), ('q_caduc', 'e')]),
		('aster', [('a', 'a'), ('s', 's'), ('t', 't'), ('e^_comp', 'e'), ('r', 'r')]),
		('cher', [('s^', 'ch'), ('e^_comp', 'e'), ('r', 'r')]),
		('coréen', [('k', 'c'), ('o_ouvert', 'o'), ('r', 'r'), ('e', 'é'), ('e~', 'en')]),
		('lycéen', [('l', 'l'), ('i', 'y'), ('s_c', 'c'), ('e', 'é'), ('e~', 'en')]),
		('examen', [('e^', 'e'), ('gz', 'x'), ('a', 'a'), ('m', 'm'), ('e~', 'en')]),
		('golem', [('g', 'g'), ('o', 'o'), ('l', 'l'), ('e^_comp', 'e'), ('m', 'm')]),
		('cet', [('s_c', 'c'), ('e^_comp', 'e'), ('t', 't')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleG(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('gagner', [('g', 'g'), ('a', 'a'), ('n~', 'gn'), ('e_comp', 'er')]),
		('gamme', [('g', 'g'), ('a', 'a'), ('m', 'mm'), ('q_caduc', 'e')]),
		('gomme', [('g', 'g'), ('o_ouvert', 'o'), ('m', 'mm'), ('q_caduc', 'e')]),
		('gypse', [('z^_g', 'g'), ('i', 'y'), ('p', 'p'), ('s', 's'), ('q_caduc', 'e')]),
		('geste', [('z^_g', 'g'), ('e^_comp', 'e'), ('s', 's'), ('t', 't'), ('q_caduc', 'e')]),
		('poing', [('p', 'p'), ('w5', 'oin'), ('#', 'g')]),
		('doigt', [('d', 'd'), ('wa', 'oi'), ('#', 'g'), ('#', 't')]),
		('gourd', [('g', 'g'), ('u', 'ou'), ('r', 'r'), ('#', 'd')]),
		('sang', [('s', 's'), ('a~', 'an'), ('#', 'g')]),
		('long', [('l', 'l'), ('o~', 'on'), ('#', 'g')]),
		('hareng', [('#', 'h'), ('a', 'a'), ('r', 'r'), ('a~', 'en'), ('#', 'g')]),
		('aiguille', [('e^_comp', 'ai'), ('g', 'g'), ('y', 'u'), ('i', 'i'), ('j', 'll'), ('q_caduc', 'e')]),
		('argument', [('a', 'a'), ('r', 'r'), ('g', 'g'), ('y', 'u'), ('m', 'm'), ('a~', 'en'), ('#', 't')]),
		('vingt', [('v', 'v'), ('e~', 'in'), ('#', 'g'), ('t', 't')]),
		('vague', [('v', 'v'), ('a', 'a'), ('g_u', 'gu'), ('q_caduc', 'e')]),
		('grog', [('g', 'g'), ('r', 'r'), ('o', 'o'), ('g', 'g')]),
		('parking', [('p', 'p'), ('a', 'a'), ('r', 'r'), ('k', 'k'), ('i', 'i'), ('g~', 'ng')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleH(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('hibou', [('#', 'h'), ('i', 'i'), ('b', 'b'), ('u', 'ou')]),
		('thé', [('t', 't'), ('#', 'h'), ('e', 'é')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleI(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('ding', [('d', 'd'), ('i', 'i'), ('g~', 'ng')]),
		('lin', [('l', 'l'), ('e~', 'in')]),
		('imbiber', [('e~', 'im'), ('b', 'b'), ('i', 'i'), ('b', 'b'), ('e_comp', 'er')]),
		('illumina', [('i', 'i'), ('l', 'll'), ('y', 'u'), ('m', 'm'), ('i', 'i'), ('n', 'n'), ('a', 'a')]),
		('ville', [('v', 'v'), ('i', 'i'), ('l', 'll'), ('q_caduc', 'e')]),
		('mille', [('m', 'm'), ('i', 'i'), ('l', 'll'), ('q_caduc', 'e')]),
		('fille', [('f', 'f'), ('i', 'i'), ('j', 'll'), ('q_caduc', 'e')]),
		('tranquille', [('t', 't'), ('r', 'r'), ('a~', 'an'), ('k_qu', 'qu'), ('i', 'i'), ('l', 'll'), ('q_caduc', 'e')]),
		('appuient', [('a', 'a'), ('p', 'pp'), ('y', 'u'), ('i', 'i'), ('#', 'ent')]),
		('confient', [('k', 'c'), ('o~', 'on'), ('f', 'f'), ('i', 'i'), ('#', 'ent')]),
		('copier', [('k', 'c'), ('o', 'o'), ('p', 'p'), ('j', 'i'), ('e_comp', 'er')]),
		('pion', [('p', 'p'), ('j', 'i'), ('o~', 'on')]),
		('chien', [('s^', 'ch'), ('j', 'i'), ('e~', 'en')]),
		('cyan', [('s_c', 'c'), ('j', 'y'), ('a~', 'an')]),
		('criant', [('k', 'c'), ('r', 'r'), ('j', 'i'), ('a~', 'an'), ('#', 't')]),
		('maïs', [('m', 'm'), ('a', 'a'), ('i', 'ï'), ('#', 's')]),
		('mistigri', [('m', 'm'), ('i', 'i'), ('s', 's'), ('t', 't'), ('i', 'i'), ('g', 'g'), ('r', 'r'), ('i', 'i')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleJ(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('joujou', [('z^', 'j'), ('u', 'ou'), ('z^', 'j'), ('u', 'ou')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleK(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('kaki', [('k', 'k'), ('a', 'a'), ('k', 'k'), ('i', 'i')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleL(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('il', [('i', 'i'), ('l', 'l')]),
		('fusil', [('f', 'f'), ('y', 'u'), ('z_s', 's'), ('i', 'i'), ('#', 'l')]),
		('outil', [('u', 'ou'), ('t', 't'), ('i', 'i'), ('#', 'l')]),
		('gentil', [('z^_g', 'g'), ('a~', 'en'), ('t', 't'), ('i', 'i'), ('#', 'l')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleM(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('somme', [('s', 's'), ('o_ouvert', 'o'), ('m', 'mm'), ('q_caduc', 'e')]),
		('automne', [('o_comp', 'au'), ('t', 't'), ('o', 'o'), ('#', 'm'), ('n', 'n'), ('q_caduc', 'e')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleN(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('tonne', [('t', 't'), ('o_ouvert', 'o'), ('n', 'nn'), ('q_caduc', 'e')]),
		('lent', [('l', 'l'), ('a~', 'en'), ('#', 't')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleO(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('coin', [('k', 'c'), ('w5', 'oin')]),
		('roi', [('r', 'r'), ('wa', 'oi')]),
		('clou', [('k', 'c'), ('l', 'l'), ('u', 'ou')]),
		('clown', [('k', 'c'), ('l', 'l'), ('u', 'ow'), ('n', 'n')]),
		('bon', [('b', 'b'), ('o~', 'on')]),
		('zoo', [('z', 'z'), ('o', 'oo')]),
		('coefficient', [('k', 'c'), ('o', 'o'), ('e^_comp', 'e'), ('f', 'ff'), ('i', 'i'), ('s_c', 'c'), ('j', 'i'), ('a~', 'en'), ('#', 't')]),
		('moelle', [('m', 'm'), ('wa', 'oe'), ('l', 'll'), ('q_caduc', 'e')]),
		('foetus', [('f', 'f'), ('e', 'oe'), ('t', 't'), ('y', 'u'), ('#', 's')]),
		('oeil', [('x', 'oe'), ('j', 'il')]),
		('homme', [('#', 'h'), ('o_ouvert', 'o'), ('m', 'mm'), ('q_caduc', 'e')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleP(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('papa', [('p', 'p'), ('a', 'a'), ('p', 'p'), ('a', 'a')]),
		('alpha', [('a', 'a'), ('l', 'l'), ('f_ph', 'ph'), ('a', 'a')]),
		('loup', [('l', 'l'), ('u', 'ou'), ('#', 'p')]),
		('camp', [('k', 'c'), ('a~', 'am'), ('#', 'p')]),
		('drap', [('d', 'd'), ('r', 'r'), ('a', 'a'), ('#', 'p')]),
		('trop', [('t', 't'), ('r', 'r'), ('o', 'o'), ('#', 'p')]),
		('sirop', [('s', 's'), ('i', 'i'), ('r', 'r'), ('o', 'o'), ('#', 'p')]),
		('salop', [('s', 's'), ('a', 'a'), ('l', 'l'), ('o', 'o'), ('#', 'p')]),
		('corps', [('k', 'c'), ('o_ouvert', 'o'), ('r', 'r'), ('#', 'p'), ('#', 's')]),
		('compte', [('k', 'c'), ('o~', 'om'), ('#', 'p'), ('t', 't'), ('q_caduc', 'e')]),
		('piqure', [('p', 'p'), ('i', 'i'), ('k', 'q'), ('y', 'u'), ('r', 'r'), ('q_caduc', 'e')]),
		('baptise', [('b', 'b'), ('a', 'a'), ('#', 'p'), ('t', 't'), ('i', 'i'), ('z_s', 's'), ('q_caduc', 'e')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleQ(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('quitte', [('k_qu', 'qu'), ('i', 'i'), ('t', 'tt'), ('q_caduc', 'e')]),
		('coq', [('k', 'c'), ('o', 'o'), ('k', 'q')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleR(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('monsieur', [('m', 'm'), ('q', 'on'), ('s', 's'), ('j', 'i'), ('x^', 'eu'), ('#', 'r')]),
		('messieurs', [('m', 'm'), ('e^_comp', 'e'), ('s', 'ss'), ('j', 'i'), ('x^', 'eu'), ('#', 'r'), ('#', 's')]),
		('gars', [('g', 'g'), ('a', 'a'), ('#', 'rs')]),
		('gare', [('g', 'g'), ('a', 'a'), ('r', 'r'), ('q_caduc', 'e')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleS(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('mars', [('m', 'm'), ('a', 'a'), ('r', 'r'), ('s', 's')]),
		('os', [('o', 'o'), ('s', 's')]),
		('bus', [('b', 'b'), ('y', 'u'), ('s', 's')]),
		('parasol', [('p', 'p'), ('a', 'a'), ('r', 'r'), ('a', 'a'), ('s', 's'), ('o', 'o'), ('l', 'l')]),
		('parasite', [('p', 'p'), ('a', 'a'), ('r', 'r'), ('a', 'a'), ('z_s', 's'), ('i', 'i'), ('t', 't'), ('q_caduc', 'e')]),
		('atlas', [('a', 'a'), ('t', 't'), ('l', 'l'), ('a', 'a'), ('s', 's')]),
		('bis', [('b', 'b'), ('i', 'i'), ('s', 's')]),
		('bise', [('b', 'b'), ('i', 'i'), ('z_s', 's'), ('q_caduc', 'e')]),
		('basse', [('b', 'b'), ('a', 'a'), ('s', 'ss'), ('q_caduc', 'e')]),
		('chats', [('s^', 'ch'), ('a', 'a'), ('#', 't'), ('#', 's')]),
		('schlem', [('s^', 'sch'), ('l', 'l'), ('e^_comp', 'e'), ('m', 'm')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleT(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('titi', [('t', 't'), ('i', 'i'), ('t', 't'), ('i', 'i')]),
		('soutien', [('s', 's'), ('u', 'ou'), ('t', 't'), ('j', 'i'), ('e~', 'en')]),
		('martien', [('m', 'm'), ('a', 'a'), ('r', 'r'), ('s_t', 't'), ('j', 'i'), ('e~', 'en')]),
		('soulocratie', [('s', 's'), ('u', 'ou'), ('l', 'l'), ('o_ouvert', 'o'), ('k', 'c'), ('r', 'r'), ('a', 'a'), ('s_t', 't'), ('i', 'i'), ('#', 'e')]),
		('vingt', [('v', 'v'), ('e~', 'in'), ('#', 'g'), ('t', 't')]),
		('addition', [('a', 'a'), ('d', 'dd'), ('i', 'i'), ('s_t', 't'), ('j', 'i'), ('o~', 'on')]),
		('yaourt', [('j', 'y'), ('a', 'a'), ('u', 'ou'), ('r', 'r'), ('t', 't')]),
		('test', [('t', 't'), ('e^_comp', 'e'), ('s', 's'), ('t', 't')]),
		('marrant', [('m', 'm'), ('a', 'a'), ('r', 'rr'), ('a~', 'an'), ('#', 't')]),
		('instinct', [('e~', 'in'), ('s', 's'), ('t', 't'), ('e~', 'in'), ('#', 'c'), ('#', 't')]),
		('succinct', [('s', 's'), ('y', 'u'), ('k', 'c'), ('s_c', 'c'), ('e~', 'in'), ('#', 'c'), ('#', 't')]),
		('respect', [('r', 'r'), ('e^_comp', 'e'), ('s', 's'), ('p', 'p'), ('e^_comp', 'e'), ('#', 'c'), ('#', 't')]),
		('aspect', [('a', 'a'), ('s', 's'), ('p', 'p'), ('e^_comp', 'e'), ('#', 'c'), ('#', 't')]),
		('tact', [('t', 't'), ('a', 'a'), ('k', 'c'), ('t', 't')]),
		('direct', [('d', 'd'), ('i', 'i'), ('r', 'r'), ('e^_comp', 'e'), ('k', 'c'), ('t', 't')]),
		('infect', [('e~', 'in'), ('f', 'f'), ('e^_comp', 'e'), ('k', 'c'), ('t', 't')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleU(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('commun', [('k', 'c'), ('o', 'o'), ('m', 'mm'), ('x~', 'un')]),
		('cercueil', [('s_c', 'c'), ('e^_comp', 'e'), ('r', 'r'), ('k', 'c'), ('x', 'ue'), ('j', 'il')]),
		('maximum', [('m', 'm'), ('a', 'a'), ('ks', 'x'), ('i', 'i'), ('m', 'm'), ('o', 'u'), ('m', 'm')]),
		('parfum', [('p', 'p'), ('a', 'a'), ('r', 'r'), ('f', 'f'), ('x~', 'um')]),
		('boum', [('b', 'b'), ('u', 'ou'), ('m', 'm')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleV(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('vélo', [('v', 'v'), ('e', 'é'), ('l', 'l'), ('o', 'o')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleW(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('wagon', [('v', 'w'), ('a', 'a'), ('g', 'g'), ('o~', 'on')]),
		('kiwi', [('k', 'k'), ('i', 'i'), ('w', 'w'), ('i', 'i')]),
		('wapiti', [('w', 'w'), ('a', 'a'), ('p', 'p'), ('i', 'i'), ('t', 't'), ('i', 'i')]),
		('sandwich', [('s', 's'), ('a~', 'an'), ('d', 'd'), ('w', 'w'), ('i', 'i'), ('s^', 'ch')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleX(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('six', [('s', 's'), ('i', 'i'), ('s_x', 'x')]),
		('dix', [('d', 'd'), ('i', 'i'), ('s_x', 'x')]),
		('axe', [('a', 'a'), ('ks', 'x'), ('q_caduc', 'e')]),
		('fixer', [('f', 'f'), ('i', 'i'), ('ks', 'x'), ('e_comp', 'er')]),
		('boxe', [('b', 'b'), ('o', 'o'), ('ks', 'x'), ('q_caduc', 'e')]),
		('xavier', [('gz', 'x'), ('a', 'a'), ('v', 'v'), ('j', 'i'), ('e_comp', 'er')]),
		('exigu', [('e^', 'e'), ('gz', 'x'), ('i', 'i'), ('g_u', 'gu')]),
		('exact', [('e^', 'e'), ('gz', 'x'), ('a', 'a'), ('k', 'c'), ('t', 't')]),
		('hexagone', [('#', 'h'), ('e^', 'e'), ('gz', 'x'), ('a', 'a'), ('g', 'g'), ('o_ouvert', 'o'), ('n', 'n'), ('q_caduc', 'e')]),
		('coexister', [('k', 'c'), ('o', 'o'), ('e^', 'e'), ('gz', 'x'), ('i', 'i'), ('s', 's'), ('t', 't'), ('e_comp', 'er')]),
		('inexact', [('i', 'i'), ('n', 'n'), ('e^', 'e'), ('gz', 'x'), ('a', 'a'), ('k', 'c'), ('t', 't')]),
		('réexamen', [('r', 'r'), ('e', 'é'), ('e^', 'e'), ('gz', 'x'), ('a', 'a'), ('m', 'm'), ('e~', 'en')]),
		('préexister', [('p', 'p'), ('r', 'r'), ('e', 'é'), ('e^', 'e'), ('gz', 'x'), ('i', 'i'), ('s', 's'), ('t', 't'), ('e_comp', 'er')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleY(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('abbaye', [('a', 'a'), ('b', 'bb'), ('e^_comp', 'a'), ('i', 'y'), ('#', 'e')]),
		('voyage', [('v', 'v'), ('wa', 'o'), ('j', 'y'), ('a', 'a'), ('z^_g', 'g'), ('q_caduc', 'e')]),
		('pays', [('p', 'p'), ('e^_comp', 'a'), ('i', 'y'), ('#', 's')]),
		('synchroniser', [('s', 's'), ('e~', 'yn'), ('k', 'ch'), ('r', 'r'), ('o', 'o'), ('n', 'n'), ('i', 'i'), ('z_s', 's'), ('e_comp', 'er')]),
		('gymnaste', [('z^_g', 'g'), ('i', 'y'), ('m', 'm'), ('n', 'n'), ('a', 'a'), ('s', 's'), ('t', 't'), ('q_caduc', 'e')]),
		('lyncher', [('l', 'l'), ('e~', 'yn'), ('s^', 'ch'), ('e_comp', 'er')]),
		('dynamo', [('d', 'd'), ('i', 'y'), ('n', 'n'), ('a', 'a'), ('m', 'm'), ('o', 'o')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestMotsRegleZ(unittest.TestCase):
	def setUp(self):
		self.mots = [
		('zozoter', [('z', 'z'), ('o', 'o'), ('z', 'z'), ('o', 'o'), ('t', 't'), ('e_comp', 'er')])
		]

	def test_mots(self):
		nb_mots = len(self.mots)
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots[i][0])
			# contrôle de l'extraction de phonèmes
			self.assertEqual(extraire_phonemes(mot, mot, 0), [(phon[0], u(phon[1])) for phon in self.mots[i][1]])

class TestSyllabesMots1(unittest.TestCase):
	def setUp(self):
		self.mots_phonemes = [
		('caisse', [('k', 'c'), ('e^_comp', 'ai'), ('s', 'ss'), ('q_caduc', 'e')]),
		('nul', [('n', 'n'), ('y', 'u'), ('l', 'l')]),
		('muscle', [('m', 'm'), ('y', 'u'), ('s', 's'), ('k', 'c'), ('l', 'l'), ('q_caduc', 'e')]),
		('pair', [('p', 'p'), ('e^_comp', 'ai'), ('r', 'r')]),
		('onze', [('o~', 'on'), ('z', 'z'), ('q_caduc', 'e')]),
		('force', [('f', 'f'), ('o_ouvert', 'o'), ('r', 'r'), ('s_c', 'c'), ('q_caduc', 'e')]),
		('couvée', [('k', 'c'), ('u', 'ou'), ('v', 'v'), ('e', 'é'), ('#', 'e')]),
		('friser', [('f', 'f'), ('r', 'r'), ('i', 'i'), ('z_s', 's'), ('e_comp', 'er')]),
		('éponge', [('e', 'é'), ('p', 'p'), ('o~', 'on'), ('z^_g', 'g'), ('q_caduc', 'e')]),
		('talon', [('t', 't'), ('a', 'a'), ('l', 'l'), ('o~', 'on')]),
		('copieur', [('k', 'c'), ('o', 'o'), ('p', 'p'), ('j', 'i'), ('x', 'eu'), ('r', 'r')]),
		('adresse', [('a', 'a'), ('d', 'd'), ('r', 'r'), ('e^_comp', 'e'), ('s', 'ss'), ('q_caduc', 'e')]),
		('abri', [('a', 'a'), ('b', 'b'), ('r', 'r'), ('i', 'i')]),
		('matin', [('m', 'm'), ('a', 'a'), ('t', 't'), ('e~', 'in')]),
		('fumer', [('f', 'f'), ('y', 'u'), ('m', 'm'), ('e_comp', 'er')]),
		('appel', [('a', 'a'), ('p', 'pp'), ('e^_comp', 'e'), ('l', 'l')]),
		('soleil', [('s', 's'), ('o', 'o'), ('l', 'l'), ('e^_comp', 'e'), ('j', 'il')]),
		('meilleur', [('m', 'm'), ('e^_comp', 'e'), ('j', 'ill'), ('x', 'eu'), ('r', 'r')]),
		('approche', [('a', 'a'), ('p', 'pp'), ('r', 'r'), ('o_ouvert', 'o'), ('s^', 'ch'), ('q_caduc', 'e')]),
		('sonnerie', [('s', 's'), ('o', 'o'), ('n', 'nn'), ('q', 'e'), ('r', 'r'), ('i', 'i'), ('#', 'e')]),
		('avenue', [('a', 'a'), ('v', 'v'), ('q', 'e'), ('n', 'n'), ('y', 'u'), ('#', 'e')]),
		('explosion', [('e^', 'e'), ('ks', 'x'), ('p', 'p'), ('l', 'l'), ('o', 'o'), ('z_s', 's'), ('j', 'i'), ('o~', 'on')]),
		('piloter', [('p', 'p'), ('i', 'i'), ('l', 'l'), ('o', 'o'), ('t', 't'), ('e_comp', 'er')]),
		('rétablir', [('r', 'r'), ('e', 'é'), ('t', 't'), ('a', 'a'), ('b', 'b'), ('l', 'l'), ('i', 'i'), ('r', 'r')])
		]

		self.mots_syllabes = [
		('caisse', ['cai', 'sse']),
		('nul', ['nul']),
		('muscle', ['mus', 'cle']),
		('pair', ['pair']),
		('onze', ['on', 'ze']),
		('force', ['for', 'ce']),
		('couvée', ['cou', 'vée']),
		('friser', ['fri', 'ser']),
		('éponge', ['é', 'pon', 'ge']),
		('talon', ['ta', 'lon']),
		('copieur', ['co', 'pieur']),
		('adresse', ['a', 'dre', 'sse']),
		('abri', ['a', 'bri']),
		('matin', ['ma', 'tin']),
		('fumer', ['fu', 'mer']),
		('appel', ['a', 'ppel']),
		('soleil', ['so', 'leil']),
		('meilleur', ['me', 'illeur']),
		('approche', ['a', 'ppro', 'che']),
		('sonnerie', ['so', 'nne', 'rie']),
		('avenue', ['a', 've', 'nue']),
		('explosion', ['ex', 'plo', 'sion']),
		('piloter', ['pi', 'lo', 'ter']),
		('rétablir', ['ré', 'ta', 'blir'])
		]

	def test_mots(self):
		nb_mots = len(self.mots_syllabes)
		self.assertEqual(nb_mots, len(self.mots_phonemes))
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots_syllabes[i][0])
			# contrôle de type de chaîne
			self.assertEqual(mot, u(self.mots_syllabes[i][0]))
			# contrôle de l'extraction de phonèmes
			pp = extraire_phonemes(mot, mot, 0)
			self.assertEqual(pp, [(phon[0], u(phon[1])) for phon in self.mots_phonemes[i][1]])
			# contrôler ensuite le décodage en syllabes
			self.assertEqual(extraire_syllabes(pp), [u(syll) for syll in self.mots_syllabes[i][1]])

class TestSyllabesMots2(unittest.TestCase):
	def setUp(self):
		self.mots_phonemes = [
		('cassis', [('k', 'c'), ('a', 'a'), ('s', 'ss'), ('i', 'i'), ('#', 's')]),
		('net', [('n', 'n'), ('e^_comp', 'et')]),
		('faisan', [('f', 'f'), ('e^_comp', 'ai'), ('z_s', 's'), ('a~', 'an')]),
		('moelle', [('m', 'm'), ('wa', 'oe'), ('l', 'll'), ('q_caduc', 'e')]),
		('aiguille', [('e^_comp', 'ai'), ('g', 'g'), ('y', 'u'), ('i', 'i'), ('j', 'll'), ('q_caduc', 'e')]),
		('porc', [('p', 'p'), ('o_ouvert', 'o'), ('r', 'r'), ('#', 'c')]),
		('tabac', [('t', 't'), ('a', 'a'), ('b', 'b'), ('a', 'a'), ('#', 'c')]),
		('ours', [('u', 'ou'), ('r', 'r'), ('s', 's')]),
		('chorale', [('k', 'ch'), ('o_ouvert', 'o'), ('r', 'r'), ('a', 'a'), ('l', 'l'), ('q_caduc', 'e')]),
		('femme', [('f', 'f'), ('a', 'e'), ('m', 'mm'), ('q_caduc', 'e')]),
		('oignon', [('o', 'oi'), ('n~', 'gn'), ('o~', 'on')]),
		('écho', [('e', 'é'), ('s^', 'ch'), ('o', 'o')]),
		('automne', [('o_comp', 'au'), ('t', 't'), ('o', 'o'), ('#', 'm'), ('n', 'n'), ('q_caduc', 'e')]),
		('mille', [('m', 'm'), ('i', 'i'), ('l', 'll'), ('q_caduc', 'e')]),
		('septième', [('s', 's'), ('e^_comp', 'e'), ('p', 'p'), ('t', 't'), ('j', 'i'), ('e^', 'è'), ('m', 'm'), ('q_caduc', 'e')]),
		('fusil', [('f', 'f'), ('y', 'u'), ('z_s', 's'), ('i', 'i'), ('#', 'l')]),
		('orchestre', [('o_ouvert', 'o'), ('r', 'r'), ('k', 'ch'), ('e^_comp', 'e'), ('s', 's'), ('t', 't'), ('r', 'r'), ('q_caduc', 'e')]),
		('hiver', [('#', 'h'), ('i', 'i'), ('v', 'v'), ('e_comp', 'er')]),
		('examen', [('e^', 'e'), ('gz', 'x'), ('a', 'a'), ('m', 'm'), ('e~', 'en')]),
		('second', [('s', 's'), ('q', 'e'), ('k', 'c'), ('o~', 'on'), ('#', 'd')]),
		('parasol', [('p', 'p'), ('a', 'a'), ('r', 'r'), ('a', 'a'), ('s', 's'), ('o', 'o'), ('l', 'l')]),
		('monsieur', [('m', 'm'), ('q', 'on'), ('s', 's'), ('j', 'i'), ('x^', 'eu'), ('#', 'r')]),
		('révolver', [('r', 'r'), ('e', 'é'), ('v', 'v'), ('o_ouvert', 'o'), ('l', 'l'), ('v', 'v'), ('e^_comp', 'e'), ('r', 'r')])
		]

		self.mots_syllabes = [
		('cassis', ['ca', 'ssis']),
		('net', ['net']),
		('faisan', ['fai', 'san']),
		('moelle', ['moe', 'lle']),
		('aiguille', ['ai', 'gui', 'lle']),
		('porc', ['porc']),
		('tabac', ['ta', 'bac']),
		('ours', ['ours']),
		('chorale', ['cho', 'ra', 'le']),
		('femme', ['fe', 'mme']),
		('oignon', ['oi', 'gnon']),
		('écho', ['é', 'cho']),
		('automne', ['au', 'tom', 'ne']),
		('mille', ['mi', 'lle']),
		('septième', ['sep', 'tiè', 'me']),
		('fusil', ['fu', 'sil']),
		('orchestre', ['or', 'ches', 'tre']),
		('hiver', ['hi', 'ver']),
		('examen', ['e', 'xa', 'men']),
		('second', ['se', 'cond']),
		('parasol', ['pa', 'ra', 'sol']),
		('monsieur', ['mon', 'sieur']),
		('révolver', ['ré', 'vol', 'ver'])
		]

	def test_mots(self):
		nb_mots = len(self.mots_syllabes)
		self.assertEqual(nb_mots, len(self.mots_phonemes))
		for i in range(nb_mots):
			mot = pretraitement_texte(self.mots_syllabes[i][0])
			# contrôle de type de chaîne
			self.assertEqual(mot, u(self.mots_syllabes[i][0]))
			# contrôle de l'extraction de phonèmes
			pp = extraire_phonemes(mot, mot, 0)
			self.assertEqual(pp, [(phon[0], u(phon[1])) for phon in self.mots_phonemes[i][1]])
			# contrôler ensuite le décodage en syllabes
			self.assertEqual(extraire_syllabes(pp), [u(syll) for syll in self.mots_syllabes[i][1]])

if __name__ == "__main__":
	unittest.main()
