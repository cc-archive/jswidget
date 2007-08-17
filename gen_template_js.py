#!/usr/bin/python
# This takes template.html and makes a document.write() for it.
# Later, it could take template.html and make DOM objects instead.

import re
from simpletal import simpleTAL, simpleTALES
import cStringIO as StringIO
import os
import BeautifulSoup
from xml.dom.minidom import parseString

LANGUAGE="en_US"

DEBUG=True

import sys
sys.path.insert(0, './license_xsl/licensexsl_tools')
import convert
import translate

if not DEBUG:
	sys.stdout = open('/dev/null', 'w')

def grab_license_ids():
	licenses_xml = BeautifulSoup.BeautifulSoup(open('license_xsl/licenses.xml'))
	juris = []
	for juri in licenses_xml('jurisdiction-info'):
		juris.append(juri['id'])
	juris = [juri for juri in juris if juri != '-']
	return juris

def escape_single_quote(s):
	return s.replace("'", "\\'")

def xml_asciify(u):
	out = ''
	for char in u:
		if ord(char) < 128:
			out += char
		else:
			out += '&#%d;' % ord(char)
	return out
	

def expand_template_with_jurisdictions(templatefilename, juridict):
	# Create the context that is used by the template
	context = simpleTALES.Context()
	context.addGlobal("jurisdictions", juridict)

	templateFile = open('template.html')
	template = simpleTAL.compileXMLTemplate(templateFile)
	templateFile.close()
	
	output_buffer = StringIO.StringIO()
	template.expand(context, output_buffer, 'utf-8')
	return output_buffer.getvalue()

def un_entities(s):
	even_odd_mixup = re.split(r"&#([0-9]*);", s)
	for k in range(len(even_odd_mixup)):
		if k % 2: # if it is odd
			even_odd_mixup[k] = unichr(even_odd_mixup[k])
	return u''.join(even_odd_mixup)

def translate_spans_with_only_text_children(spans, lang):
	for span in spans:
		if len(span.childNodes) == 1:
			child = span.childNodes[0]
			if child.nodeType == 3: # FIXME: Magic number
						# maybe means Text
						# node?
				# First, decode any &#; thing
				xml_data = child.data
				unicode_data = un_entities(xml_data)
				utf8_data = unicode_data.encode('utf-8')
				child.data = convert.extremely_slow_translation_function(utf8_data, lang)


def gen_templated_js(language):
	jurisdiction_names = grab_license_ids()
	jurisdictions = []
	# First, handle generic
	generic_value = 'generic'
	generic_element_id = 'cc_js_jurisdiction_choice_' + generic_value
	generic_name = convert.extremely_slow_translation_function('Unported', language)
	jurisdictions.append(dict(id=generic_element_id, value=generic_value, name=generic_name))
	# Now jam everyone else in, too.
	for juri in jurisdiction_names:
		value = juri
		element_id = 'cc_js_jurisdiction_choice_' + value
		english_name = convert.country_id2name(value, 'en')
		cc_js_text = 'cc_js_text_' + english_name
		name = convert.country_id2name(value, language)
		jurisdictions.append(dict(cc_js_text=cc_js_text, id=element_id, value=value, name=name))
	expanded = expand_template_with_jurisdictions('template.html', jurisdictions)
	expanded_dom = parseString(expanded)

	# translate the spans, then pull out the changed text
	translate_spans_with_only_text_children(expanded_dom.getElementsByTagName('span'), language)
	translated_expanded = expanded_dom.toxml(encoding='utf-8')

	# now provide a jurisdiction-less alternative
	jurisdiction_div = None
	for div in expanded_dom.getElementsByTagName('div'):
		if div.getAttribute('id') == 'cc_js_jurisdiction_box':
			jurisdiction_div = div
	# now, eat yourself
	jurisdiction_div.parentNode.removeChild(jurisdiction_div)
	translated_expanded_without_jurisdiction = expanded_dom.toxml(encoding='utf-8')

	# Whew, we have everything ready.  Time to save.

	for (filename_base, string) in ( ('template.js.%s', translated_expanded),
					 ('template.nojuri.js.%s', translated_expanded_without_jurisdiction) ):
		out = open((filename_base + '.tmp') % language, 'w')

		for line in string.split('\n'):
			escaped_line = escape_single_quote(line.strip())
			print >> out, "document.write('%s');" % escaped_line
		out.close()
		os.rename( (filename_base + '.tmp') % language, filename_base % language)

def main():
	# For each language, generate templated JS for it
	languages = [k for k in os.listdir('license_xsl/i18n/i18n_po/') if '.po' in k]
	
	languages = [re.split(r'[-.]', k)[1] for k in languages]
	languages = ['en_US', 'fr']
	for lang in languages:
		gen_templated_js(lang)

	for template in ('template.js', 'template.nojuri.js'):
		# And for our final trick, we will generate the .var file with
		# languages that controls dispatch of requests to the untranslated
		# JavaScript file.
		default_lang = 'en_US'
		var_lines = ['URI: ' + template]
		for lang in languages:
			var_lines.append(gen_var_lang_line(uri_base=template, lang=lang, default_lang = default_lang))
		htaccess_fd = open(template + '.var.tmp', 'w')
		htaccess_fd.write('\n\n'.join(var_lines) + '\n')
		htaccess_fd.close()
		os.rename(template + '.var.tmp', template + '.var')

def gen_var_lang_line(uri_base, lang, default_lang, content_type='text/javascript'):
	if lang == default_lang:
		quality = '1.0'
	else:
		quality = '0.8'
		
	out = '''URI: %s.%s
Content-Language: %s
Content-Type: %s; qs = %s''' % (uri_base, lang, lang, content_type, quality)
	return out

if __name__ == '__main__':
	main()
