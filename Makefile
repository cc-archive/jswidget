all: up_to_date check_depends template.en_US.js cc-translations.js.en_US

check_depends:
	python2.5 depends.py

up_to_date:
	svn up > /dev/null

template.en_US.js: template.html gen_template_js.py license_xsl/licenses.xml
	python2.5 gen_template_js.py template.html
	python2.5 update_jurisdictions.py

cc-translations.js.en_US: template.html license_xsl/licenses.xml
	python2.5 gen_translations.py

clean:
	rm -f $(shell ls -1 template.*js*)
	rm -f $(shell ls -1 cc-transla*js*)
	rm -rf $(shell ls -1 js/cc-jurisdictions.js)
	rm -f $(shell ls -1 *.pyc)
