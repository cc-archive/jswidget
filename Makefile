all: template.en_US.js

template.en_US.js: template.html gen_template_js.py
	python gen_template_js.py template.html

clean:
	rm -f template.js template.*.js template.js.*
