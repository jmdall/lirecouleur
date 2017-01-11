/*

*/
function mouseOverColor(hex) {
    document.body.style.cursor = "pointer";
}

function mouseOutMap() {
    document.body.style.cursor = "";
}

function clickColor(colorhex, seltop, selleft) {
    var colormap, areas, cc, i, areacolor, cc;
    if ((!seltop || seltop == -1) && (!selleft || selleft == -1)) {
        colormap = document.getElementById("colormap");
        areas = colormap.getElementsByTagName("AREA");
        for (i = 0; i < areas.length; i++) {
            areacolor = areas[i].getAttribute("onmouseover").replace('mouseOverColor("', '');
            areacolor = areacolor.replace('")', '');
            if (areacolor.toLowerCase() == colorhex) {
                cc = areas[i].getAttribute("onclick").replace(')', '').split(",");
                seltop = Number(cc[1]);
                selleft = Number(cc[2]);
            }
        }
    }
    if ((seltop+200)>-1 && selleft>-1) {
        document.getElementById("selectedhexagon").style.top=seltop + "px";
        document.getElementById("selectedhexagon").style.left=selleft + "px";
        document.getElementById("selectedhexagon").style.visibility="visible";
        
        var config = CKEDITOR.config.lirecouleur;
        if (config['phonid'].length > 0) {
            config['color'] = colorhex;
            LireCouleurFormateur.couleurs[config['phonid']] = assembleStyle( config );
            document.getElementById( config['apercu'] ).style.color = colorhex;
        }
	} else {
        document.getElementById("selectedhexagon").style.visibility = "hidden";
	}
}

CKEDITOR.config.lirecouleur = {'color':'', 'font-style':'', 'font-weigth':'', 'font-family':'', 'text-decoration':'', 'phonid':'', 'apercu':''};

/*

*/
function assembleStyle( stl ) 
{
    var arr = new Array();
    for (var key in stl) {
        if (( stl[key].length > 0 ) && ( key != 'phonid' ) && ( key != 'apercu' )) {
            arr.push(key+': '+stl[key]);
        }
    }
    var res = arr.join("; ")+';';
    delete arr;
    return res;
}

