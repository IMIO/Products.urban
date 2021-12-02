function getField() {
        $('[id^=pb_] [id^=fieldtoreplace_]').each(function(index) {
            here = $(this)
            field_id = here.attr('class');
            oldcontent = $('#archetypes-fieldname-' + field_id);

            // use this trick to get fields hidden by master select widget
            if (oldcontent.hasClass('refreshed')){
                newcontent = oldcontent.clone();
                // copy/paste the 'select' property manually since the clone method is bugged ..
                var selects = oldcontent.find("select");
                $(selects).each(function(i) {
                    var select = this;
                    $(newcontent).find("select").eq(i).val($(select).val());
                });
                //finally  do the replace
                here.replaceWith(newcontent);
            }
            else {
                loaded_field = $('#' + here.attr('id') + ' div:first');
                loaded_field.addClass('refreshed')
            }
        });
};

function updateField(field_ids) {
        field_ids = field_ids.split('|');
        for (var i=0; i < field_ids.length; i++)
        {
            field_id = field_ids[i];
            newcontent = $('[id^=pb_] #archetypes-fieldname-' + field_id);
            $('#archetypes-fieldname-' + field_id).replaceWith(newcontent);
        }
        closePopup();
};

function closePopup() {
        overlay = $('[id^=pb_]').data('overlay');
        overlay.close();
};
