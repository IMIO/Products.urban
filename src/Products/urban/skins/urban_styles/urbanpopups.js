/* The jQuery here above will load a jQuery popup */

jQuery(function($){

    // Long text popup
    $('#urban-claims-text a').prepOverlay({
       subtype: 'ajax',
       urlmatch: '@@claimstextview',
   });

    // parcel history popup
    $('#urban-parcel-related-licences a').prepOverlay({
       subtype: 'ajax',
       urlmatch: '@@genericlicenceview',
   });
});
