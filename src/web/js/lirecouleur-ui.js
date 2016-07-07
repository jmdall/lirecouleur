/*
 * 
 */
function LireCouleurFormat() {
	this.correspondances = {'verb_3p':'phon_muet', '#':'phon_muet', 'q_caduc':'phon_e',
		'a':'phon_a', 'q':'phon_e', 'i':'phon_i', 'o':'phon_o', 'o_comp':'phon_o',
		'o_ouvert':'phon_o', 'u':'phon_ou', 'y':'phon_u', 'e':'phon_ez',
		'e_comp':'phon_ez', 'w':'phon_w', 'wa':'phon_wa', 'w5':'phon_w5',
		'e^':'phon_et', 'e^_comp':'phon_et', 'a~':'phon_an', 'e~':'phon_in',
		'x~':'phon_un', 'o~':'phon_on', 'x':'phon_e', 'x^':'phon_eu', 'j':'phon_y',
		'z_s':'phon_z', 'g_u':'phon_g', 'z^_g':'phon_ge', 's_x':'phon_s',
		'n~':'phon_gn', 'g~':'phon_ng', 'p':'phon_p', 't':'phon_t', 'k':'phon_k', 'k_qu':'phon_k',
		'b':'phon_b', 'd':'phon_d', 'g':'phon_g', 'f':'phon_f', 'f_ph':'phon_f',
		's':'phon_s', 's_c':'phon_s', 's_t':'phon_s', 's^':'phon_ch', 'v':'phon_v',
		'z':'phon_z', 'z^':'phon_ge', 'm':'phon_m', 'n':'phon_n', 'l':'phon_l',
		'r':'phon_r', 'ks':'phon_ks', 'gz':'phon_gz'};

	/*
	 * Code les typographies adoptées pour les phonèmes et les syllabes
	 */
	this.couleurs = {
		"syl_1" : "color: #0000ff;",
		"syl_2" : "color: #ff0000;",
		"syl_3" : "color: #008000;",
		"muet" : "color: #cccccc;",
		"phon_muet": "color: #aaaaaa;",
		"phon_e": "color: #ff0000;",
		"phon_a": "color: #0023ff;",
		"phon_i": "color: #a9d82e;",
		"phon_o": "color: #cf6633;",
		"phon_ou": "color: #ffcc00; ",
		"phon_u": "color: #008000;",
		"phon_ez": "color: #00dbc5;",
		"phon_w": "color: #892ca0;",
		"phon_wa": "color: #892ca0;",
		"phon_w5": "color: #3deb3d;",
		"phon_et": "color: #666699;",
		"phon_an": "color: #0023ff; font-family: serif; font-style: oblique; font-weight: bold;",
		"phon_in": "color: #a9d82e; font-family: serif; font-style: oblique; font-weight: bold;",
		"phon_un": "color: #a9d82e; font-family: serif; font-style: oblique; font-weight: bold;",
		"phon_on": "color: #cf6633; font-family: serif; font-style: oblique; font-weight: bold;",
		"phon_eu": "color: #198a8a;",
		"phon_y": "color: #000; font-family: serif; font-style: italic; border-style: none none solid none;",
		"phon_z": "color: #31859b; font-weight: bold; font-style: oblique; ",
		"phon_g": "color: #632423; ",
		"phon_ge": "color: #205867; ",
		"phon_s": "color: #5f497a; font-weight: bold; font-style: oblique; ",
		"phon_gn": "color: #938953; font-weight: bold; font-style: oblique; font-family: serif; ",
		"phon_ng": "color: #494429; ",
		"phon_p": "color: #c3d69b; font-weight: bold; font-style: oblique; font-family: serif; ",
		"phon_t": "color: #76923c; font-weight: bold; font-style: oblique; ",
		"phon_k": "color: #4f6128; ",
		"phon_b": "color: #d99694; font-weight: bold; font-style: oblique; font-family: serif; ",
		"phon_d": "color: #953734; font-weight: bold; font-style: oblique; ",
		"phon_f": "color: #b2a2c7; font-weight: bold; font-family: serif; font-style: oblique; ",
		"phon_ch": "color: #3f3151; ",
		"phon_v": "color: #92cddc; font-weight: bold; font-style: oblique; font-family: serif; ",
		"phon_m": "color: #e36c09; font-weight: bold; font-style: oblique; ",
		"phon_n": "color: #974806; ",
		"phon_l": "color: #fac08f; font-weight: bold; font-style: oblique; font-family: serif; ",
		"phon_r": "color: #974806; font-family: serif; ",
		"phon_ks": "color: #548dd4; font-weight: bold; font-style: oblique; font-family: serif; ",
		"phon_gz": "color: #0f243e; "
	};
    
    this.style_semi = {
		"w" : "	font-family: serif; font-style: italic; border-style: none none dotted none;",
		"y" : "	font-family: serif; font-style: italic; border-style: none none double none;",
		"j" : "	font-family: serif; font-style: italic; border-style: none none solid none;",
    };
    
	this._isyl = 0;
	
	this.phonemes = {};
	for(var key in this.correspondances) {
		this.phonemes[this.correspondances[key]] = false;
	}
}
var LireCouleurFormateur = new LireCouleurFormat();

