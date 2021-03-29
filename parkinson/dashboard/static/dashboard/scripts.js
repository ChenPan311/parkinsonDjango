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
    med_key = e.data('medicine-key')
    $('.time_input' + med_key).each(function () {
        $(this).attr('disabled') ? $(this).prop('disabled', false) : $(this).prop('disabled', true)
    })
    $('.name_input' + med_key).each(function () {
        $(this).attr('disabled') ? $(this).prop('disabled', false) : $(this).prop('disabled', true)
    })
    $('.dosage_input' + med_key).each(function () {
        $(this).attr('disabled') ? $(this).prop('disabled', false) : $(this).prop('disabled', true)
    })
    save_updates = $('.save_row_btn' + med_key)
    delete_btn = $('.delete_row_btn' + med_key)
    save_updates.attr('hidden') ? save_updates.prop('hidden', false) : save_updates.prop('hidden', true)
    delete_btn.attr('hidden') ? delete_btn.prop('hidden', false) : delete_btn.prop('hidden', true)
}

function handleSaveEdits(e) {
    med_key = e.data('medicine-key')
    $('.save_row_btn' + med_key).click(function () {
        hours_arr = ""
        $('.time_input' + med_key).each(function () {
            hours_arr += ($(this)[0].value) + ','
        })
        $('.name_input' + med_key).each(function () {
            text_op = '.name_input' + med_key
            category_id = $('#' + med_key).data('category')
            medicine_id = $(this)[0].value
            medicine_name = $(text_op).children("option").filter(":selected").text()
        })
        $('.dosage_input' + med_key).each(function () {
            dosage = $(this)[0].value
        })
        hours_final = []
        for (i = 0; i < hours_arr.length; i++) {
            hours = hours_arr[i].split(':')[0]
            minutes = hours_arr[i].split(':')[1]
            hours_final[i] = {
                'hours': hours,
                'minutes': minutes
            }
        }
        data = {
            'categoryId': category_id,
            'dosage': dosage,
            'id': medicine_id,
            'name': medicine_name,
            'hoursArr': hours_arr
        }

        const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
        $.post({
            url: "/patient_detail/med_update",
            data: data,
            headers: {
                "X-CSRFToken": token
            },
            success: function (result) {
                if (result === "False") {  //If medicine already exist
                    $(".bootstrap-growl").remove();  //Nice looking alert
                    $.bootstrapGrowl("עדכון לא הצליח", {
                        ele: 'body',
                        type: 'danger',
                        offset: {from: 'top', amount: 10},
                        align: 'center',
                        width: 'auto',
                        delay: 2000,
                        allow_dismiss: false,
                    });
                } else {
                    handleAttrs($(this))
                    $(".bootstrap-growl").remove();  //Nice looking alert
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

