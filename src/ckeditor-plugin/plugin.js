/*
    Décodage d'un élément DOM sous la forme d'une suite de syllabes ou de phonèmes
 */
function _formatElement( elt, mode ) {
	// traitement des noeuds enfants
	for (var i=0; i<elt.childNodes.length; i+=1) {
		// traitement du noeud texte
		if ((elt.childNodes[i].nodeType == 3) || (elt.childNodes[i].nodeType == 4) || (elt.childNodes[i].nodeName == 'SPAN')) { // Text ou CDATA
			paragraphe = elt.childNodes[i].textContent;
			var pos = 0;
			var pmots = paragraphe.match(/([a-z@àäâéèêëîïôöûùçœ'’]+)/gi);
			if (pmots !== null) {
				var para = document.createElement("span");
                para.className = "lirecouleur";
				pmots.forEach(function( element, index, array ) {
                    var i = paragraphe.indexOf( element, pos );
                    para.appendChild( document.createTextNode( paragraphe.substring(pos, i) ) );
                    
                    var phon = LireCouleur.extrairePhonemes( element );
                    
                    if ( mode == 's' ) {
                        var sylls = LireCouleur.extraireSyllabes( phon );
                        LireCouleurFormateur.formatSyllabes( document, para, sylls );
                    }
                    else {
                        LireCouleurFormateur.formatPhonemes( document, para, phon );
                    }
                    
                    pos += element.length+( i-pos );
				});
				para.appendChild( document.createTextNode( paragraphe.substring(pos) ) );
				
				// remplace le texte d'origine par le texte traité
				elt.replaceChild(para, elt.childNodes[i]);
			}
		}
		else {
			_formatElement( elt.childNodes[i], mode );
		}
	}
}

/*
    Décodage d'un élément DOM sous la forme alternance de lignes
 */
function _formatLigne( editor, elt  ) {
	// traitement des noeuds enfants
    var prev = "";
	for (var i=0; i<elt.childNodes.length; i+=1) {
		// traitement du noeud texte
		if ((elt.childNodes[i].nodeType == 3) || (elt.childNodes[i].nodeType == 4) || (elt.childNodes[i].nodeName == 'SPAN')) { // Text ou CDATA
            var para = document.createElement("span");
			var paragraphe = elt.childNodes[i].textContent;
            // remplace le texte d'origine par le texte traité
            elt.replaceChild(para, elt.childNodes[i]);

			var pmots = paragraphe.split(/\s+/);
			if (pmots !== null) {
/*
Chante, ô Muse, la colère d’Achille, fils de Pélée, colère funeste, qui causa tant de malheurs aux Grecs, qui précipita dans les enfers les âmes courageuses de tant de héros, et rendit leurs corps la proie des chiens et des vautours.
 */
				var nligne = document.createElement("span");
                nligne.className = "lc_ligne_"+(LireCouleurFormateur._isyl+1).toString();
                nligne.innerHTML = pmots[0];
                para.appendChild(nligne);
                var maxHeight = editor.element.$.clientHeight;
                
                for (var j=1; j<pmots.length; j++) {
                    prev = nligne.innerHTML;
                    nligne.innerHTML += (' '+pmots[j]);

                    if (editor.element.$.clientHeight > maxHeight) {
                        nligne.innerHTML = prev;
                        para.appendChild( document.createTextNode( ' ' ) );
                        
                        nligne = document.createElement("span");
                        LireCouleurFormateur._isyl = ((LireCouleurFormateur._isyl+1) % 3);
                        nligne.className = "lc_ligne_"+(LireCouleurFormateur._isyl+1).toString();
                        nligne.innerHTML = pmots[j];
                        para.appendChild(nligne);
                        maxHeight = editor.element.$.clientHeight;
                    }
                }
             }
             LireCouleurFormateur._isyl = ((LireCouleurFormateur._isyl+1) % 3);
        } else {
            _formatLigne( editor, elt.childNodes[i] );
        }
    }
}

/*
    Élimine le formatage coloré d'un élémént DOM
 */
function _unformatElement( elt ) {
	// traitement des noeuds enfants
	for (var i=0; i<elt.childNodes.length; i+=1) {
		// traitement du noeud texte
		if ((elt.childNodes[i].nodeType == 3) || (elt.childNodes[i].nodeType == 4) || (elt.childNodes[i].nodeName == 'SPAN')) { // Text ou CDATA
			paragraphe = elt.childNodes[i].textContent;
            elt.replaceChild(document.createTextNode( paragraphe ), elt.childNodes[i]);
		}
		else {
			_unformatElement( elt.childNodes[i] );
		}
	}
}

/*

*/
CKEDITOR.plugins.add( 'lirecouleur', {
    icons: 'config,black,phon,syll_dys,lmuettes,lines',
    init: function( editor ) {
        var pluginDirectory = this.path;

        // ajout des scripts LireCouleur

        // https://github.com/js-cookie/js-cookie
        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'js.cookie.js' ) );

        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'lirecouleur.js' ) );
        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'lirecouleur-ui.js' ) );
        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'lirecouleur-config.js' ) );

        // conserver le texte à chaque nouvelle modification
        editor.on( 'change', function( evt ) {
            Cookies.remove( 'lirecouleur_txt' );
            Cookies.set( 'lirecouleur_txt', { text: evt.editor.getData() }, { expires: 365 });
        });

        // boite de dialogue de configuration
        editor.addCommand( 'lireCouleurDialog', new CKEDITOR.dialogCommand( 'lireCouleurDialog' ) );

        editor.addCommand( 'lc_phon', {
            exec: function( editor ) {
                // indication de sélection de traitement
                LireCouleurFormateur.selectTraitement(1);

                // lecture du texte sélectionné
                _formatElement( editor.element.$, 'p' );
            }
        });
        
        editor.addCommand( 'lc_syll_dys', {
            exec: function( editor ) {
                // indication de sélection de traitement
                LireCouleurFormateur.selectTraitement(2);

                // lecture du texte sélectionné
                _formatElement( editor.element.$, 's' );
            }
        });

        editor.addCommand( 'lc_black', {
            exec: function( editor ) {
                // indication de sélection de traitement
                LireCouleurFormateur.selectTraitement(0);

                _unformatElement( editor.element.$ );
            }
        });

        editor.addCommand( 'lc_lmuettes', {
            exec: function( editor ) {
                // indication de sélection de traitement
                LireCouleurFormateur.selectTraitement(3);

                // ne garder que le phonème muet dans la liste des phonèmes à mettre en évidence
                LireCouleurFormateur.setPhonMuet();
                
                // lecture du texte sélectionné
                _formatElement( editor.element.$, 'p' );

                // relecture des cookies
                LireCouleurFormateur.getCookies();
            }
        });

        editor.addCommand( 'lc_lignes', {
            exec: function( editor ) {
                // indication de sélection de traitement
                LireCouleurFormateur.selectTraitement(4);
                
                _formatLigne( editor, editor.element.$ );
            }
        });
        
        editor.ui.addButton( 'Config', {
            label: 'Configuration',
            command: 'lireCouleurDialog',
            toolbar: 'lirecouleur,1'
        });

        editor.ui.addButton( 'Black', {
            label: 'Style en noir',
            command: 'lc_black',
            toolbar: 'lirecouleur,2'
        });

        editor.ui.addButton( 'Phon', {
            label: 'Marquer les phonèmes',
            command: 'lc_phon',
            toolbar: 'lirecouleur,3'
        });
        
        editor.ui.addButton( 'Syll_Dys', {
            label: 'Marquer les syllabes',
            command: 'lc_syll_dys',
            toolbar: 'lirecouleur,4'
        });
        
        editor.ui.addButton( 'LMuettes', {
            label: 'Marquer les lettres muettes',
            command: 'lc_lmuettes',
            toolbar: 'lirecouleur,5'
        });
        
        editor.ui.addButton( 'Lines', {
            label: 'Marquer les lignes',
            command: 'lc_lignes',
            toolbar: 'lirecouleur,6'
        });
    }
});

/*
Chante, ô Muse, la colère d’Achille, fils de Pélée, colère funeste, qui causa tant de malheurs aux Grecs, qui précipita dans les enfers les âmes courageuses de tant de héros, et rendit leurs corps la proie des chiens et des vautours.
 */
