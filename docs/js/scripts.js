/**
 * Created by GLTN on 4/10/2017.
 */

function replace_all(str, find, replace) {
    return str.replace(new RegExp(find, 'g'), replace);
}

function get_url_param_value(name) {
    var url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
function find_next_file(image_path) {
    var image_name = image_path.split('/').reverse()[0];
    var ext = image_name.substr(image_name.lastIndexOf('.') + 1);
    var _img = image_name.substr(0, image_name.lastIndexOf('.'));

    $.getJSON('gallery_list.js', function (data) {
        var matched = [];
        $.each(data, function (url, img) {
            var name = img.name;
            if (name.indexOf(_img) >= 0 && name.indexOf(ext) >= 0) {

                matched.push(name);
            }

        });

        var next_number = matched[0].split(_img)[1];
        next_number = next_number.split(ext)[0];
        next_number = next_number.split('_')[1];
        next_number = next_number.split('.')[0];
        next_number = parseInt(next_number) + 1;
        console.log(next_number);
        console.log(_img + '_' + next_number + '.' + ext);
        return _img + '_' + next_number + '.' + ext;

    });
}
function img_absolute_to_relative(evt) {
    var elem = document.createElement("div");
    elem.innerHTML = evt.data.dataValue;
    var images = elem.getElementsByTagName("img");
    console.log(evt.data.dataValue);
    for (var i = 0; i < images.length; i++) {
        var old_src = images[i].src;
        var img_path = html_file.full_img_path.replace(/\\/g, '\/');
        // handle drag and drop
        if (old_src.search(img_path) > -1) {
            var img_folder = html_file.doc_path;
            var relative_url = images[i].src.toString().split(img_folder);
            var new_src = img_folder + relative_url[1];

            evt.data.dataValue = replace_all(
                evt.data.dataValue, old_src, new_src
            );
        }
        // handle paste from word
        else {
            console.log(old_src);
            var next_file = find_next_file(old_src);
            var src_urls = old_src.split('file:///');
            if (src_urls.length > 1) {
                var src_url = src_urls[1];
                console.log(src_urls);
                // send the url to python
                window.location.hash =
                    html_file.img_param + '=' + src_url;
                var new_upload_src =
                    html_file.relative_img_path + '/' + next_file;

                evt.data.dataValue = replace_all(
                    (evt.data.dataValue).toString(), old_src, new_upload_src
                );
            }

        }
    }
    //Disallow anchors for table of content and empty links
    var links = elem.getElementsByTagName('a');
    for (var j = 0; j < links.length; j++) {
        var old_a = links[j].outerHTML;
        var new_a = links[j].innerHTML;
        var href = links[j].getAttribute('href');

        if (href === null) {
            evt.data.dataValue = replace_all(
                evt.data.dataValue, old_a, new_a
            );
        }
    }

}

var editor = CKEDITOR.replace('editor1', {
        on: {
            'instanceReady': function (evt) {
                evt.editor.execCommand('maximize');


            }
        }

    }
);

CKEDITOR.config.simpleImageBrowserURL = 'images.js';

function prod_to_dev_image_url(html_data, body) {
    var elem = document.createElement("div");

    elem.innerHTML = body;

    var images = elem.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        var img_name = images[i].src.toString().split('/').reverse()[0];

        img_name = img_name.replace('%22', '').replace('%22', '');
        images[i].src = html_data.relative_img_path + '/' + img_name;

    }
    return elem.innerHTML

}
function load_content(html_data) {

    $.get(html_data.current, function (content) {
        var body = content.replace(/^[\S\s]*<body[^>]*?>/i, "")
            .replace(/<\/body[\S\s]*$/i, "");
        body = prod_to_dev_image_url(html_data, body);
        editor.setData(body);

    });
}

$(document).ready(function () {
    // Replace source
    load_content(html_file);
});
$('#editor1').on('paste', '[contenteditable]', function (e) {
    e.preventDefault();
    var text = (e.originalEvent || e).clipboardData.getData('text/plain');
    alert(text);
});
CKEDITOR.on("instanceReady", function (ev) {
    var editor = ev.editor;
    editor.on('paste', function (evt) {
        console.log('pasted');
        img_absolute_to_relative(evt);

    });
    editor.document.on('dragenter', function (ev) {
        ev.data.preventDefault(true);
    });

    editor.document.on('dragover', function (ev) {
        ev.data.preventDefault(true);
    })
});
// Add an event listener.
$(document).on('customChangeEvent', function (e, data) {
    load_content(data);
//  editor.on( 'paste', function( evt ) {
//    img_absolute_to_relative(evt);
//
//});
});


// Disable backspace key except in fields.
$(document).on("keydown", function (e) {
    if (e.which === 8 && !$(e.target).is("input, textarea")) {
        e.preventDefault();
    }
});
// The "change" event is fired whenever a change is made in the editor.
editor.on('change', function (evt) {
    window.location.hash = evt.editor.getData();
    return false; //Prevents Page Refresh
});
CKEDITOR.instances.editor1.on('save', function (evt) {
    window.location.hash = evt.editor.getData();
    return false; //Prevents Page Refresh
});
