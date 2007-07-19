#!/usr/bin/python
# This takes template.html and makes a document.write() for it.
# Later, it could take template.html and make DOM objects instead.

from simpletal import simpleTAL, simpleTALES
import cStringIO as StringIO
import os
import BeautifulSoup

LANGUAGE="en_US"

import sys
sys.path.insert(0, './license_xsl/licensexsl_tools')
import translate

def grab_license_ids():
	licenses_xml = BeautifulSoup.BeautifulSoup(open('license_xsl/licenses.xml'))
	juris = []
	for juri in licenses_xml('jurisdiction-info'):
		juris.append(juri['id'])
	juris = [juri for juri in juris if juri != '-']
	return juris

def get_PoFile():
	return translate.PoFile("license_xsl/i18n/i18n_po/icommons-%s.po" % LANGUAGE)

def country_id2name(country_id):
	# Now gotta look it up with gettext...
	po = get_PoFile()
	try:
		return po['country.%s' % country_id]
	except KeyError:
		return country_id

def escape_single_quote(s):
	return s.replace("'", "\\'")

def expand_template_with_jurisdictions(templatefilename, juridict):
	# Create the context that is used by the template
	context = simpleTALES.Context()
	context.addGlobal("jurisdictions", juridict)

	templateFile = open('template.html')
	template = simpleTAL.compileHTMLTemplate(templateFile)
	templateFile.close()
	
	output_buffer = StringIO.StringIO()
	template.expand(context, output_buffer)
	return output_buffer.getvalue()

def main():
	jurisdiction_names = grab_license_ids()
	jurisdictions = [ dict(id=juri, name=country_id2name(juri)) for juri in jurisdiction_names]
	expanded = expand_template_with_jurisdictions('template.html', jurisdictions)
	
	# go parse the template, and try to translate the contents of each span
	# Like, WRITEME!

	out = open('template.js.tmp', 'w')

	for line in expanded.split('\n'):
		escaped_line = escape_single_quote(line.strip())
		print >> out, "document.write('%s');" % escaped_line
	out.close()
	os.rename('template.js.tmp', 'template.js')


if __name__ == '__main__':
	main()
