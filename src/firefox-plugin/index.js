/*
 * index.js est le point d'entrée de l'extension LireCouleur pour Firefox.
 * Ce module fait partie du projet LireCouleur - http://lirecouleur.arkaline.fr
 * 
 * @author Marie-Pierre Brungard
 * @version 1.2.0
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
 * 
 */
var styles = ["._lc_syll_0 { color: #000000;}", "._lc_syll_1 { color: #00aaaa; }", "._lc_syll_2 { }", "._lc_lien { background-color: #ddd; }", "._lc_standard {font-family: sans-serif; font-size:120%; line-height: 175%; word-spacing: 0.75em; }", "._lc_l_muettes { color: #aaa; }"];

var self = require("sdk/self");
var tabs = require("sdk/tabs");
var data = require("sdk/self").data;
var archiveur = require("sdk/simple-storage");
var selection = require("sdk/selection");
var { getActiveView }=require("sdk/view/core");

// fenêtre de présentation des syllabes en plus gros
var lirecouleur_dsp = require("sdk/panel").Panel({
	width: 600,
	height: 300,
	contentURL: data.url("lirecouleur.html"),
	contentScriptFile: [data.url("lirecouleur.js"), data.url("lirecouleur-dsp.js")]
});
var lirecouleur_dsp_status = false;
var lirecouleur_status = {};
var selectedText = "";

function selectionChanged(event){
    selectedText = selection.text;
}
selection.on('select', selectionChanged);

// bouton de lancement du traitement
var lc_button1 = require("sdk/ui/button/action").ActionButton({
  id: "lc_button1",
  label: "LireCouleur",
  icon: {
    "16": "./icon-16.png",
    "32": "./icon-32.png",
    "64": "./icon-64.png"
  },
  onClick: handleButton1
});

function handleButton1()
{
	if (typeof(archiveur.storage.syll_1) !== "undefined") {
		styles[0] = archiveur.storage.syll_1;
	}
	if (typeof(archiveur.storage.syll_2) !== "undefined") {
		styles[1] = archiveur.storage.syll_2;
	}
	if (typeof(archiveur.storage.syll_3) !== "undefined") {
		styles[2] = archiveur.storage.syll_3;
	}
	if (typeof(archiveur.storage.liens) !== "undefined") {
		styles[3] = archiveur.storage.liens;
	}
	if (typeof(archiveur.storage.lc) !== "undefined") {
		styles[4] = archiveur.storage.lc;
	}
	if (typeof(archiveur.storage.l_muettes) !== "undefined") {
		styles[5] = archiveur.storage.l_muettes;
	}
	
	if (lirecouleur_dsp_status) {
		// cacher la fenêtre de texte sélectionné
		lirecouleur_dsp_status = !lirecouleur_dsp_status;
		lirecouleur_dsp.hide();

		lc_button2.state("tab", {
			disabled: false
		});
		if (selectedText) selectedText = "";
	} else {
		if (selectedText) {
			// colorier et montrer le texte sélectionné dans une fenêtre
			lirecouleur_dsp.on("show", function() {
				lirecouleur_dsp.port.emit("show", selectedText, styles);
			});
			getActiveView(lirecouleur_dsp).setAttribute("noautohide", true);
			lirecouleur_dsp_status = !lirecouleur_dsp_status;
			lirecouleur_dsp.show();

			lc_button2.state("tab", {
				disabled: true
			});
		} else {
			var lirecouleur_w = tabs.activeTab.attach({
				contentScriptFile: [self.data.url("lirecouleur.js"), self.data.url("lirecouleur-url.js")]
			});
			if (typeof(lirecouleur_status[tabs.activeTab.id]) === "undefined") lirecouleur_status[tabs.activeTab.id] = false;
			if (lirecouleur_status[tabs.activeTab.id]) {
				// page en cours à remettre en noir
				tabs.activeTab.reload();
			} else {
				// coloriage de la page en cours
				lirecouleur_w.port.emit("lirecouleur", styles);
				lc_button1.state("tab", {
					label: "Effacer couleurs",
					icon: { "16": "./icongray-16.png",
							"32": "./icongray-32.png",
							"64": "./icongray-64.png"}
				});
			}
			
			tabs.activeTab.on("ready", function() {
				// la fenêtre est rechargée
				lirecouleur_status[tabs.activeTab.id] = false;
				lc_button1.state("tab", {
					label: "LireCouleur",
					icon: { "16": "./icon-16.png",
							"32": "./icon-32.png",
							"64": "./icon-64.png"}
				});
			});

			lirecouleur_status[tabs.activeTab.id] = !lirecouleur_status[tabs.activeTab.id];
		}
	}
}

