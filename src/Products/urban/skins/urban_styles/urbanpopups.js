/* The jQuery here above will load a jQuery popup */

jQuery(function($){

    // Long text popup
    $('#urban-claims-text a').prepOverlay({
       subtype: 'ajax',
       urlmatch: '@@claimstextview',
   });

    // parcel historic popup
    $('#urban-parcel-historic a').prepOverlay({
       subtype: 'ajax',
       urlmatch: '@@genericlicenceview',
   });
});
