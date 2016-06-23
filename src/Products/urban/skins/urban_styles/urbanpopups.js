/* The jQuery here above will load a jQuery popup */

jQuery(function($){

    // Long text popup
    $('#urban-claims-text a').prepOverlay({
       subtype: 'ajax',
       urlmatch: '@@claimstextview',
   });

    // Long text popup
    $('#urban-coring a').prepOverlay({
       subtype: 'ajax',
   });

    // Long text popup
    $('#urban-minimum-conditions a').prepOverlay({
       subtype: 'ajax',
   });
    // parcel history popup
    $('#urban-parcel-related-licences a').prepOverlay({
       subtype: 'ajax',
   });
    // parcel history on old parcels popup
    $('#urban-parcel-historic-related-licences a').prepOverlay({
       subtype: 'ajax',
   });
    // CU1/CU2/NotaryLetter specific features popup
    $('#urban-specificfeatures-field a').prepOverlay({
       subtype: 'ajax',
    });
});
