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
    // Pm summary
    $('#pm-summary a').prepOverlay({
       subtype: 'ajax',
   });
    // parcel history popup
    $('#urban-parcel-related-licences a').prepOverlay({
       subtype: 'ajax',
   });
    // parcel history popup
    $('#urban-parcel-display a').prepOverlay({
       subtype: 'ajax',
   });
    // CU1/CU2/NotaryLetter specific features popup
    $('#urban-specificfeatures-field a').prepOverlay({
       subtype: 'ajax',
    });
    // Inspection report text
    $('#inspection_report_text a').prepOverlay({
       subtype: 'ajax',
    });
    // Inspection report other followup
    $('#inspection_other_followup a').prepOverlay({
       subtype: 'ajax',
    });
    // Inspection report other followup
    $('.link-overlay-urban-annex').prepOverlay({
       subtype: 'ajax',
    });
});
