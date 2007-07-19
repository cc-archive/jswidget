<?php
/**
 * NOTE: Don't be fooled by the extension.  This gets intepreted by the PHP
 * interpreter.  That way I can dispatch based on the query string.
 *
 * See .htaccess for how to configure it for php5.
 */
header("content-type: application/x-javascript");
?>

<?php
/* Figure out our base path. */
$me = $_SERVER['REQUEST_URI'];
$parsed = parse_url($me);
$dirname = dirname($parsed['path']);
$base = http_build_url($me, array('path' => $dirname));

echo "lol, base is " . $base ." <p>";

/* Load the prerequisite JS files */
document.write('<script src="http://labs.creativecommons.org/jswidget/trunk/js/prototype.js" />\n');
document.write('<script src="http://labs.creativecommons.org/jswidget/trunk/js/cc-tooltip.js" />\n');
document.write('<script src="http://labs.creativecommons.org/jswidget/trunk/js/cc-jurisdictions.js" />\n');
document.write('<script src="http://labs.creativecommons.org/jswidget/trunk/js/cc-license.js" />\n');
document.write('<script src="http://labs.creativecommons.org/jswidget/trunk/js/cc-lib-freedoms.js" />\n');
document.write('<script src="http://labs.creativecommons.org/jswidget/trunk/js/init.js" />\n');

/* NOTE: I do not include the CSS stylesheet
   and instead I let others style our boxes the way they want. */

/* Insert the template */

<?php
/* First check if we were called with ?locale=XX and dispatch accordingly */
    if (array_key_exists('locale', $_GET)) {
	$template_url = 'http://labs.creativecommons.org/jswidget/trunk/template.' . $_GET['locale'] . '.js';
    }

/* Else, do the generic one and hope they either like English or will
 * do their own language negotiation */
    else {
	$template_url = 'http://labs.creativecommons.org/jswidget/trunk/template.js';
    }
?>

document.write('<script src="<?php echo $template_url ?>" />\n');
