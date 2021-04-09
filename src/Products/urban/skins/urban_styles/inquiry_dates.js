function get_end_date(inquiry_url) {
        start_date = $('#edit_form_investigationStart_0').attr('value');
        url = inquiry_url + '/@@inquiry_dates_delay?start=' + start_date;
        /* alert(start_date);*/
        const Http = new XMLHttpRequest(url,);
        Http.open("GET", url);
        Http.send();
        Http.onreadystatechange = (e) => {
            end_date = Http.responseText;
            splitted = end_date.split('-');
            year = splitted[0];
            month = splitted[1];
            day = splitted[2];
            $('#edit_form_investigationEnd_1').attr('value', end_date + ' 00:00');
            $('#edit_form_investigationEnd_1_year > [value=' + year + ']').attr('selected', 'selected');
            $('#edit_form_investigationEnd_1_year > [value!=' + year + ']').removeAttr('selected');
            $('#edit_form_investigationEnd_1_month > [value=' + month + ']').attr('selected', 'selected');
            $('#edit_form_investigationEnd_1_month > [value!=' + month + ']').removeAttr('selected');
            $('#edit_form_investigationEnd_1_day > [value=' + day + ']').attr('selected', 'selected');
            $('#edit_form_investigationEnd_1_day > [value!=' + day + ']').removeAttr('selected');
        }
};