/*

*/
CKEDITOR.dialog.add( 'lireCouleurDialog', function( editor )
{
    return {
        title : 'Propriétés LireCouleur',
        minWidth : 400,
        minHeight : 200,
        contents : [
        { id : 'general',
            label : 'Sélection des phonèmes',
            elements : [
            { type: 'html', html: '<div style="font-weight: bold; font-size:120%;">Cocher les phonèmes à mettre en évidence</div>' },
            { type: 'hbox',
                widths: [ '33%', '33%', '33%' ],
                children: [
                { type: 'vbox',
                    children : [
                    { type : 'checkbox',
                        id : 'checkA',
                        label : '[a] ta',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_a'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkQ',
                        label : '[e] le',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_e'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkI',
                        label : '[i] il',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_i'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkY',
                        label : '[y] tu',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_u'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkH',
                        label : '[#] lettre muette',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_muet'] ); }
                    }
                ] },
                { type: 'vbox',
                    children :
                    [ { type : 'checkbox',
                        id : 'checkU',
                        label : '[u] fou',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_ou'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkE',
                        label : '[é] né',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_ez'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkO',
                        label : '[o] mot',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_o'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkEt',
                        label : '[è] sel',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_et'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkEu',
                        label : '[eu] feu',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_eu'] ); }
                    }
                ] },
                { type: 'vbox',
                    children : [
                    { type : 'checkbox',
                        id : 'checkAn',
                        label : '[an] grand',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_an'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkOn',
                        label : '[on] son',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_on'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkIn',
                        label : '[in] fin',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_in'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkW',
                        label : '[w] ouate',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_w'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkJ',
                        label : '[j] fille',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_y'] ); }
                    }
                ] }
            ] },
            { type: 'html', html: '<div>&nbsp;</div>' },
            { type: 'hbox',
                width: [ '25%', '25%', '25%', '25%' ],
                children: [
                { type: 'vbox',
                    children : [
                    { type : 'checkbox',
                        id : 'checkL',
                        label : '[l] lilas',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_l'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkV',
                        label : '[v] vélo',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_v'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkF',
                        label : '[f] fil',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_f'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkP',
                        label : '[p] pile',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_p'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkB',
                        label : '[b] bébé',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_b'] ); }
                    }
                ] },
                { type: 'vbox',
                    children : [
                    { type : 'checkbox',
                        id : 'checkM',
                        label : '[m] mémé',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_m'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkZ',
                        label : '[z] zoo',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_z'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkS',
                        label : '[s] saucisse',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_s'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkT',
                        label : '[t] tortue',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_t'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkD',
                        label : '[d] dindon',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_d'] ); }
                    }
                ] },
                { type: 'vbox',
                    children : [
                    { type : 'checkbox',
                        id : 'checkN',
                        label : '[n] âne',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_n'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkGe',
                        label : '[ge] jupe',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_ge'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkCh',
                        label : '[ch] chat',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_ch'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkK',
                        label : '[k] coq',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_k'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkG',
                        label : '[g] gare',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_g'] ); }
                    }
                ] },
                { type: 'vbox',
                    children : [
                    { type : 'checkbox',
                        id : 'checkR',
                        label : '[r] rat',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_r'] ); }
                    }
                ] }
            ] },
            { type: 'html', html: '<div>&nbsp;</div>' },
            { type: 'hbox',
                width: [ '25%', '25%', '25%', '25%' ],
                children: [
                    { type : 'checkbox',
                        id : 'checkNg',
                        label : '[ng] parking',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_ng'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkGn',
                        label : '[gn] ligne',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_gn'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkKs',
                        label : '[ks] ksi',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_ks'] ); }
                    },
                    { type : 'checkbox',
                        id : 'checkGz',
                        label : '[gz] exact',
                        setup : function( element ) { this.setValue( LireCouleurFormateur.phonemes['phon_gz'] ); }
                    }
                ] }
            ] },
        { id : 'stylphon',
            label : 'Styles de caractères',
            elements : [
                { type: 'html', html: '<div style="font-weight: bold; font-size:120%;">Édition des styles de caractères</div>' },
                { type: 'html',
                    id : 'apercu',
                    html: '<div style="text-align: center; font-size: 150%;">Lorem ipsum</div>'
                },
                { type : 'select',
                    id : 'phonid',
                    label : 'Choix du style de caractères',
                    items : [ [' ', ''],
                        ['[a] ta', 'phon_a'], ['[e] le', 'phon_e'], ['[i] il', 'phon_i'], ['[u] tu', 'phon_u'], ['[#] lettre muette', 'phon_muet'],
                        ['[ou] fou', 'phon_ou'], ['[é] né', 'phon_ez'], ['[o] mot', 'phon_o'], ['[è] sel', 'phon_et'], ['[eu] feu', 'phon_eu'],
                        ['[an] grand', 'phon_an'], ['[on] son', 'phon_on'], ['[in] fin', 'phon_in'], ['[w] ouate', 'phon_w'], ['[j] fille', 'phon_y'],
                        ['[l] lilas', 'phon_l'], ['[l] lilas', 'phon_l'], ['[v] vélo', 'phon_v'], ['[f] fil', 'phon_f'], ['[p] pile', 'phon_p'], ['[b] bébé', 'phon_b'],
                        ['[m] mémé', 'phon_m'], ['[z] zoo', 'phon_z'], ['[s] saucisse', 'phon_s'], ['[t] tortue', 'phon_t'], ['[d] dindon', 'phon_d'],
                        ['[n] âne', 'phon_n'], ['[ge] jupe', 'phon_ge'], ['[ch] chat', 'phon_ch'], ['[k] coq', 'phon_k'], ['[g] gare', 'phon_g'],
                        ['[r] rat', 'phon_r'], ['[ng] parking', 'phon_ng'], ['[gn] ligne', 'phon_gn'], ['[ks] ksi', 'phon_ks'], ['[gz] exact', 'phon_gz'],
                        ['Syllabe 1', 'syl_1'], ['Syllabe 2', 'syl_2'], ['Syllabe 3', 'syl_3']
                    ],
                    onChange : function ( api ) {
                        var dialog = this.getDialog();
                        var phon = this.getValue();
                        
                        if (phon.length > 0) {
                            dialog.getContentElement( 'stylphon', 'imagemap' ).enable();
                            dialog.getContentElement( 'stylphon', 'italique' ).enable();
                            dialog.getContentElement( 'stylphon', 'gras' ).enable();
                            dialog.getContentElement( 'stylphon', 'famille' ).enable();
                            dialog.getContentElement( 'stylphon', 'souligne' ).enable();
                            dialog.getContentElement( 'stylphon', 'surligne' ).enable();

                            var t_styles = LireCouleurFormateur.couleurs[phon].split( ';' );
                            editor.config.lirecouleur['phonid'] = phon;
                            
                            var apercu = dialog.getContentElement( 'stylphon', 'apercu' ).getElement();
                            editor.config.lirecouleur['apercu'] = apercu.getId();
                            for(var key in editor.config.lirecouleur) {
                                apercu.removeStyle(key);
                            }
                            dialog.setValueOf( 'stylphon', 'italique', false);
                            dialog.setValueOf( 'stylphon', 'gras', false);
                            dialog.setValueOf( 'stylphon', 'famille', false);
                            dialog.setValueOf( 'stylphon', 'souligne', false);
                            dialog.setValueOf( 'stylphon', 'surligne', false);
                            for(var i in t_styles) {
                                var cpl = t_styles[i].split( ':' );
                                if (cpl.length == 2) {
                                    var attr = cpl[0].trim(),
                                        val = cpl[1].trim();
                                    if (attr == 'font-style') {
                                        dialog.setValueOf( 'stylphon', 'italique', ((val == 'italic') || (val == 'oblique')));
                                    }
                                    else if (attr == 'font-weight') {
                                        dialog.setValueOf( 'stylphon', 'gras', (val == 'bold'));
                                    }
                                    else if (attr == 'font-family') {
                                        dialog.setValueOf( 'stylphon', 'famille', (val == 'serif'));
                                    }
                                    else if (attr == 'text-decoration') {
                                        dialog.setValueOf( 'stylphon', 'souligne', (val.indexOf( 'underline' ) >= 0));
                                        dialog.setValueOf( 'stylphon', 'surligne', (val.indexOf( 'overline' ) >= 0));
                                    }
                                    apercu.setStyle( attr, val );
                                    editor.config.lirecouleur[attr] = val;
                                }
                            }
                        } else {
                            dialog.getContentElement( 'stylphon', 'imagemap' ).disable();
                            dialog.getContentElement( 'stylphon', 'italique' ).disable();
                            dialog.getContentElement( 'stylphon', 'gras' ).disable();
                            dialog.getContentElement( 'stylphon', 'famille' ).disable();
                            dialog.getContentElement( 'stylphon', 'souligne' ).disable();
                            dialog.getContentElement( 'stylphon', 'surligne' ).disable();
                        }
                    }
                },
                { type : 'html',
                    id : 'imagemap',
                    html : '<div>imagemap</div>',
                    onShow : function() {
                        var path = editor.plugins.lirecouleur.path + 'images/';
                        var imagemap = '<div style="margin:auto;width:236px;"> <img style=\'margin-right:2px;\' src=\''+path+'img_colormap.gif\' usemap=\'#colormap\' alt=\'colormap\' /><map id=\'colormap\' name=\'colormap\' onmouseout=\'mouseOutMap()\'><area style=\'cursor:pointer\' shape=\'poly\' coords=\'63,0,72,4,72,15,63,19,54,15,54,4\' onclick=\'clickColor("#003366",-200,54)\' onmouseover=\'mouseOverColor("#003366")\' alt=\'#003366\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'81,0,90,4,90,15,81,19,72,15,72,4\' onclick=\'clickColor("#336699",-200,72)\' onmouseover=\'mouseOverColor("#336699")\' alt=\'#336699\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'99,0,108,4,108,15,99,19,90,15,90,4\' onclick=\'clickColor("#3366CC",-200,90)\' alt=\'#3366CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'117,0,126,4,126,15,117,19,108,15,108,4\' onclick=\'clickColor("#003399",-200,108)\' onmouseover=\'mouseOverColor("#003399")\' alt=\'#003399\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'135,0,144,4,144,15,135,19,126,15,126,4\' onclick=\'clickColor("#000099",-200,126)\' onmouseover=\'mouseOverColor("#000099")\' alt=\'#000099\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'153,0,162,4,162,15,153,19,144,15,144,4\' onclick=\'clickColor("#0000CC",-200,144)\' onmouseover=\'mouseOverColor("#0000CC")\' alt=\'#0000CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'171,0,180,4,180,15,171,19,162,15,162,4\' onclick=\'clickColor("#000066",-200,162)\' onmouseover=\'mouseOverColor("#000066")\' alt=\'#000066\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'54,15,63,19,63,30,54,34,45,30,45,19\' onclick=\'clickColor("#006666",-185,45)\' onmouseover=\'mouseOverColor("#006666")\' alt=\'#006666\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'72,15,81,19,81,30,72,34,63,30,63,19\' onclick=\'clickColor("#006699",-185,63)\' onmouseover=\'mouseOverColor("#006699")\' alt=\'#006699\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'90,15,99,19,99,30,90,34,81,30,81,19\' onclick=\'clickColor("#0099CC",-185,81)\' onmouseover=\'mouseOverColor("#0099CC")\' alt=\'#0099CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'108,15,117,19,117,30,108,34,99,30,99,19\' onclick=\'clickColor("#0066CC",-185,99)\' onmouseover=\'mouseOverColor("#0066CC")\' alt=\'#0066CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'126,15,135,19,135,30,126,34,117,30,117,19\' onclick=\'clickColor("#0033CC",-185,117)\' onmouseover=\'mouseOverColor("#0033CC")\' alt=\'#0033CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'144,15,153,19,153,30,144,34,135,30,135,19\' onclick=\'clickColor("#0000FF",-185,135)\' onmouseover=\'mouseOverColor("#0000FF")\' alt=\'#0000FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'162,15,171,19,171,30,162,34,153,30,153,19\' onclick=\'clickColor("#3333FF",-185,153)\' onmouseover=\'mouseOverColor("#3333FF")\' alt=\'#3333FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'180,15,189,19,189,30,180,34,171,30,171,19\' onclick=\'clickColor("#333399",-185,171)\' onmouseover=\'mouseOverColor("#333399")\' alt=\'#333399\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'45,30,54,34,54,45,45,49,36,45,36,34\' onclick=\'clickColor("#669999",-170,36)\' onmouseover=\'mouseOverColor("#669999")\' alt=\'#669999\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'63,30,72,34,72,45,63,49,54,45,54,34\' onclick=\'clickColor("#009999",-170,54)\' onmouseover=\'mouseOverColor("#009999")\' alt=\'#009999\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'81,30,90,34,90,45,81,49,72,45,72,34\' onclick=\'clickColor("#33CCCC",-170,72)\' onmouseover=\'mouseOverColor("#33CCCC")\' alt=\'#33CCCC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'99,30,108,34,108,45,99,49,90,45,90,34\' onclick=\'clickColor("#00CCFF",-170,90)\' onmouseover=\'mouseOverColor("#00CCFF")\' alt=\'#00CCFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'117,30,126,34,126,45,117,49,108,45,108,34\' onclick=\'clickColor("#0099FF",-170,108)\' onmouseover=\'mouseOverColor("#0099FF")\' alt=\'#0099FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'135,30,144,34,144,45,135,49,126,45,126,34\' onclick=\'clickColor("#0066FF",-170,126)\' onmouseover=\'mouseOverColor("#0066FF")\' alt=\'#0066FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'153,30,162,34,162,45,153,49,144,45,144,34\' onclick=\'clickColor("#3366FF",-170,144)\' onmouseover=\'mouseOverColor("#3366FF")\' alt=\'#3366FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'171,30,180,34,180,45,171,49,162,45,162,34\' onclick=\'clickColor("#3333CC",-170,162)\' onmouseover=\'mouseOverColor("#3333CC")\' alt=\'#3333CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'189,30,198,34,198,45,189,49,180,45,180,34\' onclick=\'clickColor("#666699",-170,180)\' onmouseover=\'mouseOverColor("#666699")\' alt=\'#666699\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'36,45,45,49,45,60,36,64,27,60,27,49\' onclick=\'clickColor("#339966",-155,27)\' onmouseover=\'mouseOverColor("#339966")\' alt=\'#339966\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'54,45,63,49,63,60,54,64,45,60,45,49\' onclick=\'clickColor("#00CC99",-155,45)\' onmouseover=\'mouseOverColor("#00CC99")\' alt=\'#00CC99\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'72,45,81,49,81,60,72,64,63,60,63,49\' onclick=\'clickColor("#00FFCC",-155,63)\' onmouseover=\'mouseOverColor("#00FFCC")\' alt=\'#00FFCC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'90,45,99,49,99,60,90,64,81,60,81,49\' onclick=\'clickColor("#00FFFF",-155,81)\' onmouseover=\'mouseOverColor("#00FFFF")\' alt=\'#00FFFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'108,45,117,49,117,60,108,64,99,60,99,49\' onclick=\'clickColor("#33CCFF",-155,99)\' onmouseover=\'mouseOverColor("#33CCFF")\' alt=\'#33CCFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'126,45,135,49,135,60,126,64,117,60,117,49\' onclick=\'clickColor("#3399FF",-155,117)\' onmouseover=\'mouseOverColor("#3399FF")\' alt=\'#3399FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'144,45,153,49,153,60,144,64,135,60,135,49\' onclick=\'clickColor("#6699FF",-155,135)\' onmouseover=\'mouseOverColor("#6699FF")\' alt=\'#6699FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'162,45,171,49,171,60,162,64,153,60,153,49\' onclick=\'clickColor("#6666FF",-155,153)\' onmouseover=\'mouseOverColor("#6666FF")\' alt=\'#6666FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'180,45,189,49,189,60,180,64,171,60,171,49\' onclick=\'clickColor("#6600FF",-155,171)\' onmouseover=\'mouseOverColor("#6600FF")\' alt=\'#6600FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'198,45,207,49,207,60,198,64,189,60,189,49\' onclick=\'clickColor("#6600CC",-155,189)\' onmouseover=\'mouseOverColor("#6600CC")\' alt=\'#6600CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'27,60,36,64,36,75,27,79,18,75,18,64\' onclick=\'clickColor("#339933",-140,18)\' onmouseover=\'mouseOverColor("#339933")\' alt=\'#339933\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'45,60,54,64,54,75,45,79,36,75,36,64\' onclick=\'clickColor("#00CC66",-140,36)\' onmouseover=\'mouseOverColor("#00CC66")\' alt=\'#00CC66\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'63,60,72,64,72,75,63,79,54,75,54,64\' onclick=\'clickColor("#00FF99",-140,54)\' onmouseover=\'mouseOverColor("#00FF99")\' alt=\'#00FF99\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'81,60,90,64,90,75,81,79,72,75,72,64\' onclick=\'clickColor("#66FFCC",-140,72)\' onmouseover=\'mouseOverColor("#66FFCC")\' alt=\'#66FFCC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'99,60,108,64,108,75,99,79,90,75,90,64\' onclick=\'clickColor("#66FFFF",-140,90)\' onmouseover=\'mouseOverColor("#66FFFF")\' alt=\'#66FFFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'117,60,126,64,126,75,117,79,108,75,108,64\' onclick=\'clickColor("#66CCFF",-140,108)\' onmouseover=\'mouseOverColor("#66CCFF")\' alt=\'#66CCFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'135,60,144,64,144,75,135,79,126,75,126,64\' onclick=\'clickColor("#99CCFF",-140,126)\' onmouseover=\'mouseOverColor("#99CCFF")\' alt=\'#99CCFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'153,60,162,64,162,75,153,79,144,75,144,64\' onclick=\'clickColor("#9999FF",-140,144)\' onmouseover=\'mouseOverColor("#9999FF")\' alt=\'#9999FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'171,60,180,64,180,75,171,79,162,75,162,64\' onclick=\'clickColor("#9966FF",-140,162)\' onmouseover=\'mouseOverColor("#9966FF")\' alt=\'#9966FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'189,60,198,64,198,75,189,79,180,75,180,64\' onclick=\'clickColor("#9933FF",-140,180)\' onmouseover=\'mouseOverColor("#9933FF")\' alt=\'#9933FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'207,60,216,64,216,75,207,79,198,75,198,64\' onclick=\'clickColor("#9900FF",-140,198)\' onmouseover=\'mouseOverColor("#9900FF")\' alt=\'#9900FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'18,75,27,79,27,90,18,94,9,90,9,79\' onclick=\'clickColor("#006600",-125,9)\' onmouseover=\'mouseOverColor("#006600")\' alt=\'#006600\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'36,75,45,79,45,90,36,94,27,90,27,79\' onclick=\'clickColor("#00CC00",-125,27)\' onmouseover=\'mouseOverColor("#00CC00")\' alt=\'#00CC00\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'54,75,63,79,63,90,54,94,45,90,45,79\' onclick=\'clickColor("#00FF00",-125,45)\' onmouseover=\'mouseOverColor("#00FF00")\' alt=\'#00FF00\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'72,75,81,79,81,90,72,94,63,90,63,79\' onclick=\'clickColor("#66FF99",-125,63)\' onmouseover=\'mouseOverColor("#66FF99")\' alt=\'#66FF99\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'90,75,99,79,99,90,90,94,81,90,81,79\' onclick=\'clickColor("#99FFCC",-125,81)\' onmouseover=\'mouseOverColor("#99FFCC")\' alt=\'#99FFCC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'108,75,117,79,117,90,108,94,99,90,99,79\' onclick=\'clickColor("#CCFFFF",-125,99)\' onmouseover=\'mouseOverColor("#CCFFFF")\' alt=\'#CCFFFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'126,75,135,79,135,90,126,94,117,90,117,79\' onclick=\'clickColor("#CCCCFF",-125,117)\' onmouseover=\'mouseOverColor("#CCCCFF")\' alt=\'#CCCCFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'144,75,153,79,153,90,144,94,135,90,135,79\' onclick=\'clickColor("#CC99FF",-125,135)\' onmouseover=\'mouseOverColor("#CC99FF")\' alt=\'#CC99FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'162,75,171,79,171,90,162,94,153,90,153,79\' onclick=\'clickColor("#CC66FF",-125,153)\' onmouseover=\'mouseOverColor("#CC66FF")\' alt=\'#CC66FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'180,75,189,79,189,90,180,94,171,90,171,79\' onclick=\'clickColor("#CC33FF",-125,171)\' onmouseover=\'mouseOverColor("#CC33FF")\' alt=\'#CC33FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'198,75,207,79,207,90,198,94,189,90,189,79\' onclick=\'clickColor("#CC00FF",-125,189)\' onmouseover=\'mouseOverColor("#CC00FF")\' alt=\'#CC00FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'216,75,225,79,225,90,216,94,207,90,207,79\' onclick=\'clickColor("#9900CC",-125,207)\' onmouseover=\'mouseOverColor("#9900CC")\' alt=\'#9900CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'9,90,18,94,18,105,9,109,0,105,0,94\' onclick=\'clickColor("#003300",-110,0)\' onmouseover=\'mouseOverColor("#003300")\' alt=\'#003300\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'27,90,36,94,36,105,27,109,18,105,18,94\' onclick=\'clickColor("#009933",-110,18)\' onmouseover=\'mouseOverColor("#009933")\' alt=\'#009933\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'45,90,54,94,54,105,45,109,36,105,36,94\' onclick=\'clickColor("#33CC33",-110,36)\' onmouseover=\'mouseOverColor("#33CC33")\' alt=\'#33CC33\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'63,90,72,94,72,105,63,109,54,105,54,94\' onclick=\'clickColor("#66FF66",-110,54)\' onmouseover=\'mouseOverColor("#66FF66")\' alt=\'#66FF66\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'81,90,90,94,90,105,81,109,72,105,72,94\' onclick=\'clickColor("#99FF99",-110,72)\' onmouseover=\'mouseOverColor("#99FF99")\' alt=\'#99FF99\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'99,90,108,94,108,105,99,109,90,105,90,94\' onclick=\'clickColor("#CCFFCC",-110,90)\' onmouseover=\'mouseOverColor("#CCFFCC")\' alt=\'#CCFFCC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'117,90,126,94,126,105,117,109,108,105,108,94\' onclick=\'clickColor("#FFFFFF",-110,108)\' onmouseover=\'mouseOverColor("#FFFFFF")\' alt=\'#FFFFFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'135,90,144,94,144,105,135,109,126,105,126,94\' onclick=\'clickColor("#FFCCFF",-110,126)\' onmouseover=\'mouseOverColor("#FFCCFF")\' alt=\'#FFCCFF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'153,90,162,94,162,105,153,109,144,105,144,94\' onclick=\'clickColor("#FF99FF",-110,144)\' onmouseover=\'mouseOverColor("#FF99FF")\' alt=\'#FF99FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'171,90,180,94,180,105,171,109,162,105,162,94\' onclick=\'clickColor("#FF66FF",-110,162)\' onmouseover=\'mouseOverColor("#FF66FF")\' alt=\'#FF66FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'189,90,198,94,198,105,189,109,180,105,180,94\' onclick=\'clickColor("#FF00FF",-110,180)\' onmouseover=\'mouseOverColor("#FF00FF")\' alt=\'#FF00FF\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'207,90,216,94,216,105,207,109,198,105,198,94\' onclick=\'clickColor("#CC00CC",-110,198)\' onmouseover=\'mouseOverColor("#CC00CC")\' alt=\'#CC00CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'225,90,234,94,234,105,225,109,216,105,216,94\' onclick=\'clickColor("#660066",-110,216)\' onmouseover=\'mouseOverColor("#660066")\' alt=\'#660066\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'18,105,27,109,27,120,18,124,9,120,9,109\' onclick=\'clickColor("#336600",-95,9)\' onmouseover=\'mouseOverColor("#336600")\' alt=\'#336600\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'36,105,45,109,45,120,36,124,27,120,27,109\' onclick=\'clickColor("#009900",-95,27)\' onmouseover=\'mouseOverColor("#009900")\' alt=\'#009900\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'54,105,63,109,63,120,54,124,45,120,45,109\' onclick=\'clickColor("#66FF33",-95,45)\' onmouseover=\'mouseOverColor("#66FF33")\' alt=\'#66FF33\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'72,105,81,109,81,120,72,124,63,120,63,109\' onclick=\'clickColor("#99FF66",-95,63)\' onmouseover=\'mouseOverColor("#99FF66")\' alt=\'#99FF66\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'90,105,99,109,99,120,90,124,81,120,81,109\' onclick=\'clickColor("#CCFF99",-95,81)\' onmouseover=\'mouseOverColor("#CCFF99")\' alt=\'#CCFF99\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'108,105,117,109,117,120,108,124,99,120,99,109\' onclick=\'clickColor("#FFFFCC",-95,99)\' onmouseover=\'mouseOverColor("#FFFFCC")\' alt=\'#FFFFCC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'126,105,135,109,135,120,126,124,117,120,117,109\' onclick=\'clickColor("#FFCCCC",-95,117)\' onmouseover=\'mouseOverColor("#FFCCCC")\' alt=\'#FFCCCC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'144,105,153,109,153,120,144,124,135,120,135,109\' onclick=\'clickColor("#FF99CC",-95,135)\' onmouseover=\'mouseOverColor("#FF99CC")\' alt=\'#FF99CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'162,105,171,109,171,120,162,124,153,120,153,109\' onclick=\'clickColor("#FF66CC",-95,153)\' onmouseover=\'mouseOverColor("#FF66CC")\' alt=\'#FF66CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'180,105,189,109,189,120,180,124,171,120,171,109\' onclick=\'clickColor("#FF33CC",-95,171)\' onmouseover=\'mouseOverColor("#FF33CC")\' alt=\'#FF33CC\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'198,105,207,109,207,120,198,124,189,120,189,109\' onclick=\'clickColor("#CC0099",-95,189)\' onmouseover=\'mouseOverColor("#CC0099")\' alt=\'#CC0099\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'216,105,225,109,225,120,216,124,207,120,207,109\' onclick=\'clickColor("#993399",-95,207)\' onmouseover=\'mouseOverColor("#993399")\' alt=\'#993399\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'27,120,36,124,36,135,27,139,18,135,18,124\' onclick=\'clickColor("#333300",-80,18)\' onmouseover=\'mouseOverColor("#333300")\' alt=\'#333300\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'45,120,54,124,54,135,45,139,36,135,36,124\' onclick=\'clickColor("#669900",-80,36)\' onmouseover=\'mouseOverColor("#669900")\' alt=\'#669900\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'63,120,72,124,72,135,63,139,54,135,54,124\' onclick=\'clickColor("#99FF33",-80,54)\' onmouseover=\'mouseOverColor("#99FF33")\' alt=\'#99FF33\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'81,120,90,124,90,135,81,139,72,135,72,124\' onclick=\'clickColor("#CCFF66",-80,72)\' onmouseover=\'mouseOverColor("#CCFF66")\' alt=\'#CCFF66\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'99,120,108,124,108,135,99,139,90,135,90,124\' onclick=\'clickColor("#FFFF99",-80,90)\' onmouseover=\'mouseOverColor("#FFFF99")\' alt=\'#FFFF99\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'117,120,126,124,126,135,117,139,108,135,108,124\' onclick=\'clickColor("#FFCC99",-80,108)\' onmouseover=\'mouseOverColor("#FFCC99")\' alt=\'#FFCC99\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'135,120,144,124,144,135,135,139,126,135,126,124\' onclick=\'clickColor("#FF9999",-80,126)\' onmouseover=\'mouseOverColor("#FF9999")\' alt=\'#FF9999\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'153,120,162,124,162,135,153,139,144,135,144,124\' onclick=\'clickColor("#FF6699",-80,144)\' onmouseover=\'mouseOverColor("#FF6699")\' alt=\'#FF6699\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'171,120,180,124,180,135,171,139,162,135,162,124\' onclick=\'clickColor("#FF3399",-80,162)\' onmouseover=\'mouseOverColor("#FF3399")\' alt=\'#FF3399\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'189,120,198,124,198,135,189,139,180,135,180,124\' onclick=\'clickColor("#CC3399",-80,180)\' onmouseover=\'mouseOverColor("#CC3399")\' alt=\'#CC3399\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'207,120,216,124,216,135,207,139,198,135,198,124\' onclick=\'clickColor("#990099",-80,198)\' onmouseover=\'mouseOverColor("#990099")\' alt=\'#990099\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'36,135,45,139,45,150,36,154,27,150,27,139\' onclick=\'clickColor("#666633",-65,27)\' onmouseover=\'mouseOverColor("#666633")\' alt=\'#666633\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'54,135,63,139,63,150,54,154,45,150,45,139\' onclick=\'clickColor("#99CC00",-65,45)\' onmouseover=\'mouseOverColor("#99CC00")\' alt=\'#99CC00\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'72,135,81,139,81,150,72,154,63,150,63,139\' onclick=\'clickColor("#CCFF33",-65,63)\' onmouseover=\'mouseOverColor("#CCFF33")\' alt=\'#CCFF33\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'90,135,99,139,99,150,90,154,81,150,81,139\' onclick=\'clickColor("#FFFF66",-65,81)\' onmouseover=\'mouseOverColor("#FFFF66")\' alt=\'#FFFF66\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'108,135,117,139,117,150,108,154,99,150,99,139\' onclick=\'clickColor("#FFCC66",-65,99)\' onmouseover=\'mouseOverColor("#FFCC66")\' alt=\'#FFCC66\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'126,135,135,139,135,150,126,154,117,150,117,139\' onclick=\'clickColor("#FF9966",-65,117)\' onmouseover=\'mouseOverColor("#FF9966")\' alt=\'#FF9966\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'144,135,153,139,153,150,144,154,135,150,135,139\' onclick=\'clickColor("#FF6666",-65,135)\' onmouseover=\'mouseOverColor("#FF6666")\' alt=\'#FF6666\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'162,135,171,139,171,150,162,154,153,150,153,139\' onclick=\'clickColor("#FF0066",-65,153)\' onmouseover=\'mouseOverColor("#FF0066")\' alt=\'#FF0066\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'180,135,189,139,189,150,180,154,171,150,171,139\' onclick=\'clickColor("#CC6699",-65,171)\' onmouseover=\'mouseOverColor("#CC6699")\' alt=\'#CC6699\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'198,135,207,139,207,150,198,154,189,150,189,139\' onclick=\'clickColor("#993366",-65,189)\' onmouseover=\'mouseOverColor("#993366")\' alt=\'#993366\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'45,150,54,154,54,165,45,169,36,165,36,154\' onclick=\'clickColor("#999966",-50,36)\' onmouseover=\'mouseOverColor("#999966")\' alt=\'#999966\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'63,150,72,154,72,165,63,169,54,165,54,154\' onclick=\'clickColor("#CCCC00",-50,54)\' onmouseover=\'mouseOverColor("#CCCC00")\' alt=\'#CCCC00\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'81,150,90,154,90,165,81,169,72,165,72,154\' onclick=\'clickColor("#FFFF00",-50,72)\' onmouseover=\'mouseOverColor("#FFFF00")\' alt=\'#FFFF00\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'99,150,108,154,108,165,99,169,90,165,90,154\' onclick=\'clickColor("#FFCC00",-50,90)\' onmouseover=\'mouseOverColor("#FFCC00")\' alt=\'#FFCC00\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'117,150,126,154,126,165,117,169,108,165,108,154\' onclick=\'clickColor("#FF9933",-50,108)\' onmouseover=\'mouseOverColor("#FF9933")\' alt=\'#FF9933\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'135,150,144,154,144,165,135,169,126,165,126,154\' onclick=\'clickColor("#FF6600",-50,126)\' onmouseover=\'mouseOverColor("#FF6600")\' alt=\'#FF6600\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'153,150,162,154,162,165,153,169,144,165,144,154\' onclick=\'clickColor("#FF5050",-50,144)\' onmouseover=\'mouseOverColor("#FF5050")\' alt=\'#FF5050\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'171,150,180,154,180,165,171,169,162,165,162,154\' onclick=\'clickColor("#CC0066",-50,162)\' onmouseover=\'mouseOverColor("#CC0066")\' alt=\'#CC0066\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'189,150,198,154,198,165,189,169,180,165,180,154\' onclick=\'clickColor("#660033",-50,180)\' onmouseover=\'mouseOverColor("#660033")\' alt=\'#660033\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'54,165,63,169,63,180,54,184,45,180,45,169\' onclick=\'clickColor("#996633",-35,45)\' onmouseover=\'mouseOverColor("#996633")\' alt=\'#996633\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'72,165,81,169,81,180,72,184,63,180,63,169\' onclick=\'clickColor("#CC9900",-35,63)\' onmouseover=\'mouseOverColor("#CC9900")\' alt=\'#CC9900\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'90,165,99,169,99,180,90,184,81,180,81,169\' onclick=\'clickColor("#FF9900",-35,81)\' onmouseover=\'mouseOverColor("#FF9900")\' alt=\'#FF9900\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'108,165,117,169,117,180,108,184,99,180,99,169\' onclick=\'clickColor("#CC6600",-35,99)\' onmouseover=\'mouseOverColor("#CC6600")\' alt=\'#CC6600\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'126,165,135,169,135,180,126,184,117,180,117,169\' onclick=\'clickColor("#FF3300",-35,117)\' onmouseover=\'mouseOverColor("#FF3300")\' alt=\'#FF3300\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'144,165,153,169,153,180,144,184,135,180,135,169\' onclick=\'clickColor("#FF0000",-35,135)\' onmouseover=\'mouseOverColor("#FF0000")\' alt=\'#FF0000\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'162,165,171,169,171,180,162,184,153,180,153,169\' onclick=\'clickColor("#CC0000",-35,153)\' onmouseover=\'mouseOverColor("#CC0000")\' alt=\'#CC0000\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'180,165,189,169,189,180,180,184,171,180,171,169\' onclick=\'clickColor("#990033",-35,171)\' onmouseover=\'mouseOverColor("#990033")\' alt=\'#990033\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'63,180,72,184,72,195,63,199,54,195,54,184\' onclick=\'clickColor("#663300",-20,54)\' onmouseover=\'mouseOverColor("#663300")\' alt=\'#663300\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'81,180,90,184,90,195,81,199,72,195,72,184\' onclick=\'clickColor("#996600",-20,72)\' onmouseover=\'mouseOverColor("#996600")\' alt=\'#996600\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'99,180,108,184,108,195,99,199,90,195,90,184\' onclick=\'clickColor("#CC3300",-20,90)\' onmouseover=\'mouseOverColor("#CC3300")\' alt=\'#CC3300\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'117,180,126,184,126,195,117,199,108,195,108,184\' onclick=\'clickColor("#993300",-20,108)\' onmouseover=\'mouseOverColor("#993300")\' alt=\'#993300\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'135,180,144,184,144,195,135,199,126,195,126,184\' onclick=\'clickColor("#990000",-20,126)\' onmouseover=\'mouseOverColor("#990000")\' alt=\'#990000\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'153,180,162,184,162,195,153,199,144,195,144,184\' onclick=\'clickColor("#800000",-20,144)\' onmouseover=\'mouseOverColor("#800000")\' alt=\'#800000\' /><area style=\'cursor:pointer\' shape=\'poly\' coords=\'171,180,180,184,180,195,171,199,162,195,162,184\' onclick=\'clickColor("#993333",-20,162)\' onmouseover=\'mouseOverColor("#993333")\' alt=\'#993333\' /></map><script>var thistop = "-35"; var thisleft = "135";	</script><div id=\'selectedhexagon\' style=\'visibility:hidden;position:relative;width:21px;height:21px;background-image:url("'+path+'img_selectedcolor.gif")\'></div></div>';
                        this.getElement().setHtml( imagemap );
                    },
                    setup : function( element ) { this.disable(); }
                },
                { type : 'hbox',
                    width : [ '25%', '25%', '25%', '25%' ],
                    children : [
                    { type : 'checkbox',
                        id : 'famille',
                        label : 'Serif',
                        onClick : function () {
                            var apercu = this.getDialog().getContentElement( 'stylphon', 'apercu' ).getElement();
                            if (this.getValue()) {
                                editor.config.lirecouleur['font-family'] = 'serif';
                                apercu.setStyle( 'font-family', 'serif' );
                            } else {
                                editor.config.lirecouleur['font-family'] = 'sans-serif';
                                apercu.setStyle( 'font-family', 'sans-serif' );
                            }
                            if (editor.config.lirecouleur['phonid'].length > 0) {
                                LireCouleurFormateur.couleurs[editor.config.lirecouleur['phonid']] = assembleStyle( editor.config.lirecouleur );
                            }
                        },
                        setup : function( element ) { this.disable(); }
                    },
                    { type : 'checkbox',
                        id : 'gras',
                        label : 'Gras',
                        onClick : function () {
                            var apercu = this.getDialog().getContentElement( 'stylphon', 'apercu' ).getElement();
                            if (this.getValue()) {
                                editor.config.lirecouleur['font-weight'] = 'bold';
                                apercu.setStyle( 'font-weight', 'bold' );
                            } else {
                                editor.config.lirecouleur['font-weight'] = '';
                                apercu.removeStyle( 'font-weight' );
                            }
                            if (editor.config.lirecouleur['phonid'].length > 0) {
                                LireCouleurFormateur.couleurs[editor.config.lirecouleur['phonid']] = assembleStyle( editor.config.lirecouleur );
                            }
                        },
                        setup : function( element ) { this.disable(); }
                    },
                    { type : 'checkbox',
                        id : 'italique',
                        label : 'Italique',
                        onClick : function () {
                            var apercu = this.getDialog().getContentElement( 'stylphon', 'apercu' ).getElement();
                            if (this.getValue()) {
                                editor.config.lirecouleur['font-style'] = 'italic';
                                apercu.setStyle( 'font-style', 'italic' );
                            } else {
                                editor.config.lirecouleur['font-style'] = '';
                                apercu.removeStyle( 'font-style' );
                            }
                            if (editor.config.lirecouleur['phonid'].length > 0) {
                                LireCouleurFormateur.couleurs[editor.config.lirecouleur['phonid']] = assembleStyle( editor.config.lirecouleur );
                            }
                        },
                        setup : function( element ) { this.disable(); }
                    },
                    { type : 'checkbox',
                        id : 'souligne',
                        label : 'Souligné',
                        onClick : function () {
                            var apercu = this.getDialog().getContentElement( 'stylphon', 'apercu' ).getElement();
                            if (this.getValue()) {
                                editor.config.lirecouleur['text-decoration'] += ' underline';
                                editor.config.lirecouleur['text-decoration'] = editor.config.lirecouleur['text-decoration'].trim();
                                apercu.setStyle( 'text-decoration', editor.config.lirecouleur['text-decoration'] );
                            } else {
                                editor.config.lirecouleur['text-decoration'] = editor.config.lirecouleur['text-decoration'].replace( 'underline', '').trim();
                                if (editor.config.lirecouleur['text-decoration'].length > 0) {
                                    apercu.setStyle( 'text-decoration', editor.config.lirecouleur['text-decoration'] );
                                }
                                else {
                                    apercu.removeStyle( 'text-decoration' );
                                }
                            }
                            if (editor.config.lirecouleur['phonid'].length > 0) {
                                LireCouleurFormateur.couleurs[editor.config.lirecouleur['phonid']] = assembleStyle( editor.config.lirecouleur );
                            }
                        },
                        setup : function( element ) { this.disable(); }
                    },
                    { type : 'checkbox',
                        id : 'surligne',
                        label : 'Surligné',
                        onClick : function () {
                            var apercu = this.getDialog().getContentElement( 'stylphon', 'apercu' ).getElement();
                            if (this.getValue()) {
                                editor.config.lirecouleur['text-decoration'] += ' overline';
                                editor.config.lirecouleur['text-decoration'] = editor.config.lirecouleur['text-decoration'].trim();
                                apercu.setStyle( 'text-decoration', editor.config.lirecouleur['text-decoration'] );
                            } else {
                                editor.config.lirecouleur['text-decoration'] = editor.config.lirecouleur['text-decoration'].replace( 'overline', '').trim();
                                if (editor.config.lirecouleur['text-decoration'].length > 0) {
                                    apercu.getElement().setStyle( 'text-decoration', editor.config.lirecouleur['text-decoration'] );
                                }
                                else {
                                    apercu.removeStyle( 'text-decoration' );
                                }
                            }
                            if (editor.config.lirecouleur['phonid'].length > 0) {
                                LireCouleurFormateur.couleurs[editor.config.lirecouleur['phonid']] = assembleStyle( editor.config.lirecouleur );
                            }
                        },
                        setup : function( element ) { this.disable(); }
                    }
                ] }
            ] }
        ],

        onShow : function() {
            var sel = editor.getSelection(),
                        element = sel.getStartElement();
            LireCouleurFormateur.getCookies();
            this.element = element;
            this.setupContent( this.element );
        },

        onOk : function() {
            var dialog = this;
            LireCouleurFormateur.phonemes['phon_a'] = dialog.getValueOf( 'general', 'checkA' );
            LireCouleurFormateur.phonemes['phon_e'] = dialog.getValueOf( 'general', 'checkQ' );
            LireCouleurFormateur.phonemes['phon_i'] = dialog.getValueOf( 'general', 'checkI' );
            LireCouleurFormateur.phonemes['phon_u'] = dialog.getValueOf( 'general', 'checkY' );
            LireCouleurFormateur.phonemes['phon_muet'] = dialog.getValueOf( 'general', 'checkH' );
            
            LireCouleurFormateur.phonemes['phon_ou'] = dialog.getValueOf( 'general', 'checkU' );
            LireCouleurFormateur.phonemes['phon_ez'] = dialog.getValueOf( 'general', 'checkE' );
            LireCouleurFormateur.phonemes['phon_o'] = dialog.getValueOf( 'general', 'checkO' );
            LireCouleurFormateur.phonemes['phon_et'] = dialog.getValueOf( 'general', 'checkEt' );
            LireCouleurFormateur.phonemes['phon_eu'] = dialog.getValueOf( 'general', 'checkEu' );
            
            LireCouleurFormateur.phonemes['phon_an'] = dialog.getValueOf( 'general', 'checkAn' );
            LireCouleurFormateur.phonemes['phon_on'] = dialog.getValueOf( 'general', 'checkOn' );
            LireCouleurFormateur.phonemes['phon_in'] = dialog.getValueOf( 'general', 'checkIn' );
            LireCouleurFormateur.phonemes['phon_w'] = dialog.getValueOf( 'general', 'checkW' );
            LireCouleurFormateur.phonemes['phon_y'] = dialog.getValueOf( 'general', 'checkJ' );
            
            LireCouleurFormateur.phonemes['phon_l'] = dialog.getValueOf( 'general', 'checkL' );
            LireCouleurFormateur.phonemes['phon_v'] = dialog.getValueOf( 'general', 'checkV' );
            LireCouleurFormateur.phonemes['phon_f'] = dialog.getValueOf( 'general', 'checkF' );
            LireCouleurFormateur.phonemes['phon_p'] = dialog.getValueOf( 'general', 'checkP' );
            LireCouleurFormateur.phonemes['phon_b'] = dialog.getValueOf( 'general', 'checkB' );
            
            LireCouleurFormateur.phonemes['phon_m'] = dialog.getValueOf( 'general', 'checkM' );
            LireCouleurFormateur.phonemes['phon_z'] = dialog.getValueOf( 'general', 'checkZ' );
            LireCouleurFormateur.phonemes['phon_s'] = dialog.getValueOf( 'general', 'checkS' );
            LireCouleurFormateur.phonemes['phon_t'] = dialog.getValueOf( 'general', 'checkT' );
            LireCouleurFormateur.phonemes['phon_d'] = dialog.getValueOf( 'general', 'checkD' );

            LireCouleurFormateur.phonemes['phon_n'] = dialog.getValueOf( 'general', 'checkN' );
            LireCouleurFormateur.phonemes['phon_ge'] = dialog.getValueOf( 'general', 'checkGe' );
            LireCouleurFormateur.phonemes['phon_ch'] = dialog.getValueOf( 'general', 'checkCh' );
            LireCouleurFormateur.phonemes['phon_k'] = dialog.getValueOf( 'general', 'checkK' );
            LireCouleurFormateur.phonemes['phon_g'] = dialog.getValueOf( 'general', 'checkG' );

            LireCouleurFormateur.phonemes['phon_r'] = dialog.getValueOf( 'general', 'checkR' );
            LireCouleurFormateur.phonemes['phon_ng'] = dialog.getValueOf( 'general', 'checkNg' );
            LireCouleurFormateur.phonemes['phon_gn'] = dialog.getValueOf( 'general', 'checkGn' );
            LireCouleurFormateur.phonemes['phon_ks'] = dialog.getValueOf( 'general', 'checkKs' );
            LireCouleurFormateur.phonemes['phon_gz'] = dialog.getValueOf( 'general', 'checkGz' );
            
            LireCouleurFormateur.setCookies();
        }
    
    };
});

