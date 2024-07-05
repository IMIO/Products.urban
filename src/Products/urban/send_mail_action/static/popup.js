/* The jQuery here above will load a jQuery popup */

// overlays for the action present in the object_actions dropdown list box 'Actions'
initializeActionsOverlays = function () {

  jQuery('a.apButtonAction_form_send_mail_action').prepOverlay({
    subtype: 'ajax',
    formselector: '#form',
    noform: 'redirect',
    redirect: $.plonepopups.redirectbasehref,
    closeselector: '[name="form.buttons.cancel"]'
  });

  var url = null;
  var has_onclick = false;
  var input = jQuery('input.apButtonAction_send_mail_action')
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