// fenêtre de configuration de style
var lirecouleur_cfg = require("sdk/panel").Panel({
	width: 700,
	height: 400,
	contentURL: data.url("lirecouleur_cfg.html"),
	contentScriptFile: [data.url("jquery-2.2.2.min.js"), data.url("jqColorPicker.min.js"), data.url("lirecouleur-cfg.js")]
});

// bouton pour ouvrir la fenêtre de configuration
var lc_button2 = require("sdk/ui/button/action").ActionButton({
	id: "lc_button2",
	label: "Configurer LireCouleur",
	icon: {
		"16": "./config-16.png",
		"32": "./config-32.png",
		"64": "./config-64.png"
	},
	onClick: function() {
		getActiveView(lirecouleur_cfg).setAttribute("noautohide", true);
		lirecouleur_cfg.show();
	}
});

lirecouleur_cfg.on("show", function() {
	lirecouleur_cfg.port.emit("show", styles);
				
	if (typeof(lirecouleur_status[tabs.activeTab.id]) === "undefined") lirecouleur_status[tabs.activeTab.id] = false;
	if (lirecouleur_status[tabs.activeTab.id]) {
		lc_button1.state("tab", {
			disabled: true,
			label: "Effacer couleurs",
			icon: { "16": "./icongray-16.png",
					"32": "./icongray-32.png",
					"64": "./icongray-64.png"}
		});
	} else {
		lc_button1.state("tab", {
			disabled: true,
			label: "LireCouleur",
			icon: { "16": "./icon-16.png",
					"32": "./icon-32.png",
					"64": "./icon-64.png"}
		});
	}
});

lirecouleur_cfg.port.on("lirecouleur-config", function (rstyles) {
	// attribution des nouvelles typographies
	var i = 0;
	styles[i] = rstyles[0];
	if (styles[i].length > 0) i ++;
	styles[i] = rstyles[1];
	if (styles[i].length > 0) i ++;
	styles[i] = rstyles[2];
	if (styles[i].length > 0) i ++;
	styles[i] = styles[i+1] = "";

	styles[3] = rstyles[3];
	styles[4] = rstyles[4].trim();
	styles[5] = rstyles[5];

	archiveur.storage.syll_1 = styles[0];
	archiveur.storage.syll_2 = styles[1];
	archiveur.storage.syll_3 = styles[2];
	archiveur.storage.liens = styles[3];
	archiveur.storage.lc = styles[4];
	archiveur.storage.l_muettes = styles[5];
	lirecouleur_cfg.hide();
	
	if (typeof(lirecouleur_status[tabs.activeTab.id]) === "undefined") lirecouleur_status[tabs.activeTab.id] = false;
	if (lirecouleur_status[tabs.activeTab.id]) {
		// mise à jour de la page affichée
		var lirecouleur_w = tabs.activeTab.attach({
			contentScriptFile: [self.data.url("lirecouleur.js"), self.data.url("lirecouleur-url.js")]
		});
		lirecouleur_w.port.emit("updateStylesheet", styles);

		lc_button1.state("tab", {
			disabled: false,
			label: "Effacer couleurs",
			icon: { "16": "./icongray-16.png",
					"32": "./icongray-32.png",
					"64": "./icongray-64.png"}
		});
	} else {
		lc_button1.state("tab", {
			disabled: false,
			label: "LireCouleur",
			icon: { "16": "./icon-16.png",
					"32": "./icon-32.png",
					"64": "./icon-64.png"}
		});
	}
});
