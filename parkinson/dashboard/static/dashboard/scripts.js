// Init the timepicker for the medicine hours to be from 00:00 to 23:00 with jumps of 30 minutes
function setTimepickerOptions(e) {
    e.timepicker({
        'timeFormat': 'H:i',
        'minTime': '00:00am',
        'maxTime': '23:30am',
        'step': 30,
        'lang': {
            mins: 'min',
            hrs: 'hr'
        }
    })
}

// Checking if a patient exists
$('#search_btn').click(function () {
    let patient_id = $('#patient_input')[0].value
    let form = $('#search_form')
    $.get({
        url: "/patient_detail/check",
        data: {data: patient_id},
        success: function (result) {
            if (result === "False") {  //If patient already exist
                GrowlCall(" מטופל לא נמצא",'danger');
            } else {
                $('<input type="submit">').hide().appendTo(form).click().remove();
            }
        }
    })
})

// When click 'ערוך' in the medicine table, able/disable the edit functionallity
function handleAttrs(e) {
    row = e.closest('tr') // finds closest <tr> element - row that contains the btn we clicked
    row.find('.row-data , .row-time-data, .add_time_btn').each(function () { // in this row find classes ... (inputs)
        $(this).attr('disabled') ? $(this).prop('disabled', false) : $(this).prop('disabled', true)
        if ($(this).hasClass('row-time-data')){
            $(this)[0].value === "00:00" || $(this)[0].value === '' ? $(this).remove() : null; // removing uninitalize time input
        }
    })
    save_updates = row.find('.save_row_btn')
    delete_btn = row.find('.delete_row_btn')
    save_updates.attr('hidden') ? save_updates.prop('hidden', false) : save_updates.prop('hidden', true)
    delete_btn.attr('hidden') ? delete_btn.prop('hidden', false) : delete_btn.prop('hidden', true)

}

// When clicking 'שמור' gather all data enterd and send it to the view function that handle adding/editing medicine
function handleSaveEdits(e) {
    row = e.closest('tr')
    hours_arr = ""
    row.find('.row-time-data').each(function () {
        hours_arr += ($(this)[0].value) + ','
    })
    row.find('.row-data').each(function () {
        if ($(this).hasClass('name')) {
            medicine_id = $(this)[0].value
            category_id = $('#' + medicine_id).data('category')
            medicine_name = $(this).children("option").filter(":selected").text()
        } else {
            dosage = $(this).children("option").filter(":selected").text()
        }
    })

    med_key = e.data('medicine-key') // for checking if we changed the medicine name
    if (med_key == '') {
        med_key = medicine_id
    }
    data = {
        'categoryId': category_id,
        'dosage': dosage,
        'id': medicine_id,
        'name': medicine_name,
        'hoursArr': hours_arr,
        'keyToUpdate': med_key
    }

    const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    $.post({
        url: "/patient_detail/med_update",
        data: data,
        headers: {
            "X-CSRFToken": token
        },
        success: function (result) {
            if (result === "False") {  //If something went wrong
                GrowlCall("עדכון לא הצליח",'danger')
            } else {
                e.data("medicine-key", medicine_id) // updating the data-medicine-key to the new medcine key
                row.find('.edit_row_btn, .delete_row_btn, .submit_delete_row_btn').data("medicine-key", medicine_id)
                handleAttrs(e)
                GrowlCall("עודכן בהצלחה!",'success')
            }
        }
    })
}

// Handling edits of existing medicines of a patient
$('table').on('click', '.edit_row_btn', function () {
    handleAttrs($(this))
})

// Handling saving of new/exist medicine of a patient
$('table').on('click', '.save_row_btn', function () {
    handleSaveEdits($(this))
})

// Handling clicking on the add time button, adding new time input
$('table').on('click', '.add_time_btn', function () {
    cell = $(this).closest('td')
    newInput = $('<input required class="row-time-data" type="time" onkeydown="return false">')
    setTimepickerOptions(newInput)
    cell.append(newInput).append(" ")

})

// When clicking 'מחק', deleting the medicine from the patient
function delete_data(e) {
    med_key = e.data('medicine-key')
    if (med_key === '') {
        row.fadeOut(1000, function () {
            row.remove();
        });
    } else {
        row = e.closest('tr')
        const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
        $.post({
            url: "/patient_detail/med_delete",
            data: {data: med_key},
            headers: {
                "X-CSRFToken": token
            },
            success: function (result) {
                if (result === "False") {  //If something went wrong
                    GrowlCall("עדכון לא הצליח",'danger')
                } else {
                    row.fadeOut(1000, function () {
                        row.remove();
                    });
                }
            }
        })
    }
}

// Handling click on 'מחק' button
$('table').on('click', '.delete_row_btn', function () {
    row = $(this).closest('tr')
    edit_btn = row.find('.edit_row_btn')
    submit_deletion = row.find('.submit_delete_row_btn')

    $(this).toggleClass('delete')
    $(this).hasClass('delete') ? $(this).text('חזור') : $(this).text('מחק')
    submit_deletion.attr('hidden') ? submit_deletion.prop('hidden', false) : submit_deletion.prop('hidden', true)
    edit_btn.attr('hidden') ? edit_btn.prop('hidden', false) : edit_btn.prop('hidden', true)
    submit_deletion.click(function () {
        delete_data($(this))
    })
})

