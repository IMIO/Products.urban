/* The jQuery here above will load a jQuery popup */

// overlays for the action present in the object_actions dropdown list box 'Actions'
initializeActionsOverlays = function () {

  jQuery('a.apButtonAction_edit_fields').prepOverlay({
    subtype: 'ajax',
    formselector: '#form',
    noform: 'redirect',
    redirect: $.plonepopups.redirectbasehref,
    closeselector: '[name="form.buttons.cancel"]',
    config: {
      onLoad: function(trigger) {
        jQuery.getScript('/++resource++ckeditor/ckeditor.js', function () {
          jQuery('textarea.ckeditor_plone').each(function () {
            var $textarea = jQuery(this);
            var id = $textarea.attr('id');
    
            // Destroy if already initialized (important when reusing overlays)
            if (CKEDITOR.instances["form.widgets.description"]) {
              CKEDITOR.instances["form.widgets.description"].destroy(true);
            }
    
            // Get custom config file if defined
            var configUrl = $textarea
              .closest('div')
              .find('input.cke_config_url')
              .val();
    
            // CKEditor replace with custom config
            CKEDITOR.replace("form.widgets.description", {
              customConfig: configUrl || ''
            });
          });
          jQuery('#form input[name="form.buttons.edit_fields"]').on('click', function () {
            CKEDITOR.instances["form.widgets.description"].updateElement();
          });
        });
      }
    }
  });

  var url = null;
  var has_onclick = false;
  var input = jQuery('input.apButtonAction_edit_fields')
  if ($(input).attr('onclick')) {
    url = $(input).attr('onclick');
    has_onclick = true;
  } else {
    url = $(input).parent().attr('action');
  }
  if (typeof url !== 'undefined' && url !== null) {
    cleanUrl = url.replace("javascript:", '').replace("window.location='", '').replace("window.open('", '').replace(", '_parent')", '').replace("'", "");
    jQuery(input).wrap("<a href='"+ cleanUrl +"'></a>");
    if (has_onclick == true) {
      $(this)[0].attributes['onclick'].value = '';
    }
    parent = jQuery(input).parent();
    parent.prepOverlay({
      subtype: 'ajax',
      formselector: '#form',
      noform: 'redirect',
      redirect: $.plonepopups.redirectbasehref,
      closeselector: '[name="form.buttons.cancel"]'
    });
  }
};

jQuery(document).ready(initializeActionsOverlays);
