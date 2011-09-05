jQuery(function($){

    // Long text popup
    $('#urban-claims-text a').prepOverlay({
       subtype: 'ajax',
       urlmatch: '@@claimstextview',
    });
});
