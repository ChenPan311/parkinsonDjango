const MSG = " מטופל לא נמצא"

$('#search_btn').click(function () {
    let patient_id = $('#patient_input')[0].value
    let form = $('#search_form')
    const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    $.post({
        url: "/patient_detail/check",
        data: {data: patient_id},
        headers: {
            "X-CSRFToken": token
        },
        success: function (result) {
            if (result === "False") {  //If medicine already exist
                $(".bootstrap-growl").remove();  //Nice looking alert
                $.bootstrapGrowl(MSG, {
                    ele: 'body',
                    type: 'danger',
                    offset: {from: 'top', amount: 10},
                    align: 'center',
                    width: 'auto',
                    delay: 2000,
                    allow_dismiss: false,
                });
            } else {
                $('<input type="submit">').hide().appendTo(form).click().remove();
            }
        }
    })
})

function handleAttrs(e) {
    row = e.closest('tr') // finds closest <tr> element - row that contains the btn we clicked
    row.find('.row-data , .row-time-data, .add_time_btn').each(function () { // in this row find classes ... (inputs)
        $(this).attr('disabled') ? $(this).prop('disabled', false) : $(this).prop('disabled', true)
    })
    save_updates = row.find('.save_row_btn')
    delete_btn = row.find('.delete_row_btn')
    save_updates.attr('hidden') ? save_updates.prop('hidden', false) : save_updates.prop('hidden', true)
    delete_btn.attr('hidden') ? delete_btn.prop('hidden', false) : delete_btn.prop('hidden', true)

}

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
            dosage = $(this)[0].value
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
                $(".bootstrap-growl").remove();
                $.bootstrapGrowl("עדכון לא הצליח", {
                    ele: '.header-nb',
                    type: 'danger',
                    offset: {from: 'top', amount: 10},
                    align: 'center',
                    width: 'auto',
                    delay: 2000,
                    allow_dismiss: false,
                });
            } else {
                e.data("medicine-key", medicine_id) // updating the data-medicine-key to the new medcine key
                row.find('.edit_row_btn, .delete_row_btn, .submit_delete_row_btn').data("medicine-key", medicine_id)
                handleAttrs(e)
                $(".bootstrap-growl").remove();
                $.bootstrapGrowl("עודכן בהצלחה!", {
                    ele: '.header-nb',
                    type: 'success',
                    offset: {from: 'top', amount: 20},
                    align: 'center',
                    width: 'auto',
                    delay: 2000,
                    allow_dismiss: false,
                });
            }
        }
    })
}

$('table').on('click', '.edit_row_btn', function () {
    handleAttrs($(this))
})

$('table').on('click', '.save_row_btn', function () {
    handleSaveEdits($(this))
})

$('table').on('click', '.add_time_btn', function () {
    cell = $(this).closest('td')
    newInput = $('<input required class="row-time-data" type="time">')
    cell.append(newInput).append(" ")
})


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
                    $(".bootstrap-growl").remove();
                    $.bootstrapGrowl("עדכון לא הצליח", {
                        type: 'danger',
                        offset: {from: 'top', amount: 10},
                        align: 'center',
                        width: 'auto',
                        delay: 2000,
                        allow_dismiss: false,
                    });
                } else {
                    row.fadeOut(1000, function () {
                        row.remove();
                    });
                }
            }
        })
    }
    // $('table tbody tr').length === 1 ?
    // console.log($('table tbody tr').length)
    // $('#alert').attr('hidden') ? $('#trhead').prop('hidden', false) : null
}

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
        $(this).hasClass('name') ? $(this).prop('selectedIndex', 1) : $(this).val("").attr('value', '')
    })
    trNew.find('.edit_row_btn, .save_row_btn ,delete_row_btn, .submit_delete_row_btn').each(function () {
        $(this).data("medicine-key", '')
    })
    trLast.after(trNew);
    console.log($('table tbody tr').length)
})

$('#notify_patient_medications').click(function (){
    token = $(this).data("token")
    const csrf_tok = $('input[name="csrfmiddlewaretoken"]').attr('value');
        $.post({
        url: "/patient_detail/send_medication_notif",
        data: {data : token},
        headers: {
            "X-CSRFToken": csrf_tok
        },
        success: function (result) {
            if (result === "False") {  //If something went wrong
                $(".bootstrap-growl").remove();
                $.bootstrapGrowl("אירעה שגיאה", {
                    ele: '.header-nb',
                    type: 'danger',
                    offset: {from: 'top', amount: 10},
                    align: 'center',
                    width: 'auto',
                    delay: 2000,
                    allow_dismiss: false,
                });
            } else {
                $(".bootstrap-growl").remove();
                $.bootstrapGrowl("התראה נשלחה!", {
                    ele: '.header-nb',
                    type: 'success',
                    offset: {from: 'top', amount: 20},
                    align: 'center',
                    width: 'auto',
                    delay: 2000,
                    allow_dismiss: false,
                });
            }
        }
    })

})

