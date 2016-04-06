/*
 * lirecouleur.js est le moteur de décodage d'un texte en phonèmes et en syllabes.
 * Ce module fait partie du projet LireCouleur - http://lirecouleur.arkaline.fr
 * 
 * @author Marie-Pierre Brungard
 * @version 0.2
 * @since 2016
 *
 * GNU General Public Licence (GPL) version 3
 *
 * LireCouleur is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation; either version 3 of the License, or (at your option) any later
 * version.
 * LireCouleur is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 * You should have received a copy of the GNU General Public License along with
 * LireCouleur; if not, write to the Free Software Foundation, Inc., 59 Temple
 * Place, Suite 330, Boston, MA  02111-1307  USA4z
 */

/*
 * Élimine les caractères accentués et les remplace par des non accentués
 */
function chaine_sans_accent(str) {
	var TabSpec = {"à":"a","á":"a","â":"a","ã":"a","ä":"a","å":"a","ò":"o","ó":"o","ô":"o","õ":"o","ö":"o","ø":"o","è":"e","é":"e","ê":"e","ë":"e","ç":"c","ì":"i","í":"i","î":"i","ï":"i","ù":"u","ú":"u","û":"u","ü":"u","ÿ":"y","ñ":"n"}; 
 
	var reg=/[àáäâèéêëçìíîïòóôõöøùúûüÿñ_-]/i; 
	return str.replace(reg, function(){ return TabSpec[arguments[0].toLowerCase()]; }).toLowerCase();
}

/*
 * Clone un tableau
 */
function clone_tableau(tab) {
	return tab.slice(0);
};

/*
 * Correspondance entre le code SAMPA et le code LireCouleur
 * référence : http://fr.wikipedia.org/wiki/Symboles_SAMPA_fran%C3%A7ais
 */
var sampa2lc = {'p':'p', 'b':'b', 't':'t', 'd':'d', 'k':'k', 'g':'g', 'f':'f', 'v':'v',
's':'s', 'z':'z', 'S':'s^', 'Z':'g^', 'j':'j', 'm':'m', 'n':'n', 'J':'g~',
'N':'n~', 'l':'l', 'R':'r', 'w':'wa', 'H':'y', 'i':'i', 'e':'e', 'E':'e^',
'a':'a', 'A':'a', 'o':'o', 'O':'o_ouvert', 'u':'u', 'y':'y', '2':'x^', '9':'x',
'@':'q', 'e~':'e~', 'a~':'a~', 'o~':'o~', '9~':'x~', '#':'#'};

/********************************************************************************************************
 ********************************************************************************************************
 *
 *	Cette partie du code est destinée au traitement des textes pour en extraires des
 *	phonèmes et des syllabes.
 *
 ********************************************************************************************************
 ********************************************************************************************************/
/*
 * Les phonèmes sont codés en voyelles (v), consonnes (c) et semi-voyelles (s)
 */
var syllaphon = {
	'v':['a','q','q_caduc','i','o','o_comp','o_ouvert','u','y','e','e_comp','e^',
	'e^_comp','a~','e~','x~','o~','x','x^','wa', 'w5'],
	'c':['p','t','k','b','d','g','f','f_ph','s','s^','v','z','z^','l','r','m','n',
	'k_qu','z^_g','g_u','s_c','s_t','z_s','ks','gz'],
	's':['j','g~','n~','w'],
	'#':['#','verb_3p']
};

/*
 * Code un phonème
 */
function LCPhoneme(phon, lett) {
	this.phoneme = phon;
	this.lettres = lett;
}

LCPhoneme.prototype.estPhoneme = function() {
	return (this.phoneme !== null);
}

LCPhoneme.prototype.estUneConsonne = function() {
	return (syllaphon['c'].indexOf(this.phoneme) > -1);
}

LCPhoneme.prototype.estUneVoyelle = function() {
	return (syllaphon['v'].indexOf(this.phoneme) > -1);
}

LCPhoneme.prototype.estSemiConsonne = function() {
	return (syllaphon['s'].indexOf(this.phoneme) > -1);
}

LCPhoneme.prototype.estPhonemeMuet = function() {
	return (syllaphon['#'].indexOf(this.phoneme) > -1);
}

LCPhoneme.prototype.estSemiVoyelle = function() {
	return this.estSemiConsonne();
}

LCPhoneme.prototype.estConsonneRedoublee = function() {
	return (this.estPhoneme() && (this.estUneConsonne() || this.estSemiConsonne()) && (this.lettres.length == 2) && (this.lettres[0] == this.lettres[1]));
}

LCPhoneme.prototype.dedoublerConsonnes = function() {
	this.lettres = this.lettres[0];
}

/*
 * Code une syllabe
 */
function LCSyllabe() {
	this.phonemes = new Array();
}

LCSyllabe.prototype.ajoutePhonemes = function(a, phon) {
	var moi = this;
	if (typeof(phon) === "undefined") {
		a.forEach(function(element, index, array) {
			moi.phonemes.push(element);
		});
	}
	else {
		if (a instanceof Array) {
			a.forEach(function(element, index, array) {
				moi.phonemes.push(phon[element]);
			});
		}
		else {
			this.phonemes.push(phon[a]);
		}
	}
}

LCSyllabe.prototype.texte = function(e, muet) {
	var l = "";

	if (typeof(muet) === "undefined") {
		this.phonemes.forEach(function(element, index, array) {
			if (element.estPhonemeMuet()) {
				var em = document.createElement("span");
				em.setAttribute("class", "_lc_l_muettes");
				em.appendChild(document.createTextNode(element.lettres));
				e.appendChild(em);
			}
			else {
				e.appendChild(document.createTextNode(element.lettres));
			}
		});
	} else {
		this.phonemes.forEach(function(element, index, array) {
			if (element.estPhonemeMuet()) {
				var em = document.createElement("span");
				em.style = muet;
				em.appendChild(document.createTextNode(element.lettres));
				e.appendChild(em);
			}
			else {
				e.appendChild(document.createTextNode(element.lettres));
			}
		});
	}
	return e;
}

/*
 * Alphabet phonétique ascii : voir http://www.icp.inpg.fr/ICP/avtts/phon.fr.html
 * Outil inestimable : http://www.lexique.org/moteur
 */

