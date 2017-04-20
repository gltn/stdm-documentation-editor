
    function insert_js_docs() {
        for (var j = 0; j < js_doc_files.length; j++) {
            var doc_script = document.createElement('script');
            doc_script.setAttribute('src', js_doc_files[j]);
            document.head.appendChild(doc_script);
        }

    }
    insert_js_docs();

    function prepare_content() {

        if (window.location.search !== '' && window.location.hash == '') {
            $('#tipue_search_content').show('slow')
        }
        else if (window.location.hash !== '') {
//            $('#doc_container').html(window[current_name][0]);
            var doc_name = window.location.hash.replace('#', '');
            $('#tipue_search_content').hide('slow');
            $('#doc_container').html(window[doc_name][0]);
        }
        else {
            $('#doc_container').html(window[current_name][0]);
            $('#tipue_search_content').hide('slow')
        }
        document.title = title;

    }
    $(window).load(function () {
        prepare_content()
    });
    function setup_side_menu() {
        $('#st_side_menu').html(window['toc_' + language][0]);

        $('#st_side_menu').on('loaded.jstree', treeLoaded).jstree({

            "plugins": [
                "contextmenu",
                "massload",
                "search",
                "types",
                "changed"
            ],
            "search": {

                "case_insensitive": false,
                "show_only_matches": true
            },
            "types": {
                "default": {
                    "icon": "glyphicon glyphicon-folder-open"
                }
            }

        }).on('changed.jstree', function (NODE, REF_NODE) {
            document.title = title;
            $("html, body").animate({scrollTop: 0});
            var clicked_file = REF_NODE.node.a_attr.href;
            if (clicked_file.length < 5) {
                return
            }
            var doc_name = clicked_file.split('.')[0].replace(/-/g, '_');
            $('#doc_container').html(window[doc_name]);
            title = REF_NODE.node.text + ' | STDM';
            document.title = title

        });

        function treeLoaded(event, data) {
            var prev_node = $('#st_side_menu').find(current_name);
            var prev_parent = $('#st_side_menu').jstree("get_parent", prev_node);

            $("#st_side_menu").jstree("select_node", prev_node);
            $("#st_side_menu").jstree("select_node", prev_parent);
            $("#st_side_menu").jstree("open_node", prev_parent);
        }

        // bind customize icon change function in jsTree open_node event.
        $('#st_side_menu').on('open_node.jstree', function (e, data) {
            var icon = $('#' + data.node.id).find(
                'i.jstree-icon.jstree-themeicon').first();
            icon.removeClass('glyphicon glyphicon-folder-close').addClass(
                'glyphicon glyphicon-folder-open');
        });
        // bind customize icon change function in jsTree open_node event.
        $('#st_side_menu').on('select_node.jstree', function (e, data) {
            if (data.node.a_attr.href != '') {
                window.location.hash = data.node.a_attr.href.split('.')[0]
            }
            else {
                window.location.hash = 'no_page';
            }

        });
        // bind customize icon change function in jsTree close_node event.
        $('#st_side_menu').on('close_node.jstree', function (e, data) {
            var icon = $(
                '#' + data.node.id).find(
                'i.jstree-icon.jstree-themeicon').first();
            icon.removeClass(
                'glyphicon glyphicon-folder-open').addClass(
                'glyphicon glyphicon-folder-close');
        });
    }

    $(document).ready(function () {
        setup_side_menu();

    });

    // load languages list
    var option;
    for (var key in added_languages) {
        if (added_languages.hasOwnProperty(key)) {
            option += '<option value="' + key + '">' +
                added_languages[key] + '</option>';
        }
    }
    $('#added_languages').append(option);
    $("#added_languages option[value='" + language + "']").prop(
        'selected', true
    );

    // handle language changes
    $('#added_languages').on('change', function () {
        // Set local storage before close.
        var sel_node = $("#st_side_menu").jstree("get_selected");
        if (sel_node.length < 1) {
            sel_html = current_js_path;
        }
        else {
            var sel_html = $('#' + sel_node).find('a').first()[0].href;
        }
        var curr_name = sel_html.split('/').reverse()[0].split('.')[0];
        var version = doc_path.split('/')[0];
        var curr_doc_path = version + '/' + this.value;
        var curr_js_path = curr_doc_path + '/' + curr_name + '.js';

        curr_data = {
            'current_js_path': curr_js_path,
            'current_name': curr_name,
            'doc_path': curr_doc_path,
            'language': this.value,
            'title': title
        };
        // Put the object into storage
        localStorage.setItem(
            'curr_data', JSON.stringify(curr_data)
        );
        // reload the page to load with the new language content
        location.reload();
    });

    $(document).ready(function () {
        $('#tipue_search_input').tipuesearch();
        $(window).on('hashchange', function (event, data) {

            $('#tipue_search_content').hide('slow');
            var doc_name = window.location.hash.replace('#', '');
            $('#doc_container').html(window[doc_name]);

        });

       $('#refresh2').on("click", function () {
           localStorage.clear();
           location.reload();
       });
        $("#left").css({'height': (window.innerHeight - 90) + "px"});

    });

