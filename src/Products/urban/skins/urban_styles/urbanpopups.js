/* The jQuery here above will load a jQuery popup */

jQuery(function($){

    // Long text popup
    $('#urban-claims-text a').prepOverlay({
       subtype: 'ajax',
       urlmatch: '@@claimstextview',
   });

    // Long text popup
    $('#urban-additional-conditions a').prepOverlay({
       subtype: 'ajax',
   });

    // parcel history popup
    $('#urban-parcel-related-licences a').prepOverlay({
       subtype: 'ajax',
   });
});
