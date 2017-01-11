/*
    Décodage d'un élément DOM sous la forme d'une suite de syllabes
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
				pmots.forEach(function( element, index, array ) {
                    var i = paragraphe.indexOf( element, pos );
                    para.appendChild( document.createTextNode( paragraphe.substring(pos, i) ) );
                    
                    var phon = LireCouleur.extrairePhonemes( element );
                    
                    if ( mode == 's' ) {
                        var sylls = LireCouleur.extraireSyllabes( phon );
                        var e = document.createElement( 'span' );
                        LireCouleurFormateur.formatSyllabes( document, e, sylls );
                        para.appendChild(e);
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

*/
CKEDITOR.plugins.add( 'lirecouleur', {
    icons: 'config,black,phon,syll_dys,espace_m,espace_l,pdf',
    init: function( editor ) {
        var pluginDirectory = this.path;

        // ajout des scripts LireCouleur

        // https://github.com/MrRio/jsPDF
        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'jspdf.min.js' ) );

        // https://github.com/js-cookie/js-cookie
        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'js.cookie.js' ) );

        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'lirecouleur.js' ) );
        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'lirecouleur-ui.js' ) );
        CKEDITOR.scriptLoader.load( CKEDITOR.getUrl( pluginDirectory + 'lirecouleur-config.js' ) );
        
        // boite de dialogue de configuration
        editor.addCommand( 'lireCouleurDialog', new CKEDITOR.dialogCommand( 'lireCouleurDialog' ) );

        editor.addCommand( 'lc_phon', {
            exec: function( editor ) {
                // relecture des cookies
                LireCouleurFormateur.getCookies();

                // lecture du texte sélectionné
                var range = editor.getSelection().getRanges()[0].clone();
                var fragment = range.cloneContents();
                var div = document.createElement('div');
                div.appendChild( fragment.$ );
                _formatElement( div, 'p' );
                editor.insertHtml( div.innerHTML, 'text' );
            }
        });
        
        editor.addCommand( 'lc_syll_dys', {
            exec: function( editor ) {
                // relecture des cookies
                LireCouleurFormateur.getCookies();

                // lecture du texte sélectionné
                var range = editor.getSelection().getRanges()[0].clone();
                var fragment = range.cloneContents();
                var div = document.createElement('div');
                div.appendChild( fragment.$ );
                _formatElement( div, 's' );
                editor.insertHtml( div.innerHTML, 'text' );
            }
        });

        editor.addCommand( 'lc_black', {
            exec: function( editor ) {
                // lecture du texte sélectionné
                var texte = editor.getSelection().getSelectedText();
                editor.insertText( texte );
            }
        });

        editor.addCommand( 'espace_m', {
            exec: function( editor ) {
                var selection = editor.getSelection();
                var range = selection.getRanges()[0].clone();

                var sel = '<span style="word-spacing: 0.3em;">';
                var clonedSelection = range.cloneContents();
                var div = document.createElement('div');
                div.appendChild(clonedSelection.$);
                sel += div.innerHTML;
                sel += '</span>';
                
                editor.insertHtml( sel, 'text' );
            }
        });

        editor.addCommand( 'espace_l', {
            exec: function( editor ) {
                editor.getSelection().getStartElement().setStyle( 'line-height', 3);
            }
        });

        editor.addCommand( 'pdfDialog', new CKEDITOR.dialogCommand( 'pdfDialog' ) );

        editor.ui.addButton( 'Config', {
            label: 'Configuration',
            command: 'lireCouleurDialog',
            toolbar: 'styles,80'
        });

        editor.ui.addButton( 'Black', {
            label: 'Style en noir',
            command: 'lc_black',
            toolbar: 'styles,81'
        });

        editor.ui.addButton( 'Espace_m', {
            label: 'Espacer les mots',
            command: 'espace_m',
            toolbar: 'styles,82'
        });

        editor.ui.addButton( 'Espace_l', {
            label: 'Espacer les lignes',
            command: 'espace_l',
            toolbar: 'styles,83'
        });

        editor.ui.addButton( 'Phon', {
            label: 'Marquer les phonèmes',
            command: 'lc_phon',
            toolbar: 'styles,84'
        });
        
        editor.ui.addButton( 'Syll_Dys', {
            label: 'Marquer les syllabes',
            command: 'lc_syll_dys',
            toolbar: 'styles,85'
        });
        
        editor.ui.addButton( 'Pdf', {
            label: 'Exporter en PDF',
            command: 'pdfDialog',
            toolbar: 'styles,86'
        });
    }
});

