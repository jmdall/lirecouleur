/*
 * lirecouleur-cfg.js gère la configuration de la boite de dialogue.
 * Ce module fait partie du projet LireCouleur - http://lirecouleur.arkaline.fr
 * 
 * @author Marie-Pierre Brungard
 * @version 0.3
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

var archStyles = ["._lc_syll_0 { color: #000000;}", "._lc_syll_1 { color: #00aaaa; }", "._lc_syll_2 { }", "._lc_lien { background-color: #ddd; }", "._lc_standard {font-family: sans-serif; font-size:120%; line-height: 175%; word-spacing: 0.75em; }", "._lc_l_muettes { color: #aaa; }"];

/*
 * Réécriture d'une chaîne de syllabes en HTML
 */
var _formatSyllabes = (function () {
	var _isyl = 0;

	return function (l_syllabes, stl, periode) {
		var docfrag = document.createElement("span");
		l_syllabes.forEach(function(element, index, array) {
			var e = document.createElement("span");
			e.setAttribute("class", "_lc_syll_"+_isyl.toString());
			docfrag.appendChild(element.texte(e));
			_isyl = ((_isyl+1) % periode);
		});
		return docfrag;
	};
})();

/*
 * Décodage d'un élément DOM sous la forme d'une suite de phonèmes
 */
function _formatTexte(paragraphe, stl, periode) {
	var docfrag = document.createElement('span');
	docfrag.setAttribute("class", "_lc_standard");
	var pos = 0;
	var pmots = paragraphe.match(/([a-z@àäâéèêëîïôöûùçœ'’]+)/gi);
	if (pmots !== null) {
		pmots.forEach(function(mot, index, array) {
			var e = document.createElement('span');
			var i = paragraphe.indexOf(mot, pos);
			e.appendChild(document.createTextNode(paragraphe.substring(pos, i)));
					
			var phon = LireCouleur.extrairePhonemes(mot);
			var sylls = LireCouleur.extraireSyllabes(phon);
								
			e.appendChild(_formatSyllabes(sylls, stl, periode));
			pos += mot.length+(i-pos);

			docfrag.appendChild(e);
		});
		docfrag.appendChild(document.createTextNode(paragraphe.substring(pos)));
	}
	return docfrag;
}

// ouverture de la fenêtre de configuration
self.port.on("show", function(paragraphe, stl) {
	var styleEl = document.getElementById("lirecouleur_stylesheet");
	if (styleEl.sheet.cssRules.length == 1) {
		for (var i=0; i<stl.length; i++) {
			try {
				styleEl.sheet.insertRule(stl[i], styleEl.sheet.cssRules.length);
			} catch (e) {
				styleEl.sheet.insertRule(archStyles[i], styleEl.sheet.cssRules.length);
			}
		}
	} else {
		for (var i=0; i<stl.length; i++) {
			styleEl.sheet.deleteRule(i+1);
			try {
				styleEl.sheet.insertRule(stl[i], i+1);
			} catch (e) {
				styleEl.sheet.insertRule(archStyles[i], i+1);
			}
		}
	}

	var elt = document.getElementById('lirecouleur');
	var periode = 1;
	if (stl[periode].indexOf("color") > -1) periode ++;
	if (stl[periode].indexOf("color") > -1) periode ++;

	elt.replaceChild(_formatTexte(paragraphe, stl, periode), elt.childNodes[0]);
});