/*

*/
CKEDITOR.dialog.add( 'pdfDialog', function( editor )
{
    return {
        title : 'Exporter en PDF',
        minWidth : 400,
        minHeight : 100,
        contents : [
            { id : 'general',
                label : 'Orientation',
                elements : [
                { type: 'html', html: '<div style="font-weight: bold;">Orientation des pages</div>' },
                { type : 'radio',
                    id : 'orientation',
                    items : [ [ 'Portrait', 'p' ], [ 'Paysage', 'l' ] ],
                    'default' : 'p'
                }
            ] }
        ],

        onOk : function() {
            var w = 522,
                orientation = 'p';
            
            if (this.getValueOf( 'general', 'orientation' ) == 'l' ) {
                w = 760;
                orientation = 'landscape';
            }
            
            var pdf = new jsPDF( orientation, 'pt', 'a4');

            // we support special element handlers. Register them with jQuery-style 
            // ID selector for either ID or node name. ("#iAmID", "div", "span" etc.)
            // There is no support for any other type of selectors 
            // (class, of compound) at this time.
            var specialElementHandlers = {
                // element with id of "bypass" - jQuery style selector
                '#bypassme': function (element, renderer) {
                    // true = "handled elsewhere, bypass text extraction"
                    return true
                }
            };
            var margins = {
                top: 40,
                bottom: 40,
                left: 40,
                width: w
            };
            // all coords and widths are in jsPDF instance's declared units
            // 'inches' in this case
            pdf.fromHTML(
                editor.getData(), // HTML string or DOM elem ref.
                margins.left, // x coord
                margins.top, { // y coord
                    'width': margins.width, // max width of content on PDF
                    'elementHandlers': specialElementHandlers
                },

                function (dispose) {
                    // dispose: object with X, Y of the last line add to the PDF 
                    //
                    pdf.save( 'lirecouleur.pdf' );
                }, margins);

        }
    };
});
