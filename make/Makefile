all : LireCouleur.oxt LireCouleurAOO4.oxt tests web

clean :
	rm -r images locale pythonpath template lirecouleur.dic lirecouleurooo.py AddonUI.xcu description.xml LireCouleur.oxt LireCouleurAOO4.oxt ../tests/lirecouleur.*

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

cleanweb:
	rm ../src/firefox-plugin/data/jquery.min.js
	rm ../src/firefox-plugin/data/jqColorPicker.min.js
	rm ../src/web/js/jquery.min.js
	rm ../src/web/js/jquery-ui.min.js
	rm ../src/web/js/js.cookie.js
	rm ../src/web/js/jquery.ui.touch-punch.min.js
	rm ../src/web/js/evol.colorpicker.min.js
	rm ../src/web/js/iosCheckbox.min.js
	rm ../src/web/css/evol.colorpicker.min.css
	rm ../src/web/css/iosCheckbox.css
	rm ../src/web/css/jquery-ui.min.css
	rm ../src/firefox-plugin/data/lirecouleur.js

web :
	cp ../src/vendors/js/jquery.min.js ../src/firefox-plugin/data/
	cp ../src/vendors/js/jqColorPicker.min.js ../src/firefox-plugin/data/
	cp ../src/vendors/js/jquery.min.js ../src/web/js/
	cp ../src/vendors/js/jquery-ui.min.js ../src/web/js/
	cp ../src/vendors/js/js.cookie.js ../src/web/js/
	cp ../src/vendors/js/jquery.ui.touch-punch.min.js ../src/web/js/
	cp ../src/vendors/js/evol.colorpicker.min.js ../src/web/js/
	cp ../src/vendors/js/iosCheckbox.min.js ../src/web/js/
	cp ../src/vendors/css/evol.colorpicker.min.css ../src/web/css/
	cp ../src/vendors/css/iosCheckbox.css ../src/web/css/
	cp ../src/vendors/css/jquery-ui.min.css ../src/web/css/
	cp ../src/web/js/lirecouleur.js ../src/firefox-plugin/data/