function LireCouleurEngine() {
	/*
	 * Ensemble des règles d'extraction des phonèmes
	 * '*' signifie 'suivi par n'importe quelle lettre
	 * '@' signifie 'dernière lettre du mot
	 *
	 * format de l'automate:
	 *		'lettre': [[règles l'ordre où elles doivent être déclenchées],[liste des règles]]
	 *
	 * 	ATTENTION. Il faut faire attention à l'ordre de précédence des règles. Plusieurs règles peuvent
	 *	en effet s'appliquer pour une même succession de lettres. Il faut ranger les règles de la plus
	 *	spécifique à la plus générale.
	 *
	 * format d'une règle :
	 *		'nom_de_la_regle': [motif, phoneme, pas]
	 *
	 *	motif : il s'agit d'une expression régulière qui sert à tester les successions de lettres qui suivent
	 *		la lettre en cours de traitement dans le mot et les successions de lettres qui précèdent la lettre
	 *		en cours de traitement.
	 *	phoneme : le nom du phonème codé selon le format ascii décrit dans
	 *		http://www.icp.inpg.fr/ICP/avtts/phon.fr.html
	 *	pas : le nombre de lettres à lire à partir de la lettre courante si le motif a été reconnu
	 *		dans le mot de part et d'autre de la lettre en cours de traitement.
	 */
	this.MESTESSESLESDESCES = {'':'e_comp','fr':'e_comp','fr_CA':'e^_comp'};
	this.autom = {
		'a' : [['u','il','in','nc_ai_fin','ai_fin','i','n','m','nm','y_except','y'],
				{'n':[{'+':/n[bcçdfgjklmpqrstvwxz]/i},'a~',2],
				'm':[{'+':/m[bcçdfgjklpqrstvwxz]/i},'a~',2], // toute consonne sauf le n
				'nm':[{'+':/[nm]$/i},'a~',2],
				'y_except':[{'-':/(^b|cob|cip)/i,'+':/y/i},'a',1], // exception : baye, cobaye
				'y':[{'+':/y/i},'e^_comp',1],
				'u':[{'+':/u/i},'o_comp',2],
				'il':[{'+':/il($|l)/i},'a',1],
				'in':[{'+':/i[nm]([bcçdfghjklnmpqrstvwxz]|$)/i},'e~',3], // toute succession 'ain' 'aim' suivie d'une consonne ou d'une fin de mot
				'nc_ai_fin':[this.regle_nc_ai_final,'e^_comp',2],
				'ai_fin':[{'+':/i$/i},'e_comp',2],
				'i':[{'+':/[iî]/i},'e^_comp',2],
				'*':[{},'a',1]}],
		'â' : [[],
				{'*':[{},'a',1]}],
		'à' : [[],
				{'*':[{},'a',1]}],
		'b' : [['b','plomb'],
				{'b':[{'+':/b/i},'b',2],
				'plomb':[{'-':/plom/i,'+':/(s?)$/i},'#',1], // le "b" à la fin de plomb ne se prononce pas
				'*':[{},'b',1]}],
		'c' : [['eiy','choeur_1','choeur_2','chor','psycho','brachio','cheo','chest','chiro','chlo_chlam','chr',
				'h','erc_orc','cisole','c_muet_fin','onc_donc','nc_muet_fin','_spect','_inct','cciey','cc','apostrophe'],
				{'choeur_1':[{'+':/hoe/i},'k',2],
				'choeur_2':[{'+':/hœ/i},'k',2],
				'chor':[{'+':/hor/i},'k',2], // tous les "choral, choriste"... exceptions non traitées : chorizo, maillechort
				'psycho':[{'-':/psy/i,'+':/ho/i},'k',2], // tous les "psycho" quelque chose
				'brachio':[{'-':/bra/i,'+':/hio/i},'k',2], // brachiosaure, brachiocéphale
				'cheo':[{'+':/héo/i},'k',2], // archéo..., trachéo...
				'chest':[{'+':/hest/i},'k',2], // orchestre et les mots de la même famille
				'chiro':[{'+':/hiro[p|m]/i},'k',2], // chiroptère, chiromancie
				'chlo_chlam':[{'+':/hl(o|am)/i},'k',2], // chlorure, chlamyde
				'chr':[{'+':/hr/i},'k',2], // de chrétien à synchronisé
				'h':[{'+':/h/i},'s^',2],
				'eiy':[{'+':/[eiyéèêëîï]/i},'s_c',1],
				'cisole':[{'+':/$/i,'-':/^/i},'s_c',1], // exemple : c'est
				'erc_orc':[{'-':/[e|o]r/i,'+':/(s?)$/i},'#',1], // clerc, porc,
				'c_muet_fin':[{'-':/taba|accro/i,'+':/(s?)$/i},'#',1], // exceptions traitées : tabac, accroc
				'onc_donc':[{'-':/^on|^don/i},'k',1], // non exceptions traitées : onc, donc
				'nc_muet_fin':[{'-':/n/i,'+':/(s?)$/i},'#',1], // exceptions traitées : tous les mots terminés par *nc
				'_spect':[{'-':/spe/i,'+':/t(s?)$/i},'#',1], // respect, suspect, aspect
				'_inct':[{'-':/in/i,'+':/t(s?)$/i},'#',1], // instinct, succinct, distinct
				'cciey':[{'+':/c[eiyéèêëîï]/i},'k',1], // accident, accepter, coccyx
				'cc':[{'+':/c/i},'k',2], // accorder, accompagner
				'apostrophe':[{'+':/(\'|\’)/i},'s',2], // apostrophe
				'*':[{},'k',1], '@':['','k',1]}],
	 // + tous les *nc sauf "onc" et "donc"
		'ç' : [[],
				{'*':[{},'s',1]}],
		'd' : [['d','aujourdhui','disole','dmuet','apostrophe'],
				{'d':[{'+':/d/i},'d',2],
				'aujourdhui':[{'-':/aujour/i},'d',1], // aujourd'hui
				'disole':[{'+':/$/i,'-':/^/i},'d',1], // exemple : d'abord
				'dmuet':[{'+':/(s?)$/i},'#',1], // un d suivi éventuellement d'un s ex. : retards
				'apostrophe':[{'+':/(\'|\’)/i},'d',2], // apostrophe
				'*':[{},'d',1]}],
		'e' : [['conj_v_ier','uient','ien','een','except_en','_ent','clef','hier','adv_emment_fin',
				'ment','imparfait','verbe_3_pluriel','au',
				'avoir','monsieur','jeudi','jeu_','eur','eu','eu_accent_circ','in','eil','y','iy','ennemi','enn_debut_mot','dessus_dessous',
				'et','cet','t_final','eclm_final','est','drz_final','n','adv_emment_a','femme','lemme','em_gene','nm','tclesmesdes',
				'que_isole','que_gue_final','jtcnslemede','jean','ge','eoi','ex','reqquechose','2consonnes','abbaye','e_muet','e_caduc','e_deb'],
				{'_ent':[this.regle_mots_ent,'a~',2], // quelques mots (adverbes ou noms) terminés par ent
				'adv_emment_fin':[{'-':/emm/i,'+':/nt/i},'a~',2], // adverbe avec 'emment' => se termine par le son [a~]
				'ment':[this.regle_ment,'a~',2], // on considère que les mots terminés par 'ment' se prononcent [a~] sauf s'il s'agit d'un verbe
				'imparfait':[{'-':/ai/i,'+':/nt$/i},'verb_3p',3], // imparfait à la 3ème personne du pluriel
				'verbe_3_pluriel':[{'+':/nt$/i},'q_caduc',1], // normalement, pratiquement tout le temps verbe à la 3eme personne du pluriel
				'clef':[{'-':/cl/i,'+':/f/i},'e_comp',2], // une clef
				'hier':[this.regle_er,'e^_comp',1], // encore des exceptions avec les mots terminés par 'er' prononcés 'R'
				'n':[{'+':/n[bcdfghjklmpqrstvwxzç]/i},'a~',2],
				'adv_emment_a':[{'+':/mment/i},'a',1], // adverbe avec 'emment' => son [a]
				'eclm_final':[{'+':/[clm](s?)$/i},'e^_comp',1], // donne le son [e^] et le l ou le c se prononcent (ex. : miel, sec)
				'femme':[{'-':/f/i,'+':/mm/i},'a',1], // femme et ses dérivés => son [a]
				'lemme':[{'-':/l/i,'+':/mm/i},'e^_comp',1], // lemme et ses dérivés => son [e^]
				'em_gene':[{'+':/m[bcçdfghjklmnpqrstvwxz]/i},'a~',2], // 'em' cas général => son [a~]
				'uient':[{'-':/ui/i,'+':/nt$/i},'#',3], // enfuient, appuient, fuient, ennuient, essuient
				'conj_v_ier':[this.regle_ient,'#',3], // verbe du 1er groupe terminé par 'ier' conjugué à la 3ème pers du pluriel
				'except_en':[{'-':/exam|mino|édu/i,'+':/n(s?)$/i},'e~',2], // exceptions des mots où le 'en' final se prononce [e~] (héritage latin)
				'een':[{'-':/é/i,'+':/n(s?)$/i},'e~',2], // les mots qui se terminent par 'éen'
				'ien':[{'-':/[bdlmrstvh]i/i,'+':/n([bcçdfghjklpqrstvwxz]|$)/i},'e~',2], // certains mots avec 'ien' => son [e~]
				'nm':[{'+':/[nm]$/i},'a~',2],
				'drz_final':[{'+':/[drz](s?)$/i},'e_comp',2], // e suivi d'un d,r ou z en fin de mot done le son [e]
				'que_isole':[{'-':/^qu/i,'+':/$/i},'q',1], // que isolé
				'que_gue_final':[{'-':/[gq]u/i,'+':/(s?)$/i},'q_caduc',1], // que ou gue final
				'jtcnslemede':[{'-':/^[jtcnslmd]/i,'+':/$/i},'q',1], // je, te, me, le, se, de, ne
				'tclesmesdes':[{'-':/^[tcslmd]/i,'+':/s$/i},'e_comp', 2], // mes, tes, ces, ses, les
				'in':[{'+':/i[nm]([bcçdfghjklnmpqrstvwxz]|$)/i},'e~',3], // toute succession 'ein' 'eim' suivie d'une consonne ou d'une fin de mot
				'avoir':[this.regle_avoir,'y',2],
				'monsieur':[{'-':/si/i,'+':/ur/i},'x^',2],
				'jeudi':[{'-':/j/i,'+':/udi/i},'x^',2], // jeudi
				'jeu_':[{'-':/j/i,'+':/u/i},'x',2], // tous les "jeu*" sauf jeudi
				'eur':[{'+':/ur/i},'x',2],
				'eu':[{'+':/u/i},'x',2],
				'eu_accent_circ':[{'+':/û/i},'x^',2],
				'est':[{'-':/^/i,'+':/st$/i},'e^_comp',3],
				'et':[{'-':/^/i,'+':/t$/i},'e_comp',2],
				'eil':[{'+':/il/i},'e^_comp',1],
				'y':[{'+':/y[aeiouéèêààäôâ]/i},'e^_comp',1],
				'iy':[{'+':/[iy]/i},'e^_comp',2],
				'cet':[{'-':/^c/i,'+':/[t]$/i},'e^_comp',1], // 'cet'
				't_final':[{'+':/[t]$/i},'e^_comp',2], // donne le son [e^] et le t ne se prononce pas
				'au':[{'+':/au/i},'o_comp',3],
				'ennemi':[{'-':/^/i,'+':/nnemi/i},'e^_comp',1], // ennemi est l'exception ou 'enn' en début de mot se prononce 'èn' (cf. enn_debut_mot)
				'enn_debut_mot':[{'-':/^/i,'+':/nn/i},'a~',2], // 'enn' en début de mot se prononce 'en'
				'ex':[{'+':/x/i},'e^',1], // e suivi d'un x se prononce è
				'reqquechose':[{'-':/r/i,'+':/[bcçdfghjklmnpqrstvwxz](h|l|r)/i},'q',1], // re-quelque chose : le e se prononce 'e'
				'dessus_dessous':[{'-':/d/i,'+':/ss(o?)us/i},'q',1], // dessus, dessous : 'e' = e
				'2consonnes':[{'+':/[bcçdfghjklmnpqrstvwxz]{2}/i},'e^_comp',1], // e suivi de 2 consonnes se prononce è
				'e_deb':[{'-':/^/i},'q',1], // par défaut, un 'e' en début de mot se prononce [q]
				'abbaye':[{'-':/abbay/i,'+':/(s?)$/i},'#',1], // ben oui...
				'e_muet':[{'-':/[aeiouéèêà]/i,'+':/(s?)$/i},'#',1], // un e suivi éventuellement d'un 's' et précédé d'une voyelle ou d'un 'g' ex. : pie, geai
				'jean':[{'-':/j/i,'+':/an/i},'#',1], // jean
				'ge':[{'-':/g/i,'+':/[aouàäôâ]/i},'#',1], // un e précédé d'un 'g' et suivi d'une voyelle ex. : cageot
				'eoi':[{'+':/oi/i},'#',1], // un e suivi de 'oi' ex. : asseoir
				'e_caduc':[{'-':/[bcçdfghjklmnpqrstvwxzy]/i,'+':/(s?)$/i},'q_caduc',1], // un e suivi éventuellement d'un 's' et précédé d'une consonne ex. : correctes
				'*':[{},'q',1],
				'@':['','q_caduc',1]
				}],
		'é' : [[],
				{'*':[{},'e',1]}],
		'è' : [[],
				{'*':[{},'e^',1]}],
		'ê' : [[],
				{'*':[{},'e^',1]}],
		'ë' : [[],
				{'*':[{},'e^',1]}],
		'f' : [['f','oeufs'],
				{'f':[{'+':/f/i},'f',2],
				 'oeufs':[{'-':/(oeu|œu)/i,'+':/s/i},'#',1], // oeufs et boeufs
				 '*':[{},'f',1]}],
		'g' : [['g','ao','eiy','aiguille','u_consonne','u','n','vingt','g_muet_oin',
				'g_muet_our','g_muet_an','g_muet_fin'],
				{'g':[{'+':/g/i},'g',2],
				'n':[{'+':/n/i},'n~',2],
				'ao':[{'+':/a|o/i},'g',1],
				'eiy':[{'+':/[eéèêëïiy]/i},'z^_g',1], // un 'g' suivi de e,i,y se prononce [z^]
				'g_muet_oin':[{'-':/oi(n?)/i},'#',1], // un 'g' précédé de 'oin' ou de 'oi' ne se prononce pas ; ex. : poing, doigt
				'g_muet_our':[{'-':/ou(r)/i},'#',1], // un 'g' précédé de 'our' ou de 'ou(' ne se prononce pas ; ex. : bourg
				'g_muet_an':[{'-':/(s|^ét|^r)an/i,'+':/(s?)$/i},'#',1], // sang, rang, étang
				'g_muet_fin':[{'-':/lon|haren/i},'#',1], // pour traiter les exceptions : long, hareng
				'aiguille':[{'-':/ai/i,'+':/u/i},'g',1], // encore une exception : aiguille et ses dérivés
				'vingt':[{'-':/vin/i,'+':/t/i},'#',1], // vingt
				'u_consonne':[{'+':/u[bcçdfghjklmnpqrstvwxz]/i},'g',1], // gu suivi d'une consonne se prononce [g][y]
				'u':[{'+':/u/i},'g_u',2],
				'*':[{},'g',1]}],
		'h' : [[],
				{'*':[{},'#',1]}],
		'i' : [['ing','n','m','nm','lldeb','vill','mill','tranquille',
				'ill','@ill','@il','ll','ui','ient_1','ient_2','ie','i_voyelle'],
				{'ing':[{'-':/[bcçdfghjklmnpqrstvwxz]/i,'+':/ng$/i},'i',1],
				'n':[{'+':/n[bcçdfghjklmpqrstvwxz]/i},'e~',2],
				'm':[{'+':/m[bcçdfghjklnpqrstvwxz]/i},'e~',2],
				'nm':[{'+':/[n|m]$/i},'e~',2],
				'lldeb':[{'-':/^/i,'+':/ll/i},'i',1],
				'vill':[{'-':/v/i,'+':/ll/i},'i',1],
				'mill':[{'-':/m/i,'+':/ll/i},'i',1],
				'tranquille':[{'-':/tranqu/i,'+':/ll/i},'i',1],
				'ill':[{'+':/ll/i,'-':/[bcçdfghjklmnpqrstvwxz](u?)/i},'i',1], // précédé éventuellement d'un u et d'une consonne, donne le son [i]
				'@ill':[{'-':/[aeo]/i,'+':/ll/i},'j',3], // par défaut précédé d'une voyelle et suivi de 'll' donne le son [j]
				'@il':[{'-':/[aeou]/i,'+':/l(s?)$/i},'j',2], // par défaut précédé d'une voyelle et suivi de 'l' donne le son [j]
				'll':[{'+':/ll/i},'j',3], // par défaut avec ll donne le son [j]
				'ui':[{'-':/u/i,'+':/ent/i},'i',1], // essuient, appuient
				'ient_1':[this.regle_ient,'i',1], // règle spécifique pour différencier les verbes du premier groupe 3ème pers pluriel
				'ient_2':[{'+':/ent(s)?$/i},'j',1], // si la règle précédente ne fonctionne pas
				'ie':[{'+':/e(s|nt)?$/i},'i',1], // mots terminés par -ie(s|nt)
				'i_voyelle':[{'+':/[aäâeéèêëoôöuù]/i},'j',1], // i suivi d'une voyelle donne [j]
				'*':[{},'i',1]}],
		'ï' : [[],
				{'*':[{},'i',1]}],
		'î' : [[],
				{'*':[{},'i',1]}],
		'j' : [[],
				{'*':[{},'z^',1]}],
		'k' : [[],
				{'*':[{},'k',1]}],
		'l' : [['vill','mill','tranquille','illdeb','ill','eil','ll','excep_il', 'apostrophe','lisole'],
				{'vill':[{'-':/^vi/i,'+':/l/i},'l',2], // ville, village etc. => son [l]
				'mill':[{'-':/^mi/i,'+':/l/i},'l',2], // mille, million, etc. => son [l]
				'tranquille':[{'-':/tranqui/i,'+':/l/i},'l',2], // tranquille => son [l]
				'illdeb':[{'-':/^i/i,'+':/l/i},'l',2], // 'ill' en début de mot = son [l] ; exemple : illustration
				'lisole':[{'+':/$/i,'-':/^/i},'l',1], // exemple : l'animal
				'ill':[{'-':/.i/i,'+':/l/i},'j',2], // par défaut, 'ill' donne le son [j]
				'll':[{'+':/l/i},'l',2], // à défaut de l'application d'une autre règle, 'll' donne le son [l]
				'excep_il':[{'-':/fusi|outi|genti/i,'+':/(s?)$/i},'#',1], // les exceptions trouvées ou le 'l' à la fin ne se prononce pas : fusil, gentil, outil
				'eil':[{'-':/e(u?)i/i},'j',1], // les mots terminés en 'eil' ou 'ueil' => son [j]
				'apostrophe':[{'+':/(\'|\’)/i},'l',2], // apostrophe
				'*':[{},'l',1]}],
		'm' : [['m','tomn','misole','apostrophe'],
				{'m':[{'+':/m/i},'m',2],
				'tomn':[{'-':/to/i,'+':/n/i},'#',1], // regle spécifique pour 'automne' et ses dérivés
				'*':[{},'m',1],
				'misole':[{'+':/$/i,'-':/^/i},'m',1], // exemple : m'a
				'apostrophe':[{'+':/(\'|\’)/i},'m',2] // apostrophe
				}],
		'n' : [['ing','n','ment','urent','irent','erent','ent','nisole','apostrophe'],
				{'n':[{'+':/n/i},'n',2],
				'ment':[this.regle_verbe_mer,'verb_3p',2], // on considère que les verbent terminés par 'ment' se prononcent [#]
				'urent':[{'-':/ure/i,'+':/t$/i},'verb_3p',2], // verbes avec terminaisons en -urent
				'irent':[{'-':/ire/i,'+':/t$/i},'verb_3p',2], // verbes avec terminaisons en -irent
				'erent':[{'-':/ère/i,'+':/t$/i},'verb_3p',2], // verbes avec terminaisons en -èrent
				'ent':[{'-':/e/i,'+':/t$/i},'verb_3p',2],
				'ing':[{'-':/i/i,'+':/g$/i},'g~',2],
				'*':[{},'n',1],
				'nisole':[{'+':/$/i,'-':/^/i},'n',1], // exemple : n'a
				'apostrophe':[{'+':/(\'|\’)/i},'n',2] // apostrophe
				}],
		'o' : [['in','oignon','i','tomn','monsieur','n','m','nm','y1','y2','u','o','oe_0','oe_1','oe_2', 'oe_3','voeux','oeufs','noeud','oeu_defaut','oe_defaut'],
				{'in':[{'+':/i[nm]/i},'w5',3],
				'oignon':[{'-':/^/i,'+':/ignon/i},'o',2],
				'i':[{'+':/(i|î)/i},'wa',2],
				'u':[{'+':/[uwûù]/i},'u',2], // son [u] : clou, clown
				'tomn':[{'-':/t/i,'+':/mn/i},'o',1], // regle spécifique pour 'automne' et ses dérivés
				'monsieur':[{'-':/m/i,'+':/nsieur/i},'q',2],
				'n':[{'+':/n[bcçdfgjklmpqrstvwxz]/i},'o~',2],
				'm':[{'+':/m[bcçdfgjklpqrstvwxz]/i},'o~',2], // toute consonne sauf le m
				'nm':[{'+':/[nm]$/i},'o~',2],
				'y1':[{'+':/y$/i},'wa',2],
				'y2':[{'+':/y/i},'wa',1],
				'o':[{'+':/o/i},'o',2], // exemple : zoo
				'voeux':[{'+':/eux/i},'x^',3], // voeux
				'noeud':[{'+':/eud/i},'x^',3], // noeud
				'oeufs':[{'+':/eufs/i},'x^',3], // traite oeufs et boeufs
				'oeu_defaut':[{'+':/eu/i},'x',3], // exemple : oeuf
				'oe_0':[{'+':/ê/i},'wa',2],
				'oe_1':[{'-':/c/i,'+':/e/i},'o',1], // exemple : coefficient
				'oe_2':[{'-':/m/i,'+':/e/i},'wa',2], // exemple : moelle
				'oe_3':[{'-':/f/i,'+':/e/i},'e',2], // exemple : foetus
				'oe_defaut':[{'+':/e/i},'x',2], // exemple : oeil
				'*':[{},'o',1]}],
		'œ' : [['voeux','oeufs','noeud'],
				{'voeux':[{'+':/ux/i},'x^',2], // voeux
				'noeud':[{'+':/ud/i},'x^',2], // noeud
				'oeufs':[{'+':/ufs/i},'x^',2], // traite oeufs et boeufs
				'*':[{'+':/u/i},'x^',2]}],
		'ô' : [[],
				{'*':[{},'o',1]}],
		'ö' : [[],
				{'*':[{},'o',1]}],
		'p' : [['h','oup','drap','trop','sculpt','sirop','sgalop','rps','amp','compt','bapti','sept','p'],
				{'p':[{'+':/p/i},'p',2],
				'oup':[{'-':/[cl]ou/i,'+':/$/i},'#',1], // les exceptions avec un p muet en fin de mot : loup, coup
				'amp':[{'-':/c(h?)am/i,'+':/$/i},'#',1], // les exceptions avec un p muet en fin de mot : camp, champ
				'drap':[{'-':/dra/i,'+':/$/i},'#',1], // les exceptions avec un p muet en fin de mot : drap
				'trop':[{'-':/tro/i,'+':/$/i},'#',1], // les exceptions avec un p muet en fin de mot : trop
				'sculpt':[{'-':/scul/i,'+':/t/i},'#',1], // les exceptions avec un p muet : sculpter et les mots de la même famille
				'sirop':[{'-':/siro/i,'+':/$/i},'#',1], // les exceptions avec un p muet en fin de mot : sirop
				'sept':[{'-':/^se/i,'+':/t(s?)$/i},'#',1], // les exceptions avec un p muet en fin de mot : sept
				'sgalop':[{'-':/[gs]alo/i,'+':/$/i},'#',1], // les exceptions avec un p muet en fin de mot : galop
				'rps':[{'-':/[rm]/i,'+':/s$/i},'#',1], // les exceptions avec un p muet en fin de mot : corps, camp
				'compt':[{'-':/com/i,'+':/t/i},'#',1], // les exceptions avec un p muet : les mots en *compt*
				'bapti':[{'-':/ba/i,'+':/ti/i},'#',1], // les exceptions avec un p muet : les mots en *bapti*
				'h':[{'+':/h/i},'f_ph',2],
				'*':[{},'p',1]}],
		'q' : [['qu','k'],
				{'qu':[{'+':/u[bcçdfgjklmnpqrstvwxz]/i},'k',1],
				'k':[{'+':/u/i},'k_qu',2],
				'*':[{},'k',1]}],
		'r' : [['monsieur','messieurs','gars','r'],
				{'monsieur':[{'-':/monsieu/i},'#',1],
				'messieurs':[{'-':/messieu/i},'#',1],
				'r':[{'+':/r/i},'r',2],
				'gars':[{'+':/s/i,'-':/ga/i},'#',2], // gars
				'*':[{},'r',1]}],
		's' : [['sch','h','s_final','parasit','para','mars','s','z','sisole','smuet','apostrophe'],
				{'sch':[{'+':/ch/i},'s^',3], // schlem
				'h':[{'+':/h/i},'s^',2],
				's_final':[this.regle_s_final,'s',1], // quelques mots terminés par -us, -is, -os, -as
				'z':[{'-':/[aeiyouéèàüûùëöêîô]/i,'+':/[aeiyouéèàüûùëöêîô]/i},'z_s',1], // un s entre 2 voyelles se prononce [z]
				'parasit':[{'-':/para/i,'+':/it/i},'z_s',1], // parasit*
				'para':[{'-':/para/i},'s',1], // para quelque chose (parasol, parasismique, ...)
				's':[{'+':/s/i},'s',2], // un s suivi d'un autre s se prononce [s]
				'sisole':[{'+':/$/i,'-':/^/i},'s',1], // exemple : s'approche
				'mars':[{'+':/$/i,'-':/mar/i},'s',1], // mars
				'smuet':[{'-':/(e?)/i,'+':/$/i},'#',1], // un s en fin de mot éventuellement précédé d'un e ex. : correctes
				'apostrophe':[{'+':/(\'|\’)/i},'s',2], // apostrophe
				'*':[{},'s',1],
				'@':[{},'#',1]}],
		't' : [['t','tisole','except_tien','_tien','cratie','vingt','tion',
				'ourt','_inct','_spect','_ct','_est','t_final','tmuet','apostrophe'],
				{'t':[{'+':/t/i},'t',2],
				'except_tien':[this.regle_tien,'t',1], // quelques mots où 'tien' se prononce [t]
				'_tien':[{'+':/ien/i},'s_t',1],
				'cratie':[{'-':/cra/i,'+':/ie/i},'s_t',1],
				'vingt':[{'-':/ving/i,'+':/$/i},'t',1], // vingt mais pas vingts
				'tion':[{'+':/ion/i},'s_t',1],
				'tisole':[{'+':/$/i,'-':/^/i},'t',1], // exemple : demande-t-il
				'ourt':[{'-':/(a|h|g)our/i,'+':/$/i},'t',1], // exemple : yaourt, yoghourt, yogourt
				'_est':[{'-':/es/i,'+':/(s?)$/i},'t',1], // test, ouest, brest, west, zest, lest
				'_inct':[{'-':/inc/i,'+':/(s?)$/i},'#',1], // instinct, succinct, distinct
				'_spect':[{'-':/spec/i,'+':/(s?)$/i},'#',1], // respect, suspect, aspect
				'_ct':[{'-':/c/i,'+':/(s?)$/i},'t',1], // tous les autres mots terminés par 'ct'
				't_final':[this.regle_t_final,'t',1], // quelques mots où le "t" final se prononce
				'tmuet':[{'+':/(s?)$/i},'#',1], // un t suivi éventuellement d'un s ex. : marrants
				'*':[{},'t',1],
				'apostrophe':[{'+':/(\'|\’)/i},'t',2], // apostrophe
				'@':[{},'#',1]}],
		'u' : [['um','n','nm','ueil'],
				{'um':[{'-':/[^aefo]/i,'+':/m$/i},'o',1],
				'n':[{'+':/n[bcçdfghjklmpqrstvwxz]/i},'x~',2],
				'nm':[{'+':/[nm]$/i},'x~',2],
				'ueil':[{'+':/eil/i},'x',2], // mots terminés en 'ueil' => son [x^]
				'*':[{},'y',1]}],
		'û' : [[],
				{'*':[{},'y',1]}],
		'ù' : [[],
				{'*':[{},'y',1]}],
		'v' : [[],
				{'*':[{},'v',1]}],
		'w' : [['wapiti','kiwi','sandwich'],
				{'wapiti':[{'+':/apiti/i},'w',1],
				'kiwi':[{'-':/ki/i,'+':/i/i},'w',1],
				'sandwich':[{'+':/ich/i},'w',1],
				'*':[{},'v',1]}],
		'x' : [['six_dix','gz_1','gz_2','gz_3','gz_4','gz_5','_aeox','fix','_ix'],
				{'six_dix':[{'-':/(s|d)i/i},'s_x',1],
				'gz_1':[{'-':/^/i,'+':/[aeiouéèàüëöêîôûù]/i},'gz',1], // mots qui commencent par un x suivi d'une voyelle
				'gz_2':[{'-':/^(h?)e/i,'+':/[aeiouéèàüëöêîôûù]/i},'gz',1], // mots qui commencent par un 'ex' ou 'hex' suivi d'une voyelle
				'gz_3':[{'-':/^coe/i,'+':/[aeiouéèàüëöêîôûù]/i},'gz',1], // mots qui commencent par un 'coex' suivi d'une voyelle
				'gz_4':[{'-':/^ine/i,'+':/[aeiouéèàüëöêîôûù]/i},'gz',1], // mots qui commencent par un 'inex' suivi d'une voyelle
				'gz_5':[{'-':/^(p?)rée/i,'+':/[aeiouéèàüëöêîôûù]/i},'gz',1], // mots qui commencent par un 'réex' ou 'préex' suivi d'une voyelle
				'_aeox':[{'-':/[aeo]/i},'ks',1],
				'fix':[{'-':/fi/i},'ks',1],
				'_ix':[{'-':/(remi|obéli|astéri|héli|phéni|féli)/i},'ks',1],
				'*':[{},'ks',1],
				'@':[{},'#',1]}],
		'y' : [['m','n','nm','abbaye','y_voyelle'],
				{'y_voyelle':[{'+':/[aeiouéèàüëöêîôûù]/i},'j',1], // y suivi d'une voyelle donne [j]
				'abbaye':[{'-':/abba/i,'+':/e/i},'i', 1], // abbaye... bien irrégulier
				'n':[{'+':/n[bcçdfghjklmpqrstvwxz]/i},'e~',2],
				'm':[{'+':/m[mpb]/i},'e~',2],
				'nm':[{'+':/[n|m]$/i},'e~',2],
				'*':[{},'i',1]}],
		'z' : [['riz', 'iz', 'gaz'],
				{'riz':[{'-':/i/i,'+':/$/i},'#',1], // y suivi d'une voyelle donne [j]
				'iz':[{'-':/i/i,'+':/$/i},'z',1],
				'gaz':[{'-':/a/i,'+':/$/i},'z',1],
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
	};
}

/*
 * Règle spécifique de traitement des successions de lettres finales 'ient'
 * sert à savoir si la séquence 'ient' se prononce [i][#] ou [j][e~]
 */
LireCouleurEngine.prototype.regle_ient = function(mot, pos_mot) {
	/*
	 * Ensemble de verbes qui se terminent par -ier // attention : pas d'accents !!
	 */
	var verbes_ier = ['affilier','allier','allier','amnistier','amplifier','anesthesier','apparier',
	'approprier','apprecier','asphyxier','associer','atrophier','authentifier','autographier',
	'autopsier','balbutier','bonifier','beatifier','beneficier','betifier','calligraphier','calomnier',
	'carier','cartographier','certifier','charrier','chier','choregraphier','chosifier','chatier',
	'clarifier','classifier','cocufier','codifier','colorier','communier','conchier','concilier',
	'confier','congedier','contrarier','copier','crier','crucifier','dactylographier',
	'differencier','disgracier','disqualifier','dissocier','distancier','diversifier','domicilier',
	'decrier','dedier','defier','deifier','delier','demarier','demultiplier','demystifier','denazifier',
	'denier','deplier','deprecier','dequalifier','devier','envier','estropier','excommunier',
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
	'verifier','echographier','ecrier','edifier','electrifier','emulsifier','epier','etudier'];
	
	if ((mot.slice(-5).match(/[bcçdfghjklnmpqrstvwxz]ient/) === null) || (pos_mot < mot.length-4)) {
		// le mot ne se termine pas par 'ient' (précédé d'une consonne)
		// ou alors on est en train d'étudier une lettre avant la terminaison en 'ient'
		return false;
	}

	// il faut savoir si le mot est un verbe dont l'infinitif se termine par 'ier' ou non
	var pseudo_infinitif = chaine_sans_accent(mot).substring(0, mot.length-2)+'r';
	if ((pseudo_infinitif.length > 1) && (pseudo_infinitif[1] == '@')) {
		// mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
		pseudo_infinitif = pseudo_infinitif.slice(2);
	}	
	return (verbes_ier.indexOf(pseudo_infinitif) >= 0);
}

/*
 * Règle spécifique de traitement des successions de lettres '*ent'
 * sert à savoir si le mot figure dans les mots qui se prononcent a~ à la fin
 */
LireCouleurEngine.prototype.regle_mots_ent = function(mot, pos_mot) {
	/*
	 * Ensemble de mots qui se terminent par -ent
	 */
	var mots_ent = ['absent', 'abstinent', 'accent', 'accident', 'adhérent', 'adjacent',
	'adolescent', 'afférent', 'agent', 'ambivalent', 'antécédent', 'apparent',
	'arborescent', 'ardent', 'ardent', 'argent', 'arpent', 'astringent', 'auvent',
	'avent', 'cent', 'chiendent', 'client', 'coefficient', 'cohérent', 'dent',
	'différent', 'diligent', 'dissident', 'divergent', 'dolent', 'décadent', 'décent',
	'déficient', 'déférent', 'déliquescent', 'détergent', 'fervent', 'flatulent',
	'fluorescent', 'fréquent', 'féculent', 'gent', 'gradient', 'grandiloquent',
	'immanent', 'imminent', 'impatient', 'impertinent', 'impotent', 'imprudent',
	'impudent', 'impénitent', 'incandescent', 'incident', 'incohérent', 'incompétent',
	'inconscient', 'inconséquent', 'incontinent', 'inconvénient', 'indifférent', 'indigent',
	'indolent', 'indulgent', 'indécent', 'ingrédient', 'inhérent', 'inintelligent',
	'innocent', 'insolent', 'intelligent', 'interférent', 'intermittent', 'iridescent',
	'lactescent', 'latent', 'lent', 'luminescent', 'malcontent', 'mécontent', 'occident',
	'omnipotent', 'omniprésent', 'omniscient', 'onguent', 'opalescent', 'opulent',
	'orient', 'paravent', 'parent', 'patent', 'patient', 'permanent', 'pertinent', 'phosphorescent',
	'polyvalent', 'pourcent', 'proéminent', 'prudent', 'précédent', 'présent',
	'prévalent', 'pschent', 'purulent', 'putrescent', 'pénitent', 'quotient',
	'relent', 'récent', 'récipient', 'récurrent', 'référent', 'régent', 'rémanent',
	'réticent', 'sanguinolent', 'sergent', 'serpent', 'somnolent', 'souvent',
	'spumescent', 'strident', 'subconscient', 'subséquent', 'succulent', 'tangent',
	'torrent', 'transparent', 'trident', 'truculent', 'tumescent', 'turbulent',
	'turgescent', 'urgent', 'vent', 'ventripotent', 'violent', 'virulent', 'effervescent',
	'efficient', 'effluent', 'engoulevent', 'entregent', 'escient', 'event',
	'excédent', 'expédient', 'éloquent', 'éminent', 'émollient', 'évanescent', 'évent'];

	var verbes_enter = ['absenter','accidenter','agrémenter','alimenter','apparenter',
	'cimenter','contenter','complimenter','bonimenter','documenter','patienter',
	'parlementer','ornementer','supplémenter','argenter','éventer','supplémenter',
	'tourmenter','violenter','arpenter','serpenter','coefficienter', 'argumenter',
	'présenter'];

	if (mot.match(/^[bcdfghjklmnpqrstvwxz]ent(s?)$/) !== null) {
		return true;
	}

	// il faut savoir si le mot figure dans la liste des adverbes ou des noms répertoriés
	var comparateur = mot;
	if (mot[mot.length-1] == 's') {
		comparateur = mot.substring(0, mot.length-1);
	}
	if (pos_mot+2 < comparateur.length) {
		return false;
	}

	if ((comparateur.length > 1) && (comparateur[1] == '@')) {
		// mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
		comparateur = comparateur.slice(2);
	}

	// comparaison directe avec la liste de mots où le 'ent' final se prononce [a~]
	if (mots_ent.indexOf(comparateur) >= 0) {
		return true;
	}

	// comparaison avec la liste de verbes qui se terminent par 'enter'
	var pseudo_verbe = comparateur+'er';
	return (verbes_enter.indexOf(pseudo_verbe) >= 0);
}

/*
 * Règle spécifique de traitement des successions de lettres 'ment'
 * sert à savoir si le mot figure dans les mots qui se prononcent a~ à la fin
 */
LireCouleurEngine.prototype.regle_ment = function(mot, pos_mot) {
	/*
	 * Ensemble de verbes qui se terminent par -mer
	 */
	var verbes_mer = ['abimer','acclamer','accoutumer','affamer','affirmer','aimer',
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
	'trimer','zoomer','ecremer','ecumer','elimer'];

	if ((mot.slice(-4).match(/ment/) === null) || (pos_mot < mot.length-3)) {
		// le mot ne se termine pas par 'ment'
		// ou alors on est en train d'étudier une lettre avant la terminaison en 'ment'
		return false;
	}

	// il faut savoir si le mot est un verbe dont l'infinitif se termine par 'ier' ou non
	var pseudo_infinitif = chaine_sans_accent(mot).substring(0, mot.length-2)+'r';
	if ((pseudo_infinitif.length > 1) && (pseudo_infinitif[1] == '@')) {
		// mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
		pseudo_infinitif = pseudo_infinitif.slice(2);
	}	
	if (verbes_mer.indexOf(pseudo_infinitif) > -1) {
		return false;
	}

	// dernier test : le verbe dormir (ils/elles dorment)
	return (mot.slice(-7) !== 'dorment');
}

LireCouleurEngine.prototype.regle_verbe_mer = function(mot, pos_mot) {
	// L'inverse de la règle ci-dessus ou presque
	if ((mot.slice(-4).match(/ment/) === null) || (pos_mot < mot.length-3)) {
		// le mot ne se termine pas par 'ment'
		// ou alors on est en train d'étudier une lettre avant la terminaison en 'ment'
		return false;
	}

	return (!LireCouleurEngine.prototype.regle_ment(mot, pos_mot));
}

/*
 * Règle spécifique de traitement des successions de lettres finales 'er'
 * sert à savoir si le mot figure dans la liste des exceptions
 */
LireCouleurEngine.prototype.regle_er = function(mot, pos_mot) {
	// prendre le mot au singulier uniquement
	var m_sing = mot;
	if (mot[mot.length-1] == 's') {
		m_sing = mot.substring(0, mot.length-1);
	}

	if ((m_sing.length > 1) && (m_sing[1] == '@')) {
		// mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
		m_sing = m_sing.slice(2);
	}

	// tester la terminaison
	if ((mot.slice(-4).match(/er/) === null) || (pos_mot < mot.length-2)) {
		// le mot ne se termine pas par 'er'
		// ou alors on est en train d'étudier une lettre avant la terminaison en 'er'
		return false;
	}

	// il faut savoir si le mot figure dans la liste des exceptions
	var exceptions_final_er = ['amer', 'cher', 'hier', 'mer', 'coroner', 'charter', 'cracker',
	'chester', 'doppler', 'cascher', 'bulldozer', 'cancer', 'carter', 'geyser', 'cocker',
	'alter', 'aster', 'fer', 'cuiller', 'container', 'cutter', 'révolver', 'super', 'master'];
	return (exceptions_final_er.indexOf(m_sing) > -1);
}

/*
 * Règle spécifique de traitement des noms communs qui se terminent par 'ai'
 * Dans les verbes terminés par 'ai', le phonème est 'é'
 * Dans les noms communs terminés par 'ai', le phonème est 'ê'
 */
LireCouleurEngine.prototype.regle_nc_ai_final = function(mot, pos_mot) {
	var possibles = ['balai', 'brai', 'chai', 'déblai', 'délai', 'essai', 'frai', 'geai', 'lai', 'mai',
				'minerai', 'papegai', 'quai', 'rai', 'remblai'];

	var m_seul = mot;
	if ((m_seul.length > 1) && (m_seul[1] == '@')) {
		// mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
		m_seul = m_seul.slice(2);
	}

	if (possibles.indexOf(m_seul) >= 0) {
		return (pos_mot == mot.length-1);
	}
	return false;
}

/*
 * Règle spécifique de traitement des successions de lettres 'eu('
 * Sert à savoir si le mot est le verbe avoir conjugué (passé simple, participe
 * passé ou subjonctif imparfait
 */
LireCouleurEngine.prototype.regle_avoir = function(mot, pos_mot) {
	var possibles = ['eu', 'eue', 'eues', 'eus', 'eut', 'eûmes', 'eûtes', 'eurent',
				'eusse', 'eusses', 'eût', 'eussions', 'eussiez', 'eussent'];
	if (possibles.indexOf(mot) >= 0) {
		return (pos_mot < 2);
	}
	return false;
}

/*
 * Règle spécifique de traitement des mots qui se terminent par "us".
 * Pour un certain nombre de ces mots, le 's' final se prononce.
 */
LireCouleurEngine.prototype.regle_s_final = function(mot, pos_mot) {
	var mots_s_final = ['abribus','airbus','autobus','bibliobus','bus','nimbus','gibus',
	'microbus','minibus','mortibus','omnibus','oribus', 'pédibus', 'quibus','rasibus',
	'rébus','syllabus','trolleybus','virus','antivirus','anus','asparagus','médius',
	'autofocus','focus','benedictus','bonus','campus','cirrus','citrus',
	'collapsus','consensus','corpus','crochus','crocus','crésus','cubitus','humérus',
	'diplodocus','eucalyptus','erectus','hypothalamus','mordicus','mucus','stratus',
	'nimbostratus','nodus','modus','opus','ours','papyrus','plexus','plus','processus','prospectus',
	'lapsus','prunus','quitus','rétrovirus','sanctus','sinus','solidus','liquidus',
	'stimulus','stradivarius','terminus','tonus','tumulus','utérus','versus','détritus',
	'ratus','couscous', 'burnous', 'tous','anis','bis','anubis',
	'albatros','albinos','calvados','craignos','mérinos','rhinocéros','tranquillos','tétanos','os',
	'alias','atlas','hélas','madras','sensas','tapas','trias','vasistas','hypocras','gambas','as',
	'biceps','quadriceps','chips','relaps','forceps','schnaps','laps','oups','triceps','princeps',
	'tricératops'];

	var m_seul = mot;
	if ((m_seul.length > 1) && (m_seul[1] == '@')) {
		// mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
		m_seul = m_seul.slice(2);
	}

	return (mots_s_final.indexOf(m_seul) >= 0);
}

/*
 * Règle spécifique de traitement des mots qui se terminent par la lettre "t" prononcée.
 */
LireCouleurEngine.prototype.regle_t_final = function(mot, pos_mot) {
	var mots_t_final = ['accessit','cet','but','diktat','kumquat','prurit','affidavit','dot','rut','audit',
	'exeat','magnificat','satisfecit','azimut','exit','mat','scorbut','brut',
	'fiat','mazout','sinciput','cajeput','granit','net','internet','transat','sept',
	'chut','huit','obit','transit','coït','incipit','occiput','ut','comput',
	'introït','pat','zut','déficit','inuit','prétérit',
	'gadget','kilt','kit','scout','fret'];

	// prendre le mot au singulier uniquement
	var m_sing = mot;
	if (mot[mot.length-1] == 's') {
		m_sing = mot.substring(0, mot.length-1);
	}

	if ((m_sing.length > 1) && (m_sing[1] == '@')) {
		// mot précédé d'un déterminant élidé - codage de l'apostrophe : voir pretraitement_texte
		m_sing = m_sing.slice(2);
	}

	return (mots_t_final.indexOf(m_sing) > -1);
}


/*
 * Règle spécifique de traitement de quelques mots qui se terminent par 'tien' et
 * dans lesquels le 't' se prononce [t]
 */
LireCouleurEngine.prototype.regle_tien = function(mot, pos_mot) {
	// prendre le mot au singulier uniquement
	var m_sing = mot;
	if (m_sing[mot.length-1] == 's') {
		m_sing = mot.substring(0, mot.length-1);
	}

	// tester la terminaison
	if ((m_sing.slice(-4).match(/tien/) === null) || (pos_mot < m_sing.length-4)) {
		// le mot ne se termine pas par 'tien'
		// ou alors on est en train d'étudier une lettre avant la terminaison en 'tien'
		return false;
	}

	// il faut savoir si le mot figure dans la liste des exceptions
	var exceptions_final_tien = ['chrétien','entretien','kantien','proustien','soutien'];
	return (exceptions_final_tien.indexOf(m_sing) > -1);
}

/*
 * Teste l'application d'une règle
 */
LireCouleurEngine.prototype.teste_regle = function(nom_regle, cle, mot, pos_mot) {

	if (typeof(cle) === "function") {
		// la regle est une fonction spécifique
		// console.log(nom_regle, ' fonction');
		return cle(mot, pos_mot);
	}

	// exemples : '+':'n|m' ou '-':'[aeiou]'
	var trouve_s = true;
	var trouve_p = true;

	if (typeof(cle['+']) !== "undefined") {
		// console.log(nom_regle, ' cle + testee : '+cle['+']);
		// il faut lire les lettres qui suivent
		// recherche le modèle demandé au début de la suite du mot
		var res = cle['+'].exec(mot.slice(pos_mot));
		trouve_s = ((res !== null) && (res.index == 0));
	}
	
	if (typeof(cle['-']) !== "undefined") {
		// console.log(nom_regle, ' cle - testee : '+cle['+']);
		trouve_p = false;
		// teste si la condition inclut le début du mot ou seulement les lettres qui précèdent
		if (cle['-'].source[0] == '^') {
			// le ^ signifie 'début de chaîne' et non 'tout sauf'
			if (cle['-'].source.length == 1) {
				// on vérifie que le début de mot est vide
				trouve_p = (pos_mot == 1);
			} else {
				// le début du mot doit correspondre au pattern
				var res = cle['-'].exec(mot.substring(0, pos_mot-1));
				if (res !== null) {
					trouve_p = (res[0].length == pos_mot-1);
				}
			}
		}
		else {
			var k = pos_mot-2;
			while ((k > -1) && (!trouve_p)) {
				// il faut lire les lettres qui précèdent
				// recherche le modèle demandé à la fin du début du mot
				var res = cle['-'].exec(mot.substring(k, pos_mot-1));
				if (res !== null) {
					trouve_p = (res[0].length == res.input.length);
				}
				k -= 1;
			}
		}
	}

	if (trouve_p & trouve_s) {
		// console.log('mot:'+mot+'['+(pos_mot-1).toString()+'] ; lettre:'+mot[pos_mot-1]+' ; regle appliquee:'+nom_regle+' ; clef utilisee:'+cle);
	}

	return (trouve_p & trouve_s);
}

/*
 * Post traitement pour déterminer si le son [o] est ouvert ou fermé
 */
LireCouleurEngine.prototype.post_traitement_o_ouvert_ferme = function(pp) {
	if ((pp.constructor !== Array) || (pp.length == 1)) {
		return pp;
	}

	if (pp.filter(function(phon, index, array) { return (phon.phoneme == 'o'); }) > 0) {
		// pas de 'o' dans le mot
		return pp;
	}

	// mots en 'osse' qui se prononcent avec un o ouvert
	var mots_osse = ['cabosse', 'carabosse', 'carrosse', 'colosse', 'molosse', 'cosse', 'crosse', 'bosse',
	'brosse', 'rhinocéros', 'désosse', 'fosse', 'gosse', 'molosse', 'écosse', 'rosse', 'panosse'];

	// indice du dernier phonème prononcé
	var npp = clone_tableau(pp);
	while ((npp.length > 0) && (npp[npp.length-1].phoneme == "#")) {
		npp.pop();
	}

	// reconstitution du mot sans les phonèmes muets à la fin
	var mot = "";
	npp.forEach(function(element, index, array) {
		mot += element.lettres;
	});

	if (mots_osse.indexOf(mot) > -1) {
		// certains mots en 'osse' on un o ouvert
		pp.forEach(function(element, index, array) {
			if (element.phoneme == 'o') {
				pp[index].phoneme = 'o_ouvert';
			}
		});
		return pp;
	}

	// consonnes qui rendent possible un o ouvert en fin de mot
	var consonnes_syllabe_fermee = ['p','k','b','d','g','f','f_ph','s^','l','r','m','n'];

	npp.forEach(function(element, i_ph, array) {
		if (element.phoneme == 'o') {
			if (i_ph == npp.length-1) {
				// syllabe tonique ouverte (rien après ou phonème muet) en fin de mot : o fermé
				return pp;
			}

			if (element.lettres != 'ô') {
				// syllabe tonique fermée (présence de consonne après) en fin de mot : o ouvert
				var cas1 = ((i_ph == npp.length-3) && (consonnes_syllabe_fermee.indexOf(pp[i_ph+1].phoneme) > -1) && (pp[i_ph+2].phoneme == 'q_caduc'));
				// o ouvert lorsqu’il est suivi d’un [r] : or, cor, encore, dort, accord
				// o ouvert lorsqu’il est suivi d’un [z^_g] : loge, éloge, horloge
				// o ouvert lorsqu’il est suivi d’un [v] : ove, innove.
				var cas2 = ((i_ph < pp.length-1) && (['r', 'z^_g', 'v'].indexOf(pp[i_ph+1].phoneme) > -1));
				// un o suivi de 2 phonemes consonnes est un o ouvert
				var cas3 = ((i_ph < pp.length-2) && (syllaphon['c'].indexOf(pp[i_ph+1].phoneme) > -1) && (syllaphon['c'].indexOf(pp[i_ph+2].phoneme) > -1));
				
				if (cas1 || cas2 || cas3) {
					pp[i_ph].phoneme = 'o_ouvert';
				}
			}
		}
	});

	return pp;
}

/*
 * Post traitement pour déterminer si le son [x] est ouvert "e" ou fermé "eu"
 */
LireCouleurEngine.prototype.post_traitement_e_ouvert_ferme = function(pp) {
	if ((pp.constructor !== Array) || (pp.length == 1)) {
		return pp;
	}

	if (pp.filter(function(phon, index, array) { return (phon.phoneme == 'x'); }) > 0) {
		// pas de 'x' dans le mot
		return pp;
	}

	// indice du dernier phonème prononcé
	var lpp = pp.length-1;
	while ((lpp > 0) && (pp[lpp].phoneme == "#")) {
		lpp -= 1;
	}

	// on ne s'intéresse qu'au dernier phonème (pour les autres, on ne peut rien décider)
	var i_ph = pp.map(function(phon) { return phon.phoneme; }).lastIndexOf('x');

	if (i_ph < lpp-2) {
		// le phonème n'est pas l'un des 3 derniers du mot : on ne peut rien décider
		return pp;
	}

	if (i_ph == lpp) {
		// le dernier phonème prononcé dans le mot est le 'eu' donc 'eu' fermé
		pp[i_ph].phoneme = 'x^';
		return pp;
	}

 	// le phonème est l'avant dernier du mot (syllabe fermée)
	var consonnes_son_eu_ferme = ['z','z_s','t'];
	if ((consonnes_son_eu_ferme.indexOf(pp[i_ph+1].phoneme) > -1) && (pp[pp.length-1].phoneme == 'q_caduc')) {
		pp[i_ph].phoneme = 'x^';
	}

	return pp;
}

/*
 * Décodage d'un mot sous la forme d'une suite de phonèmes
 */
LireCouleurEngine.prototype.extrairePhonemes = function(mot, para, p_para) {
	var p_mot = 0;
	var codage = new Array();
	var phoneme, pas, lettre;
	var trouve, i, k;
	var np_para = p_para;
	var motmin = mot.toLowerCase();
	
	if (typeof(para) === "undefined") {
		para = mot;
	}
	if (typeof(p_para) === "undefined") {
		np_para = 0;
	}
	while (p_mot < mot.length) {
		// On teste d'application des règles de composition des sons
		lettre = motmin[p_mot];
		// console.log('lettre : '+lettre);

		trouve = false;
		if (lettre in this.autom) {
			var aut = this.autom[lettre][1];
			i = 0;
			while ((!trouve) && (i < this.autom[lettre][0].length)) {
				k = this.autom[lettre][0][i];
				if (this.teste_regle(k, aut[k][0], mot, p_mot+1)) {
					phoneme = aut[k][1];
					pas = aut[k][2];
					codage.push(new LCPhoneme(phoneme, para.substring(np_para, np_para+pas)));
					// console.log('phoneme:'+phoneme+' ; lettre(s) lue(s):'+para.substring(np_para, np_para+pas));
					p_mot += pas;
					np_para += pas;
					trouve = true;
				}
				i += 1;
			}
			// console.log('trouve:'+trouve.toString()+' - '+codage.toString());

			if ((!trouve) && (p_mot == mot.length-1) && aut.hasOwnProperty('@')) {
				if (p_mot == mot.length-1) {
					// c'est la dernière lettre du mot, il faut vérifier que ce n'est pas une lettre muette
					phoneme = aut['@'][1];
					pas = 1;
					codage.push(new LCPhoneme(phoneme,lettre));
					trouve = true;
					p_mot += 1;
					np_para += 1;
					// console.log('phoneme fin de mot:'+phoneme+' ; lettre lue:'+lettre);
				}
			}

			// rien trouvé donc on prend le phonème de base ('*')
			if (!trouve) {
				try {
					phoneme = aut['*'][1];
					pas = aut['*'][2];
					codage.push(new LCPhoneme(phoneme,para.substring(np_para, np_para+pas)));
					np_para += pas;
					p_mot += pas;
					// console.log('phoneme par defaut:'+phoneme+' ; lettre lue:'+lettre);
				}
				catch (e) {
					codage.push(new LCPhoneme(null, lettre));
					np_para += 1;
					p_mot += 1;
					// console.log('non phoneme ; caractere lu:'+lettre);
				}
			}
		}
		else {
			codage.push(new LCPhoneme(null, lettre));
			p_mot += 1;
			np_para += 1;
			// console.log('non phoneme ; caractere lu:'+lettre);
		}
	}
	// console.log('--------------------');
	// console.log(codage);
	// console.log('--------------------');

	// post traitement pour différencier les o ouverts et les o fermés
	codage = this.post_traitement_o_ouvert_ferme(codage);

	// post traitement pour différencier les eu ouverts et les eu fermés
	codage = this.post_traitement_e_ouvert_ferme(codage);

	return codage;
}

/*
 * Décodage d'un mot sous la forme d'une suite de phonèmes
 */
LireCouleurEngine.prototype.extraireSyllabes = function(phonemes, std_lc, oral_ecrit) {
	var i, j, k;
	var phon, phon1, phon2;
	
	if (typeof(std_lc) === "undefined") {
		std_lc = 'std';
	}
	if (typeof(oral_ecrit) === "undefined") {
		oral_ecrit = 'ecrit';
	}

	var nb_phon = phonemes.length;
	if (nb_phon < 2) {
		var syll = new LCSyllabe();
		syll.ajoutePhonemes(phonemes);
		return [syll];
	}

	var nphonemes = new Array();
	if (std_lc == 'std') {
		// Si le décodage est standard dupliquer les phonèmes qui comportent des consonnes doubles
		for (i=0; i<nb_phon; i++) {
			var phon = phonemes[i];
			if (phon.estConsonneRedoublee()) {
				// consonne redoublée
				phon.dedoublerConsonnes()
				nphonemes.push(phon);
				nphonemes.push(phon);
			}
			else {
				nphonemes.push(phon);
			}
		}
	}
	else {
		nphonemes = clone_tableau(phonemes);
	}
	var nb_phon = nphonemes.length;

	// console.log('--------------------'+nphonemes.toString()+'--------------------')
	// préparer la liste de syllabes
	var sylph = new Array();
	for (i=0; i<nb_phon; i++) {
		phon = nphonemes[i];
		if (phon.estPhoneme()) {
			if (phon.estUneVoyelle()) {
				sylph.push(['v',[i]]);
			}
			else if (phon.estUneConsonne()) {
				sylph.push(['c',[i]]);
			}
			else if (phon.estSemiConsonne()) {
				sylph.push(['s',[i]]);
			}
			else {
				// c'est un phonème muet : '#'
				sylph.push(['#',[i]]);
			}
		}
	}

	// mixer les doubles phonèmes de consonnes qui incluent [l] et [r] ; ex. : bl, tr, cr, chr, pl
	i = 0;
	while (i < sylph.length-1) {
		if ((sylph[i][0] == 'c') && (sylph[i+1][0] == 'c')) {
			// deux phonèmes consonnes se suivent
			phon0 = nphonemes[sylph[i][1][0]];
			phon1 = nphonemes[sylph[i+1][1][0]];
			if (((phon1.phoneme == 'l') || (phon1.phoneme == 'r')) && (['b','k','p','t','g','d','f','v'].indexOf(phon0.phoneme) >= 0)) {
				// mixer les deux phonèmes puis raccourcir la chaîne
				sylph[i][1].push.apply(sylph[i][1], sylph[i+1][1]);
				sylph.splice(i+1, 1);
			}
		}
		i += 1;
	}
	// console.log("mixer doubles phonèmes consonnes (bl, tr, cr, etc.) :"+sylph.toString());

	// mixer les doubles phonèmes [y] et [i], [u] et [i,e~,o~]
	i = 0;
	while (i < sylph.length-1) {
		if ((sylph[i][0] == 'v') && (sylph[i+1][0] == 'v')) {
			// deux phonèmes voyelles se suivent
			phon1 = nphonemes[sylph[i][1][0]];
			phon2 = nphonemes[sylph[i+1][1][0]];
			if (((phon1.phoneme == 'y') && (phon2.phoneme == 'i')) || ((phon1.phoneme == 'u') && (['i','e~','o~'].indexOf(phon2.phoneme) >= 0))) {
				// mixer les deux phonèmes puis raccourcir la chaîne
				sylph[i][1].push.apply(sylph[i][1], sylph[i+1][1]);
				sylph.splice(i+1, 1);
			}
		}
		i += 1;
	}
	// console.log("mixer doubles phonèmes voyelles ([y] et [i], [u] et [i,e~,o~]) :"+sylph.toString());

	// accrocher les lettres muettes aux lettres qui précèdent
	i = 0
	while (i < sylph.length-1) {
		if (sylph[i+1][0] == '#') {
			// mixer les deux phonèmes puis raccourcir la chaîne
			sylph[i][1].push.apply(sylph[i][1], sylph[i+1][1]);
			sylph.splice(i+1, 1);
		}
		i += 1;
	}

	// construire les syllabes par association de phonèmes consonnes et voyelles
	sylls = new Array();
	var nb_sylph = sylph.length;
	i = j = 0;
	while (i < nb_sylph) {
		// début de syllabe = tout ce qui n'est pas voyelle
		j = i;
		while ((i < nb_sylph) && (sylph[i][0] != 'v')) {
			i += 1;
		}

		// inclure les voyelles
		var cur_syl = new LCSyllabe(nphonemes);
		if ((i < nb_sylph) && (sylph[i][0] == 'v')) {
			i += 1;
			for (k=j; k<i; k++) {
				cur_syl.ajoutePhonemes(sylph[k][1], nphonemes);
			}
			j = i;

			// ajouter la syllabe à la liste
			sylls.push(cur_syl);
		}

		// la lettre qui suit est une consonne
		if (i+1 < nb_sylph) {
			var lettre1 = nphonemes[sylph[i][1][sylph[i][1].length-1]].lettres;
			var lettre2 = nphonemes[sylph[i+1][1][0]].lettres[0];
			lettre1 = lettre1[lettre1.length-1];
			if (('bcdfghjklmnpqrstvwxzç'.indexOf(lettre1) > -1) && ('bcdfghjklmnpqrstvwxzç'.indexOf(lettre2) > -1)) {
				// inclure cette consonne si elle est suivie d'une autre consonne
				cur_syl.ajoutePhonemes(sylph[i][1], nphonemes);
				i += 1;
				j = i;
			}
		}
	}

	// précaution de base : si pas de syllabes reconnues, on concatène simplement les phonèmes
	if (sylls.length == 0) {
		var syll = new LCSyllabe();
		syll.ajoutePhonemes(phonemes);
		return [syll];
	}

	// il ne doit rester à la fin que les lettres muettes ou des consonnes qu'on ajoute à la dernière syllabe
	for (k=j; k<nb_sylph; k++) {
		sylls[sylls.length-1].ajoutePhonemes(sylph[k][1], nphonemes);
	}

	if ((oral_ecrit == 'oral') && (sylls.length > 1)) {
		// syllabes orales : si la dernière syllabe est finalisée par des lettres muettes ou
		// un e caduc, il faut la concaténer avec la syllabe précédente
		var derniereSyllabe = sylls[sylls.length-1];
		k = derniereSyllabe.phonemes.length-1;
		while ((k > 0) && (['#', 'verb_3p'].indexOf(derniereSyllabe.phonemes[k]) >= 0)) {
			k -= 1;
		}
		if (derniereSyllabe.phonemes[k].phoneme == 'q_caduc') {
			// concaténer la dernière syllabe à l'avant-dernière
			sylls.pop();
			sylls[sylls.length-1].phonemes.push.apply(sylls[sylls.length-1].phonemes, derniereSyllabe.phonemes);
		}
	}

	return sylls;
}

var LireCouleur = new LireCouleurEngine();
