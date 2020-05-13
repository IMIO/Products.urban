var initialize_overlay = function() {

  jQuery(function($) {

    var handle_task_action_overlay = function(evt) {
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
    $('input.overlay-task-action').prepOverlay({
      subtype: 'ajax',
      filter: '#task-action',
      cssclass: 'overlay-task-action',
      closeselector: '[name="form.buttons.cancel"]',
      config: {
        onLoad: handle_task_action_overlay,
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

