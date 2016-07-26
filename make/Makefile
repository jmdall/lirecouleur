all : LireCouleur.oxt LireCouleurAOO4.oxt tests web

clean :
	rm -r images locale pythonpath template lirecouleur.dic lirecouleurooo.py AddonUI.xcu description.xml LireCouleur.oxt LireCouleurAOO4.oxt ../tests/lirecouleur.* ../src/firefox-plugin/data/lirecouleur.js

core : Descriptions/descr-fr.txt Legal/license-fr.txt META-INF/manifest.xml WindowState/tbWriter.xcu ../src/opendocument-plugin/lirecouleurooo.py ../src/opendocument-plugin/pythonpath/lirecouleur.py
	cp -r ../src/opendocument-plugin/* .

LireCouleur.oxt : core standard_oxt/AddonUI.xcu standard_oxt/description.xml
	cp standard_oxt/* .
	zip -r $@ WindowState locale template pythonpath Legal META-INF Descriptions images
	zip $@ lirecouleurooo.py
	zip $@ description.xml
	zip $@ lirecouleur.dic
	zip $@ AddonUI.xcu

LireCouleurAOO4.oxt : core aoo4_oxt/AddonUI.xcu aoo4_oxt/description.xml
	cp aoo4_oxt/* .
	zip -r $@ WindowState locale template pythonpath Legal META-INF Descriptions images
	zip $@ lirecouleurooo.py
	zip $@ description.xml
	zip $@ lirecouleur.dic
	zip $@ AddonUI.xcu

tests : ../src/opendocument-plugin/pythonpath/lirecouleur.py ../src/opendocument-plugin/lirecouleur.dic ../tests/tests_lirecouleur.py
	cp ../src/opendocument-plugin/pythonpath/lirecouleur.py ../tests/
	cp ../src/opendocument-plugin/lirecouleur.dic ../tests/
	python ../tests/tests_lirecouleur.py

web :
	cp ../src/ckeditor-plugin/lirecouleur.js ../src/firefox-plugin/data/
