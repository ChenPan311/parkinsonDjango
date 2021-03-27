const MSG = " מטופל  לא נמצא"

$('#search_btn').click(function () {
    let patient_id =$('#patient_input')[0].value
    let form = $('#search_form')
    const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    $.post({
        url: "/patient_detail/check",
        data: {data:patient_id},
        headers: {
            "X-CSRFToken": token
        },
        success: function (result) {
            if (result === "False") {  //If medicine already exist
                $(".bootstrap-growl").remove();  //Nice looking alert
                $.bootstrapGrowl(MSG, {
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
