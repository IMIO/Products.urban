(function($) {
function parseTab(tab, lid, legend){
    /* XXX change by urban
     *  keep the last selected tab after edition */
    if ((window.location.href.search("/edit") != -1) &&
       (lid != 'fieldsetlegend-urban_events') &&
       (lid != 'fieldsetlegend-attachments')){
        tab += ' onClick = "'+
               'var search_form = document.getElementsByTagName(\'form\')[1];'+
               'var action_url = search_form.getAttribute(\'action\');'+
               'action_url = action_url.substr(0, action_url.lastIndexOf(\'/base_edit\'));'+
               'search_form.setAttribute(\'action\', action_url+\'/base_edit/#'+lid+'\')"';
    }
    tab += '><a id="'+lid+'" href="#'+lid+'"><span>';
    /* XXX change by urban */
    /* display the edit icon only if we are not already editing the element... */
    tab += $(legend).text()+'</span>';
    if ((window.location.href.search("/edit") == -1) &&
       (lid != 'fieldsetlegend-urban_events') &&
       (lid.startsWith('fieldsetlegend-urban_')) &&
       (lid != 'fieldsetlegend-attachments')){
        gni = window.location.pathname;
        gni = gni.replace('/view', '');
        tab += '&nbsp;&nbsp;<img class="urban-edit-tabbing"'+
               'onclick="javascript:window.location=gni+&quot;/edit#'+
               lid+
               '&quot;" src="edit.png"></a></li>';
    } else if ((window.location.href.search("/edit") == -1) &&
       (lid == 'fieldsetlegend-attachments')){
        tab += '&nbsp;&nbsp;<img class="urban-edit-tabbing"'+
               ' src="attachment.png"></a></li>';
    } else {
        tab += '</a></li>';
    }
    return tab;
}
if(ploneFormTabbing){
    ploneFormTabbing._buildTabs = function(container, legends) {
        var threshold = legends.length > ploneFormTabbing.max_tabs;
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
                tab = '<li '+className;
                tab = parseTab(tab, lid, legend);
            }

            tabs += tab;
            // don't use .hide() for ie6/7/8 support
            $(legend).css({'visibility': 'hidden', 'font-size': '0',
                           'padding': '0', 'height': '0',
                           'width': '0', 'line-height': '0'});
        }

        tab_ids = tab_ids.join(',');
        panel_ids = tab_ids.replace(/#fieldsetlegend-/g, "#fieldset-");

        if (threshold) {
            tabs = $('<select class="formTabs">'+tabs+'</select>');
            tabs.change(function(){
                var selected = $(this).attr('value');
                $(this).parent().find('option#'+selected).click();
            });
        } else {
            tabs = $('<ul class="formTabs">'+tabs+'</ul>');
        }
        return tabs;
    };
}
})(jQuery);
