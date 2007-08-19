// <![CDATA[
/**
 * Creative Commons has made the contents of this file
 * available under a CC-GNU-GPL license:
 *
 * http://creativecommons.org/licenses/GPL/2.0/
 *
 * A copy of the full license can be found as part of this
 * distribution in the file COPYING.
 *
 * You may use this software in accordance with the
 * terms of that license. You agree that you are solely 
 * responsible for your use of this software and you
 * represent and warrant to Creative Commons that your use
 * of this software will comply with the CC-GNU-GPL.
 *
 * $Id: $
 *
 * Copyright 2006, Creative Commons, www.creativecommons.org.
 *
 * This is code that is used to generate licenses.
 *
 */

function cc_js_$F(id) {
	if (cc_js_$(id)) {
		return cc_js_$(id).value;
	}
	return null; // if we can't find the form element, pretend it has no contents
}

function cc_js_$(id) {
    return document.getElementById("cc_js_" + id);
}

/* A wrapper to get Elements By ID
 * Really used for grabbing translations.
 * Unfortunately, having spaces is not valid in IDs, so
 * in the future this should base64 encode the IDs.
 *
 * Also, I should really join all the text children rather than just getting
 * the first.
 */
function cc_js_t(s) {
    return cc_js_$('text_' + s).firstChild.data;
}


