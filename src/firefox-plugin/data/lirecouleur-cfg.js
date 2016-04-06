/*
 * lirecouleur-cfg.js gère la configuration de la boite de dialogue.
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

var archStyles = ["._lc_syll_0 { color: #000000;}", "._lc_syll_1 { color: #00aaaa; }", "._lc_syll_2 { }", "._lc_lien { background-color: #ddd; }", "._lc_standard {font-family: sans-serif; font-size:120%; line-height: 175%; word-spacing: 0.75em; }", "._lc_l_muettes { color: #aaa; }"];

function rgb2hex(orig){
	var rgb = orig.replace(/\s/g,'').match(/^rgba?\((\d+),(\d+),(\d+)/i);
	return (rgb && rgb.length === 4) ? "#" +
		("0" + parseInt(rgb[1],10).toString(16)).slice(-2) +
		("0" + parseInt(rgb[2],10).toString(16)).slice(-2) +
		("0" + parseInt(rgb[3],10).toString(16)).slice(-2) : orig;
}

function replaceRule(sheet, indice) {
	var fg = document.getElementById("fg_"+indice.toString());
	var bg = document.getElementById("bg_"+indice.toString());

	var nr = sheet.cssRules[indice].selectorText+" { ";
	if (fg.value.length > 0) nr += "color: "+rgb2hex(fg.value)+"; ";
	if (bg.value.length > 0) nr += "background-color: "+rgb2hex(bg.value)+"; ";
	nr += "}";
	
	sheet.deleteRule(indice);
	return sheet.insertRule(nr, indice);
}

function effacer(id, indice) {
	var styleEl = document.getElementById("lirecouleur_stylesheet");
	var elt = document.getElementById(id+"_"+indice);
	elt.value = "";
	elt.style.background = "#fff";
	return replaceRule(styleEl.sheet, parseInt(indice, 10));
}

function ajusterStyleStandard(id, sens) {
	var styleEl = document.getElementById("lirecouleur_stylesheet");
	var elt = document.getElementById(id);
	var val = parseFloat(elt.value);
	if ((id == "fontSize") || (id == "lineHeight")) {
		if (sens == "-") val -= 5;
		if (sens == "+") val += 5;
		if (val < 0) val = 0;
		elt.value = val.toString()+"%";
	} else {
		if (sens == "-") val -= 0.05;
		if (sens == "+") val += 0.05;
		if (val < 0) val = 0;
		elt.value = val.toString()+"em";
	}

	var fontSize = document.getElementById("fontSize");
	var lineHeight = document.getElementById("lineHeight");
	var wordSpacing = document.getElementById("wordSpacing");

	var nr = styleEl.sheet.cssRules[5].selectorText+" { font-family: sans-serif; ";
	nr += "font-size: "+fontSize.value+"; ";
	nr += "line-height: "+lineHeight.value+"; ";
	nr += "word-spacing: "+wordSpacing.value+"; ";
	nr += "}";
	
	styleEl.sheet.deleteRule(5);
	return styleEl.sheet.insertRule(nr, 5);
}

// ouverture de la fenêtre de configuration
self.port.on("show", function(styles) {
	var bouton_ok = document.getElementById("okButton");
	var bouton_reset = document.getElementById("resetButton");
	var fg_1 = document.getElementById("fg_1");
	var fg_2 = document.getElementById("fg_2");
	var fg_3 = document.getElementById("fg_3");
	var fg_4 = document.getElementById("fg_4");
	var fg_6 = document.getElementById("fg_6");
	var bg_1 = document.getElementById("bg_1");
	var bg_2 = document.getElementById("bg_2");
	var bg_3 = document.getElementById("bg_3");
	var bg_4 = document.getElementById("bg_4");
	var bg_6 = document.getElementById("bg_6");
	var fontSize = document.getElementById("fontSize");
	var lineHeight = document.getElementById("lineHeight");
	var wordSpacing = document.getElementById("wordSpacing");
	var styleEl = document.getElementById("lirecouleur_stylesheet");

	$('.color').colorPicker({
		renderCallback: function($elm, toggled) {
			var elt = document.getElementById($elm[0].id);
			elt.value = rgb2hex(elt.value);
			var indice = parseInt(elt.id.split("_")[1], 10);

			// remplace la règle existante
			replaceRule(styleEl.sheet, indice);			
		}
	});

	// validation pahr touche "entrée"
	bouton_ok.addEventListener('keyup', function onkeyup(event) {
		if (event.keyCode == 13) {
			self.port.emit("lirecouleur-config", [styleEl.sheet.cssRules[1].cssText, styleEl.sheet.cssRules[2].cssText, styleEl.sheet.cssRules[3].cssText, styleEl.sheet.cssRules[4].cssText, styleEl.sheet.cssRules[5].cssText, styleEl.sheet.cssRules[6].cssText]);
		}
	}, false);

	// validation par "clic"
	bouton_ok.addEventListener('click', function () {
		self.port.emit("lirecouleur-config", [styleEl.sheet.cssRules[1].cssText, styleEl.sheet.cssRules[2].cssText, styleEl.sheet.cssRules[3].cssText, styleEl.sheet.cssRules[4].cssText, styleEl.sheet.cssRules[5].cssText, styleEl.sheet.cssRules[6].cssText]);
	}, false);

	// réinitialisation par "clic"
	bouton_reset.addEventListener('click', function () {
		styles = ["._lc_syll_0 { color: #000000;}", "._lc_syll_1 { color: #00aaaa; }", "._lc_syll_2 { }", "._lc_lien { background-color: #ddd; }", "._lc_standard {font-family: sans-serif; font-size:120%; line-height: 175%; word-spacing: 0.75em; }", "._lc_l_muettes { color: #aaa; }"];
		for (var i=0; i<6; i++) {
			styleEl.sheet.deleteRule(i+1);
			styleEl.sheet.insertRule(styles[i], i+1);
		}

		fg_1.value = fg_1.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[1].style.color);
		fg_2.value = fg_2.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[2].style.color);
		fg_3.value = fg_3.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[3].style.color);
		fg_4.value = fg_4.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[4].style.color);
		fg_6.value = fg_6.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[6].style.color);

		bg_1.value = bg_1.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[1].style.backgroundColor);
		bg_2.value = bg_2.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[2].style.backgroundColor);
		bg_3.value = bg_3.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[3].style.backgroundColor);
		bg_4.value = bg_4.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[4].style.backgroundColor);
		bg_6.value = bg_6.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[6].style.backgroundColor);

		fontSize.value = styleEl.sheet.cssRules[5].style.fontSize;
		lineHeight.value = styleEl.sheet.cssRules[5].style.lineHeight;
		wordSpacing.value = styleEl.sheet.cssRules[5].style.wordSpacing;
	}, false);

	if (styleEl.sheet.cssRules.length == 1) {
		for (var i=0; i<6; i++) {
			try {
				styleEl.sheet.insertRule(styles[i], i+1);
			} catch (e) {
				styleEl.sheet.insertRule(archStyles[i], i+1);
			}
		}
	}
			
	fg_1.value = fg_1.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[1].style.color);
	fg_2.value = fg_2.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[2].style.color);
	fg_3.value = fg_3.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[3].style.color);
	fg_4.value = fg_4.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[4].style.color);
	fg_6.value = fg_6.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[6].style.color);
	bg_1.value = bg_1.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[1].style.backgroundColor);
	bg_2.value = bg_2.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[2].style.backgroundColor);
	bg_3.value = bg_3.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[3].style.backgroundColor);
	bg_4.value = bg_4.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[4].style.backgroundColor);
	bg_6.value = bg_6.style.backgroundColor = rgb2hex(styleEl.sheet.cssRules[6].style.backgroundColor);
	fontSize.value = styleEl.sheet.cssRules[5].style.fontSize;
	lineHeight.value = styleEl.sheet.cssRules[5].style.lineHeight;
	wordSpacing.value = styleEl.sheet.cssRules[5].style.wordSpacing;

	bouton_ok.focus();
});

/*
$(document).ready(function()
{
});
*/
