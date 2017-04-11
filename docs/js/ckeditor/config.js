/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function(config) {
	// Define changes to default configuration here. For example:
	 config.language = 'en';
	 //config.uiColor = '#fff';
	 config.skin = 'office2013';
	 config.height = '407';

// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbarGroups = [
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'simple-image-browser' },
		{ name: 'tools' },

		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'styles' },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },

		{ name: 'colors' },
		{ name: 'about' }
	];
	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;h4;h5';

	config.extraPlugins = 'image2,simple-image-browser,zoom,pastefromword';
	// config.pasteFromWordCleanupFile = true;
	// config.pasteFromWordPromptCleanup = true;
	// config.pasteFromWordRemoveFontStyles = true;
	config.forcePasteAsPlainText = false;
    config.pasteFromWordRemoveFontStyles = true;
    config.pasteFromWordRemoveStyles = false;
    config.allowedContent = true;
    config.extraAllowedContent = 'p(mso*,Normal)';
    //config.pasteFilter = null;
    config.pasteFilter = 'h1 h2 h3 h4 h5 h6 h7 p ul ol li; img[!src, alt]; a[!href]';
    config.removeButtons='Flash,Smiley';
// config.htmlEncodeOutput = false;
// config.entities = false;
// config.basicEntities = false;
};
