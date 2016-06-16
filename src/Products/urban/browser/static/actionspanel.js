var initialize_overlay = function() {

  jQuery(function($) {

    var handle_change_owner_overlay = function(evt) {
      var overlay = $(evt.target);
      var submit = overlay.find('form#form input[type="submit"]');
      submit.click(function() {
        var form = $(this).closest('form');
        var post_url = form.attr('action');
        data = {
          'form.buttons.confirm': 'Confirm',
          'form.widgets.new_owner:list': form.find('select[name="form.widgets.new_owner:list"]').val(),
        }
        $.ajax({
          type: 'POST',
          url: form.attr('action'),
          data: data,
          success: function(data) {
            Faceted.URLHandler.hash_changed();
            overlay.overlay().close();
          },
        });
        return false;
      });
    };

    // Change owner popup
    $('a.overlay-change-owner').prepOverlay({
      subtype: 'ajax',
      filter: '#change-owner',
      cssclass: 'overlay-change-owner',
      closeselector: '[name="form.buttons.cancel"]',
      config: {
        onLoad: handle_change_owner_overlay,
      },
    });

  });
};

jQuery(document).ready(initialize_overlay);
jQuery(document).ready(function($) {
  if(window.Faceted){
    $(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(){
      initialize_overlay();
    });
  }
});

