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
    row.find('.row-data , .row-time-data').each(function () { // in this row find classes ... (inputs)
        $(this).attr('disabled') ? $(this).prop('disabled', false) : $(this).prop('disabled', true)
    })
    save_updates = row.find('.save_row_btn')
    delete_btn = row.find('.delete_row_btn')
    save_updates.attr('hidden') ? save_updates.prop('hidden', false) : save_updates.prop('hidden', true)
    delete_btn.attr('hidden') ? delete_btn.prop('hidden', false) : delete_btn.prop('hidden', true)
}

function handleSaveEdits(e) {
    row = e.closest('tr')
    med_key = e.data('medicine-key')
    row.find('.save_row_btn').click(function () {
        hours_arr = ""
        row.find('.row-time-data').each(function () {
            hours_arr += ($(this)[0].value) + ','
        })
        row.find('.row-data').each(function () {
            if ($(this).hasClass('name')) {
                category_id = $('#' + med_key).data('category')
                medicine_id = $(this)[0].value
                medicine_name = $(this).children("option").filter(":selected").text()
            } else {
                dosage = $(this)[0].value
            }
        })

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
                    $(".bootstrap-growl").remove();  //Nice looking alert
                    $.bootstrapGrowl("עדכון לא הצליח", {
                        type: 'danger',
                        offset: {from: 'top', amount: 10},
                        align: 'center',
                        width: 'auto',
                        delay: 2000,
                        allow_dismiss: false,
                    });
                } else {
                    handleAttrs(e)
                    $(".bootstrap-growl").remove();
                    $.bootstrapGrowl("עודכן בהצלחה!", {
                        type: 'success',
                        offset: {from: 'top', amount: 10},
                        align: 'center',
                        width: 'auto',
                        delay: 2000,
                        allow_dismiss: false,
                    });
                }
            }
        })
    })
}

$('.edit_row_btn').click(function () {
    handleAttrs($(this))
    handleSaveEdits($(this))
})

