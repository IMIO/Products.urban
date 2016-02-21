// ajax call managing a call to a given p_view_name and reload taking faceted into account
function generate_document(generation_url) {
  $.ajax({
    url: generation_url,
    cache: false,
    async: false,
    success: function(data) {
        // open the document in external edition in a new tab
        url = data + '/external_edit';
        window.open(url,'_blank');
    },
    complete: function(jqXHR, textStatus) {
      // reload the page
      window.location.href = window.location.href;
    }
  });
}
