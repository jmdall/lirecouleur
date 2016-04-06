/*
 * lirecouleur-url.js effectue le formatage d'un texte en syllabes.
 * Ce module fait partie du projet LireCouleur - http://lirecouleur.arkaline.fr
 * 
 * @author Marie-Pierre Brungard
 * @version 0.1
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
 * Réécriture d'une chaîne de syllabes en HTML
 */
var _formatSyllabes = (function () {
	var _isyl = 0;

	return function (l_syllabes, periode) {
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
 * Décodage d'un élément DOM sous la forme d'une suite de syllabes
 */
function _formatElement(elt, periode) {
	// traitement des noeuds enfants
	for (var i=0; i<elt.childNodes.length; i+=1) {
		// traitement du noeud texte
		if ((elt.childNodes[i].nodeType == 3) || (elt.childNodes[i].nodeType == 4) || (elt.childNodes[i].nodeName == 'SPAN')) { // Text ou CDATA
			paragraphe = elt.childNodes[i].textContent;
			var pos = 0;
			var pmots = paragraphe.match(/([a-z@àäâéèêëîïôöûùçœ'’]+)/gi);
			if (pmots !== null) {
				var para = document.createElement("span");
				para.setAttribute("class", "_lc_standard");
				if (elt.nodeName == 'A') {
					para.setAttribute("class", "_lc_lien");
				}
				pmots.forEach(function(mot, index, array) {
					var i = paragraphe.indexOf(mot, pos);
					para.appendChild(document.createTextNode(paragraphe.substring(pos, i)));
							
					var phon = LireCouleur.extrairePhonemes(mot);
					var sylls = LireCouleur.extraireSyllabes(phon);
								
					para.appendChild(_formatSyllabes(sylls, periode));
					pos += mot.length+(i-pos);
				});
				para.appendChild(document.createTextNode(paragraphe.substring(pos)));
				
				// remplace le texte d'origine par le texte traité
				elt.replaceChild(para, elt.childNodes[i]);
			}
		}
		else {
			_formatElement(elt.childNodes[i], periode);
		}
	}
}

/*
 * "self" is a global object in content scripts
 */
self.port.on("lirecouleur", function(styles) {
	var archStyles = ["._lc_syll_0 { color: #000000;}", "._lc_syll_1 { color: #00aaaa; }", "._lc_syll_2 { }", "._lc_lien { background-color: #ddd; }", "._lc_standard {font-family: sans-serif; font-size:120%; line-height: 175%; word-spacing: 0.75em; }", "._lc_l_muettes { color: #aaa; }"];
	var styleEl = document.getElementById("lirecouleur_stylesheet");
	if ((typeof(styleEl) === "undefined") || (styleEl === null)) {
		var periode = 1;
		if (styles[periode].indexOf("color") > -1) periode ++;
		if (styles[periode].indexOf("color") > -1) periode ++;

		// création de la feuille de style lirecouleur
		styleEl = document.createElement('style');
		styleEl.type = 'text/css';
		styleEl.id = "lirecouleur_stylesheet";
        // styleEl.innerHTML = ...;
		document.head.appendChild(styleEl);
		for (var i=0; i<styles.length; i++) {
			try {
				styleEl.sheet.insertRule(styles[i], styleEl.sheet.cssRules.length);
			} catch (e) {
				styleEl.sheet.insertRule(archStyles[i], styleEl.sheet.cssRules.length);
			}
		}
		
		// segmenter le texte en syllabes
		_formatElement(document.body, periode);
	}
});

/*
 * "self" is a global object in content scripts
 */
self.port.on("updateStylesheet", function(styles) {
	var styleEl = document.getElementById("lirecouleur_stylesheet");
	if ((typeof(styleEl) !== "undefined") && (styleEl !== null)) {
		for (var i=0; i<styles.length; i++) {
			styleEl.sheet.deleteRule(i);
			styleEl.sheet.insertRule(styles[i], i);
		}
	}
});
