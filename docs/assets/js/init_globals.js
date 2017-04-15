var toc_src, doc_list_src, language, current_name, doc_src,
    current_js_path, local_store, doc_path, curr_data, title;
//        localStorage.clear();
if (localStorage["curr_data"] === undefined) {
    curr_data = {
        'current_js_path': html_file.current_js_path,
        'current_name': html_file.current_name,
        'doc_path': html_file.doc_path,
        'language': html_file.language,
        'search_data': html_file.search_data,
        'title': html_file.title
    };
    // Put the object into storage
    retrieved_object = localStorage.getItem(
        'curr_data', JSON.stringify(curr_data)
    );
    // Retrieve the object from storage
    local_store = JSON.parse(retrieved_object);
    toc_src = html_file.doc_path + '/table_of_contents.js';
    doc_list_src = html_file.doc_path + '/docs_js_list.js';
    language = html_file.language;
    current_name = html_file.current_name;
    doc_src = html_file.current_js_path;
    current_js_path = html_file.current_js_path;
    doc_path = html_file.doc_path;
    search_data = html_file.search_data;
    title = html_file.title + ' | STDM';
}
else {
    local_store = JSON.parse(localStorage["curr_data"]);
    toc_src = local_store.doc_path + '/table_of_contents.js';
    doc_list_src = local_store.doc_path + '/docs_js_list.js';
    language = local_store.language;
    current_name = local_store.current_name;
    current_js_path = local_store.current_js_path;
    doc_path = local_store.doc_path;
    search_data = local_store.search_data;
    title = local_store.title + ' | STDM';

}

document.write('<' + 'script src="' +
    doc_list_src + '" type="text/javascript"><' + '/script' + '>');
document.write('<' + 'script src="' + toc_src +
    '" type="text/javascript"><' + '/script' + '>');

document.write('<' + 'script src="' + current_js_path +
    '" type="text/javascript"><' + '/script' + '>');
document.write('<' + 'script src="' + doc_path + '/' + 'search_data.js' +
    '" type="text/javascript"><' + '/script' + '>');
