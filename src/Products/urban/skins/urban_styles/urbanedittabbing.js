/* Override the default ploneFormTabbing _buildTabs method to add icon.gif when needed */

ploneFormTabbing._buildTabs = function(container, legends) {
    var threshold = legends.length > 6;
    var panel_ids, tab_ids = [], tabs = '';

    for (var i=0; i < legends.length; i++) {
        var className, tab, legend = legends[i], lid = legend.id;
        tab_ids[i] = '#' + lid;

        switch (i) {
            case (0):
                className = 'class="formTab firstFormTab"';
                break;
            case (legends.length-1):
                className = 'class="formTab lastFormTab"';
                break;
            default:
                className = 'class="formTab"';
                break;
        }

        if (threshold) {
            tab = '<option '+className+' id="'+lid+'" value="'+lid+'">';
            tab += $(legend).text()+'</option>';
        } else {
            tab = '<li '+className+'><a id="'+lid+'" href="#'+lid+'"><span>';
            /* XXX change by urban */
            /* display the edit icon only if we are not already editing the element... */
            tab += $(legend).text()+'</span>';
            if ((window.location.href.search("/edit") == -1) && (lid != 'fieldsetlegend-urban_events')) {
                tab += '&nbsp;&nbsp;<img class="urban-edit-tabbing" onclick="javascript:window.location=&quot;edit#'+lid+'&quot;" src="edit.gif"></a></li>'
            } else {
                tab += '</a></li>'
            }
        }

        tabs += tab;
        $(legend).hide();
    }

    tab_ids = tab_ids.join(',');
    panel_ids = tab_ids.replace(/#fieldsetlegend-/g, "#fieldset-");

    if (threshold) {
        tabs = $('<select class="formTabs">'+tabs+'</select>');
        tabs.change(function(){
            var selected = $(this).attr('value');
            jq('#'+selected).click();
        })
    } else {
        tabs = $('<ul class="formTabs">'+tabs+'</ul>');
    }

    return tabs;
};