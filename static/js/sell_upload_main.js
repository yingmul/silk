/*
 * jQuery File Upload Plugin JS Example 8.8.2
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, regexp: true */
/*global $, window, blueimp */

// this file is used in sell_outfit.html since it needs to call different url in ajax call
$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        //url: 'server/php/'
    });

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    $('#fileupload').fileupload('option', {
        // Enable image resizing, except for Android and Opera,
        // which actually support image resizing, but fail to
        // send Blob objects via XHR requests:
        disableImageResize: /Android(?!.*Chrome)|Opera/
            .test(window.navigator.userAgent),
        imageMaxWidth: 500,
        imageMaxHeight: 600,
        imageCrop: false,

        maxFileSize: 1572864, // 1.5 MB
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxNumberOfFiles: 6,
        autoUpload: true,

        // The maximum width of the preview images:
        previewMaxWidth: 150,
        // The maximum height of the preview images:
        previewMaxHeight: 180,

        messages: {
            maxNumberOfFiles: 'Maximum number of files exceeded (up to 6 is allowed)',
            acceptFileTypes: 'File type not allowed',
            maxFileSize: 'File is too large (max size is 10MB)',
            minFileSize: 'File is too small'
        }
    });

    // Load existing files:
    $('#fileupload').addClass('fileupload-processing');
});
