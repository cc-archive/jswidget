#!/usr/bin/python
# This takes template.html and makes a document.write() for it.
# Later, it could take template.html and make DOM objects instead.

def escape_single_quote(s):
	return s.replace("'", "\\'")

inp = open('template.html')
out = open('template.js', 'w')
for line in inp:
	escaped_line = escape_single_quote(line.strip())
	print >> out, "document.write('%s');" % escaped_line

