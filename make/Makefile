all : LireCouleur.oxt LireCouleurAOO4.oxt

clean :
	rm -r images locale pythonpath template lirecouleur.dic lirecouleurooo.py AddonUI.xcu LireCouleur.oxt LireCouleurAOO4.oxt

core : Descriptions/descr-fr.txt Legal/license-fr.txt META-INF/manifest.xml WindowState/tbWriter.xcu description.xml ../src/opendocument-plugin/lirecouleurooo.py ../src/opendocument-plugin/pythonpath/lirecouleur.py
	cp -r ../src/opendocument-plugin/* .

LireCouleur.oxt : core standard_oxt/AddonUI.xcu
	cp standard_oxt/AddonUI.xcu ./AddonUI.xcu
	zip -r $@ WindowState locale template pythonpath Legal META-INF Descriptions images
	zip $@ lirecouleurooo.py
	zip $@ description.xml
	zip $@ lirecouleur.dic
	zip $@ AddonUI.xcu

LireCouleurAOO4.oxt : core aoo4_oxt/AddonUI.xcu
	cp aoo4_oxt/AddonUI.xcu ./AddonUI.xcu
	zip -r $@ WindowState locale template pythonpath Legal META-INF Descriptions images
	zip $@ lirecouleurooo.py
	zip $@ description.xml
	zip $@ lirecouleur.dic
	zip $@ AddonUI.xcu