// When clicking on 'הוסף', adding new row to the medicine table
$('#add_medicine_btn').click(function () {
    $('#trhead').attr('hidden') ? $('#trhead').prop('hidden', false) : null
    $('#alert').prop('hidden', true)
    tableBody = $('table').find('tbody')
    trLast = tableBody.find("tr:last")
    trNew = trLast.clone(); // creating new row which is a duplicate of the last row
    trNew.attr('hidden') ? trNew.prop('hidden', false) : null
    trNew.find('.row-time-data').each(function () {
        $(this).remove()
    })
    trNew.find('.row-data').each(function () {
        $(this).hasClass('name') ? $(this).prop('selectedIndex', 1) : $(this).prop('selectedIndex', 0)
    })
    trNew.find('.edit_row_btn, .save_row_btn ,delete_row_btn, .submit_delete_row_btn').each(function () {
        $(this).data("medicine-key", '')
    })
    trLast.after(trNew);
})

// $('#notify_patient_medications').click(function (){
//     token = $(this).data("token")
//     const csrf_tok = $('input[name="csrfmiddlewaretoken"]').attr('value');
//         $.post({
//         url: "/patient_detail/send_medication_notif",
//         data: {data : token},
//         headers: {
//             "X-CSRFToken": csrf_tok
//         },
//         success: function (result) {
//             if (result === "False") {  //If something went wrong
//                 GrowlCall("אירעה שגיאה",'danger')
//             } else {
//                 GrowlCall("התראה נשלחה!",'success')
//             }
//         }
//     })
//
// })

// $('#notify_patient_questionnaire').click(function (){
//     token = $(this).data("token")
//     const csrf_tok = $('input[name="csrfmiddlewaretoken"]').attr('value');
//         $.post({
//         url: "/patient_detail/send_questionnaire_notif",
//         data: {data : token},
//         headers: {
//             "X-CSRFToken": csrf_tok
//         },
//         success: function (result) {
//             if (result === "False") {  //If something went wrong
//                 GrowlCall("אירעה שגיאה",'danger')
//             } else {
//                 GrowlCall("התראה נשלחה!",'success')
//             }
//         }
//     })
// })

// Showing nice alert of given message and type
function GrowlCall(msg,type){
    $(".bootstrap-growl").remove();
    $.bootstrapGrowl(msg, {
        ele: 'nav',
        type: type,
        offset: {from: 'top', amount: 20},
        align: 'center',
        width: 'auto',
        delay: 2000,
        allow_dismiss: false,
    });
}

// returning formatted date
function formatDate(formated, date = null) {
    var dtToday;
    if (!date)
        dtToday = new Date()
    else
        dtToday = new Date(date)

    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();
    if (month < 10)
        month = '0' + month.toString();
    if (day < 10)
        day = '0' + day.toString();

    if (formated)
        return [year, month, day].join('-'); // for init the date picker
    else
        return [day, month, year].join('-'); // for filter dates
}

// Taking the relvant reports
function updateMedReports(isDefault,medication_reports,mychart) {
    if (isDefault)
        formated_today = formatDate(false)
    else
        formated_today = formatDate(false, date_picker.value)

    med_reports = []
    for (const reportee of medication_reports) {
        new_label = reportee.label;
        new_label = new_label.split(' ')
        if (new_label[0] === formated_today) {
            report = {
                x: new_label[1],
                y: 8,
                id: reportee.name
            }
            med_reports.push(report)
        }
    }
    mychart.data.datasets[1].data = med_reports;
    mychart.update();
}

// Making the data for the chart
function filterDatesAndLabels(isDefault, reports) {
    let status_reports = []
    let pointsStyles = []
    let pointsColors = []
    if (isDefault)
        formated_today = formatDate(false)
    else
        formated_today = formatDate(false, date_picker.value)

    for (const reportee of reports) {
        new_label = reportee.label;
        new_value = reportee.value;
        new_label = new_label.split(' ')

        if (new_label[0] === formated_today) {
            if(reportee.hallucinations === 'True' && reportee.falls === 'True') {
                pointsStyles.push('cross')
                pointsColors.push('rgb(0,0,0)')
            }
            else if (reportee.hallucinations === 'True') {
                pointsStyles.push('triangle')
                pointsColors.push('rgb(255,82,82)')
            }
            else if(reportee.falls === 'True'){
                pointsStyles.push('rect')
                pointsColors.push('rgb(231, 161, 0)')
            }else {
                pointsStyles.push('circle')
                pointsColors.push('rgb(39,65,181)')
            }
            report = {
                x: new_label[1],
                y: parseInt(new_value),
            }
            status_reports.push(report)
        }
    }
    myChart.data.datasets[0].pointStyle = pointsStyles
    myChart.data.datasets[0].pointBorderColor = pointsColors
    myChart.data.datasets[0].data = status_reports;
    myChart.data.datasets[0].pointBackgroundColor = pointsColors;
    myChart.update();
}

// Makes the tooltips to be always shown
Chart.pluginService.register({
    beforeRender: function (chart) {
        if (chart.config.options.showAllTooltips) {
            chart.pluginTooltips = [];
            chart.config.data.datasets.forEach(function (dataset, i) {
                if (i == 1) { // only Medications tooltips
                    chart.getDatasetMeta(i).data.forEach(function (sector, j) {
                        chart.pluginTooltips.push(new Chart.Tooltip({
                            _chart: chart.chart,
                            _chartInstance: chart,
                            _data: chart.data,
                            _options: chart.options.tooltips,
                            _active: [sector]
                        }, chart));
                    });
                }
            });
            chart.options.tooltips.enabled = false;
            chart.options.tooltips.displayColors = false;
        }
    },
    afterDraw: function (chart, easing) {
        if (chart.config.options.showAllTooltips) {
            chart.options.tooltips.enabled = true;
            Chart.helpers.each(chart.pluginTooltips, function (tooltip) {
                tooltip.initialize();
                tooltip.update();
                tooltip.pivot();
                tooltip.transition(easing).draw();
            });
            chart.options.tooltips.enabled = false;
        }
    }
});