/*
 * Repère la sélection des phonèmes à présenter
 */
LireCouleurFormat.prototype.selecteur = function() {
	for(var key in this.phonemes) {
		var chkbox = document.getElementById("chk_"+key);
		if (chkbox !== null) {
			this.phonemes[key] = chkbox.checked;
		}
		else {
			this.phonemes[key] = false;
		}
	}
}

/*
 * Convertit les données en texte
 */
LireCouleurFormat.prototype.toString = function() {
	var txt = '{ "lirecouleur" : [';
	for(var key in this.phonemes) {
		txt += '\n\t{"phon" : "' + key + '", "style": "'+this.couleurs[key]+'", ';
		txt += '"select": "'+this.phonemes[key].toString()+'"},';
	}
	
	return txt.substring(0,txt.length-1)+"\n]}";
}

/*
 * Convertit le texte en données
 */
LireCouleurFormat.prototype.fromString = function(txt) {
	var moi = this;
	var cfg = JSON.parse(txt)['lirecouleur'];
	
	cfg.forEach(function(element, index, array) {
		moi.phonemes[element.phon] = (String(element.select) == 'true');
		moi.couleurs[element.phon] = element.style;
		if (document.getElementById("chk_"+element.phon) !== null) {
			document.getElementById("chk_"+element.phon).checked = moi.phonemes[element.phon];
		}
		if (document.getElementById("cfg_"+element.phon) !== null) {
			document.getElementById("cfg_"+element.phon).innerHTML = '<span style="'+element.style+'">'+element.phon.substring(5)+'</span>';
		}
	});
}

/*
 * Place le formatage dans des cookies
 */
LireCouleurFormat.prototype.setCookies = function() {
	this.selecteur();
	for(var key in this.phonemes) {
		Cookies.remove(key);
		Cookies.set(key, {style: this.couleurs[key], select: this.phonemes[key]}, { expires: 365 });
	}
}

/*
 * Relit les cookies pour récupérer la configuration
 */
LireCouleurFormat.prototype.getCookies = function() {
	var cc = 0;
	for(var key in this.phonemes) {
		var cook = Cookies.getJSON(key);
		if (typeof(cook) !== 'undefined') {
			this.couleurs[key] = cook.style;
			this.phonemes[key] = (String(cook.select) == "true");
			cc += 1;
		}
	}
	if (cc == 0) {
		for (var i=0; i<syllaphon['v'].length; i+=1) {
			this.phonemes[this.correspondances[syllaphon['v'][i]]] = true;
		}
	}
}

/*
 * Décodage d'un mot sous la forme d'une suite de phonèmes
 */
LireCouleurFormat.prototype.formatPhonemes = function(document, docfrag, l_phonemes) {
	var moi = this;
	var iphon;
	l_phonemes.forEach(function(element, index, array) {
		var e = document.createElement("span");
        
        if (element.estSemiConsonne()) {
            var il = 1;
            if (element.phoneme.startsWith('w_') && element.lettres.startsWith('ou')) {
                // micmac pour savoir s'il faut souligner une ou 2 lettres
                il = 2;
            }
            iphon = moi.correspondances[element.phoneme.substring(2)];
            if (element.estPhoneme() && moi.phonemes[iphon]) {
                e.style = moi.couleurs[iphon];
                
                var ee = document.createElement("span");
                ee.style = moi.style_semi[element.phoneme.substring(0, 1)];
                ee.appendChild(document.createTextNode(element.lettres.substring(0, il)));
                e.appendChild(ee);
                
                e.appendChild(document.createTextNode(element.lettres.substring(il)));
            }
        }
        else {
            iphon = moi.correspondances[element.phoneme];
            if (element.estPhoneme() && moi.phonemes[iphon]) {
                e.style = moi.couleurs[iphon];
            }
            e.appendChild(document.createTextNode(element.lettres));
        }
		docfrag.appendChild(e);
	});
	return docfrag;
}

