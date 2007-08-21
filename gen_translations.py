#!/usr/bin/python
import re
import os
import sys
import json
sys.path.insert(0, './license_xsl/licensexsl_tools')
import convert
import gen_template_js

# Look with a cheesy regex for cc_js_t('something') calls
def findall(s):
	utf8 = re.findall(r'''cc_js_t[(]['"](.*?)['"'[)]''', s)
	return utf8

def translation_table_to_js_function_body(table):
	## NOTE WEIRD CHARSET ASSUMPTIONS
	## This does input and output in pure Unicode strings, even though
	## there's no such thing in JavaScript.  Just encode() the output of
	## me to utf-8.

	ret = u''
	template = u' if (s == %s) { return %s; } \n'
	for key in table:
		try:
			key = unicode(key)
		except:
			key = unicode(key, 'utf-8')
		ret += template % (json.write(key), json.write(table[key]))
	ret += 'return null;'
	return ret

def main():
	languages = [k for k in os.listdir('license_xsl/i18n/i18n_po/') if '.po' in k]
	languages = [re.split(r'[-.]', k)[1] for k in languages]
	translate_all_of_me = findall(open('template.html').read())
	for lang in languages:
		translation_table = {}
		for english in translate_all_of_me:
			translation_table[english] = convert.extremely_slow_translation_function(english, lang)
		fn_body = translation_table_to_js_function_body(translation_table)
		fn = '''function cc_js_t(s) {
		%s
		}''' % fn_body
		fd = open('cc-translate.js.%s' % lang, 'w')
		fd.write(fn.encode('utf-8'))
		fd.close()
	# Whew.  Generated some JS files.  Now should also make some .var
	# file for those who can't use these.
	default_lang = 'en'
	gen_template_js.create_var_file(my_variants = None, languages=languages, base_filename='cc-translate.js')
	

if __name__ == '__main__':
	main()
