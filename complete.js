<?php
ob_start("ob_gzhandler");
/**
 * NOTE: Don't be fooled by the extension.  This gets intepreted by the PHP
 * interpreter.  That way I can dispatch based on the query string.
 *
 * See .htaccess for how to configure it for php5.
 */
require_once('accept-to-gettext.inc.php');
require_once("phphelpers.php");

$supported_gettext_languages = list_languages();

/* Prepare for internationalization. */
$mime = 'text/javascript'; // real MIME type of this document
$lang = 'en-US'; // default language
$gettextlang = 'en_US'; // default language, gettext style
$charset = 'UTF-8'; // default charset for this document

/* Did the user request a language? */
/* First check if we were called with ?locale=XX and dispatch accordingly */
if (array_key_exists('locale', $_GET) &&
    // valid locales are lower or upper case alphas plus _ or -
    preg_match('/^([a-zA-Z-_]+)$/', $_GET['locale']) &&
    in_array($_GET['locale'], $supported_gettext_languages))
  {
    $gettextlang = $_GET['locale'];
    $lang = str_replace('-', '_', $gettextlang);
  }
 else {
   $values = al2gt($supported_gettext_languages);
   if ($values['gettextlang'] != '') {
     $gettextlang = $values['gettextlang'];
     $lang = $values['lang'];
     $charset = $values['charset'];
   }
 }

/*  No matter what, emit headers to the browser indicating what we will be sending. */
emit_language_and_type_header($lang, $charset, $mime);

/******** i18n preparation done. ************
 * time to send out the actual JS. */

/* Load the prerequisite JS files */
$pre_reqs = array('js/cc-prereq.js', 'js/safari-label-fix.js', 'js/cc-tooltip.js', 'js/cc-jurisdictions.js', 'js/cc-license.js');
foreach ($pre_reqs as $pre_req) {
    echo file_get_contents($pre_req);
}

/* Send out the translations, too. */
echo file_get_contents('cc-translations.js.' . $gettextlang);

/* NOTE: I shove a stylesheet into the header in init.js.
   I put it before all the others, so they can still override our stuff. */

/* Apply extras */

/*
options:

show_jurisdiction_chooser = (y/n);
   default = y;
show_cc0_option = (y/n);
   default = y;
show_cc-license_option = (y/n);
   default = y;
show_no-license_option = (y/n);
   default = y;
default_option = (cc0/cc-license/no-license);
   default = cc-license

(locale is handled differently, see above)

*/
/*this is about to get messy: php echoing javascript.  brace yourself.*/

function extra_chosen($key, $value){
   return (array_key_exists($key, $_GET) && $_GET[$key] == $value);
}

//we'll use the following javascript function to pluck stuff from the document tree
//(for example, we use it to hide the No License option when the url includes ?show_no-license_option=n)
?>
function cc_js_remove_item(item){
   item.style.display = 'none';
   //or we could have done this:
   //item.parentNode.removeChild(item);
}
<?php

//we'll use the following javascript function to do act on all of the "extras"
//we only do this once, on document.onload
echo "function cc_js_apply_extras(){\n";

//hide the jurisdiction chooser, if they want
if (extra_chosen('show_jurisdiction_chooser', 'n')){
   echo "cc_js_remove_item(cc_js_$('jurisdiction_box'));\n";
}

//hide the various licensing options, if they want
//we remove the parent node of the radio button, because each radio is inside of a span which also conains a label.

$radios_removed = 0;
if (extra_chosen('show_cc0_option', 'n')){
   echo "cc_js_remove_item(cc_js_$('want_cc_license_zero').parentNode);\n";
   $radios_removed++;
}
if (extra_chosen('show_cc-license_option', 'n')){
   echo "cc_js_remove_item(cc_js_$('want_cc_license_sure').parentNode);\n";
   $radios_removed++;
}
if (extra_chosen('show_no-license_option', 'n')){
   echo "cc_js_remove_item(cc_js_$('want_cc_license_nah').parentNode);\n";
   $radios_removed++;
}
//if they disabled all of the options except one, then no point displaying the radio button bar at all...
if($radios_removed >= 2){
   echo "cc_js_remove_item(cc_js_$('want_cc_license_at_all'));\n";
}

//set the default licensing option
if (extra_chosen('default_option', 'cc0')){
   echo "cc_js_$('want_cc_license_zero').checked = 'checked';\n";
   echo "cc_js_$('want_cc_license_sure').checked = '';\n";
   echo "cc_js_$('want_cc_license_nah').checked = '';\n";
   echo "cc_js_set_cc0();\n";
}
else if (extra_chosen('default_option', 'cc-license')){
   echo "cc_js_$('want_cc_license_zero').checked = '';\n";
   echo "cc_js_$('want_cc_license_sure').checked = 'checked';\n";
   echo "cc_js_$('want_cc_license_nah').checked = '';\n";
   echo "cc_js_enable_widget();\n";
}
else if (extra_chosen('default_option', 'no-license')){
   echo "cc_js_$('want_cc_license_zero').checked = '';\n";
   echo "cc_js_$('want_cc_license_sure').checked = '';\n";
   echo "cc_js_$('want_cc_license_nah').checked = 'checked';\n";
   echo "cc_js_set_noLicense();\n";
}
//if they didn't specify, use this:
//choose cc-license by default
else{
   echo "cc_js_$('want_cc_license_zero').checked = '';\n";
   echo "cc_js_$('want_cc_license_sure').checked = 'checked';\n";
   echo "cc_js_$('want_cc_license_nah').checked = '';\n";
   echo "cc_js_enable_widget();\n";

}

echo '}'; //end of cc_js_apply_extras() definition

/* Now, send out the appropriate template. */
$template_dot_js = 'template.js';
/* Just tack on the gettext language. */
$template_filename = $template_dot_js . '.' . $gettextlang;

/* Slurp them in and send them. */
echo file_get_contents($template_filename);

/* Finally, initialize the JS. */
echo file_get_contents('js/init.js');