/*
 * Décodage d'un mot sous la forme d'une suite de phonèmes
 */
LireCouleurFormat.prototype.formatSyllabes = function(document, docfrag, l_syllabes) {
	var moi = this;
	var muet = this.couleurs['phon_muet'];
	l_syllabes.forEach(function(element, index, array) {
		var e = document.createElement("span");
		e.style = moi.couleurs['syl_'+(moi._isyl+1).toString()];
		docfrag.appendChild(element.texte(e, muet));
		moi._isyl = ((moi._isyl+1) % 3);
	});
	return docfrag;
}

/*
 * 
 */
var LireCouleurStyle = function(chaine) {
	var moi = this;
	this.dict = {};
	chaine.split(';').forEach(function(un_item, index, array) {
		if (un_item.length > 0) {
			var attval = un_item.split(':');
			if (attval.length == 2) {
				moi.dict[attval[0].trim()] = attval[1].trim();
			}
		}
	});
}

/*
 * Transforme un style en chaîne de caractères
 */
LireCouleurStyle.prototype.toString = function() {
	var stl = "";
	for(var key in this.dict) {
		stl += key + ': ' + this.dict[key] + '; ';
	}
	return stl;
}

/*

*/
function lirecouleurPhonemes()
{
	var pos;
	var node = document.getElementById("lirecouleur");
	node.innerHTML = "";

	LireCouleurFormateur.selecteur();
	document.getElementById("lcTexte").value.split("\n").forEach(function(paragraphe, index, array) {
		var para = document.createElement('p');
		pos = 0;
		var pmots = paragraphe.match(/([a-z@àäâéèêëîïôöûùçœ'’]+)/gi);
		if (pmots !== null) {
			pmots.forEach(function(element, index, array) {
				var i = paragraphe.indexOf(element, pos);
				para.appendChild(document.createTextNode(paragraphe.substring(pos, i)));
				
				var phon = LireCouleur.extrairePhonemes(element);
				
				LireCouleurFormateur.formatPhonemes(document, para, phon);
				pos += element.length+(i-pos);
			});
			para.appendChild(document.createTextNode(paragraphe.substring(pos)));
			node.appendChild(para);
		}
	});
}

/*

*/
function lirecouleurSyllabes()
{
	var pos;
	var node = document.getElementById("lirecouleur");
	node.innerHTML = "";

	document.getElementById("lcTexte").value.split("\n").forEach(function(paragraphe, index, array) {
		var para = document.createElement('p');
		pos = 0;
		var pmots = paragraphe.match(/([a-z@àäâéèêëîïôöûùçœ'’]+)/gi);
		if (pmots !== null) {
			pmots.forEach(function(element, index, array) {
				var i = paragraphe.indexOf(element, pos);
				para.appendChild(document.createTextNode(paragraphe.substring(pos, i)));
					
				var phon = LireCouleur.extrairePhonemes(element);
				var sylls = LireCouleur.extraireSyllabes(phon);
					
				var e = document.createElement('span');
				LireCouleurFormateur.formatSyllabes(document, e, sylls);
				para.appendChild(e);
				pos += element.length+(i-pos);
			});
			para.appendChild(document.createTextNode(paragraphe.substring(pos)));
			node.appendChild(para);
		}
	});
}

/*

*/
function lirecouleurSaveCfg()
{
	var blob = new Blob([$("#lcConfig")[0].value], {
		"type": "text/plain;charset=utf8;"			
	});
	$.each($("#lcCfgEnregistrer"), function() {
		$(this)[0].setAttribute('download', 'lirecouleur.json');
		$(this)[0].setAttribute("href", window.URL.createObjectURL(blob));
	});
}

/*

*/
function lirecouleurLoadCfg()
{
	LireCouleurFormateur.fromString($("#lcConfig")[0].value);
}

/*

*/
$(document).ready(function()
{
	window.onunload = function () {
		// archiver le formatage lorsqu'on quitte la configuration
		LireCouleurFormateur.setCookies();
	}
	
	// relecture des cookies
	LireCouleurFormateur.getCookies();
	
	// initialisation du mode de présentation
	$("#tabs").tabs();
	$("#cfgtabs").tabs({
		activate: function(event, ui) {
			if (ui.newPanel.selector == "#lcConfigEdit") {
				LireCouleurFormateur.selecteur();
				$("#lcConfig")[0].value = LireCouleurFormateur.toString();
			}
		}
	});
	
	// autoriser le collage de texte dans la fenêtre de saisie
	$("#lcTexte").bind("paste", function(e){
		// access the clipboard using the api
		$(this)[0].value = e.originalEvent.clipboardData.getData('text');
	});

	// positionnement des cases à cocher en fonction de la configuration
	$.each($(".ios"), function() {
		var key = $(this)[0].id.substring(4);
		$(this)[0].checked = LireCouleurFormateur.phonemes[key];
	});
	
	// transformer l'aspect des cases à cocher pour les rendre plus jolies
	$(".ios").iosCheckbox();
	
	// insérer le sélecteur de couleurs
	$("#couleurs").colorpicker({
		defaultPalette: 'web',
		displayIndicator: false,
		transparentColor: false,
		history: false
	});
	
	// fonction déclenchée lorsqu'une couleur est sélectionnée dans le sélecteur
	$("#couleurs").on("change.color", function(event, color){
		var selectionne = $("#lcConfigTypographie").attr('selec');
		if (typeof(selectionne) !== "undefined") {
			var stl = new LireCouleurStyle(LireCouleurFormateur.couleurs[selectionne]);
			stl.dict['color'] = color;
			LireCouleurFormateur.couleurs[selectionne] = stl.toString();
			$("#cfg_"+selectionne)[0].innerHTML = '<span style="'+LireCouleurFormateur.couleurs[selectionne]+'">'+selectionne.substring(5)+'</span>';
			$("#lcCfgExemple")[0].innerHTML = '<span style="'+LireCouleurFormateur.couleurs[selectionne]+'">Sélectionné : '+selectionne.substring(5)+'</span>';
		}
	});

	// attribution de la bonne typo aux boutons de configuration
	$.each($(".lcSelecteur a"), function() {
		var id = $(this)[0].id.substring(4);
		$(this)[0].innerHTML = '<span style="'+LireCouleurFormateur.couleurs[id]+'">'+id.substring(5)+'</span>';
	});

	// fonction de réaction lorsque les boutons phonèmes sont cliqués dans la configuration
	$(".lcSelecteur a").click(function() {
		var texte = $(this)[0].id.substring(4);
		var stl = new LireCouleurStyle(LireCouleurFormateur.couleurs[texte]);
		$("#lcConfigTypographie").attr('selec', texte);
		$("#lcCfgExemple")[0].innerHTML = '<span style="'+LireCouleurFormateur.couleurs[texte]+'">Sélectionné : '+texte.substring(5)+'</span>';
	});

	// fonction de réaction lorsqu'un changement de typo est demandé (gras, oblique, ...)
	$(".lcCfg a").click(function() {
		var moi = $(this);
		var selectionne = $("#lcConfigTypographie").attr('selec');
		if (typeof(selectionne) !== "undefined") {
			var stl = new LireCouleurStyle(LireCouleurFormateur.couleurs[selectionne]);
			if (moi.attr('valeur').length > 0) {
				stl.dict[moi.attr('attribut')] = moi.attr('valeur');
			}
			else {
				delete stl.dict[moi.attr('attribut')];
			}
			LireCouleurFormateur.couleurs[selectionne] = stl.toString();
			$("#cfg_"+selectionne)[0].innerHTML = '<span style="'+LireCouleurFormateur.couleurs[selectionne]+'">'+selectionne.substring(5)+'</span>';
			$("#lcCfgExemple")[0].innerHTML = '<span style="'+LireCouleurFormateur.couleurs[selectionne]+'">Sélectionné : '+selectionne.substring(5)+'</span>';
		}
	});
});
