const MSG = "   התרופה כבר קיימת! בחר שם אחר"

// Handling edit existing medicine
$('#edit-modal-bg').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget); // Button that triggered the modal
    const key_to_edit = button.data('key-to-edit');
    const medicine_name = button.data('med-name'); // Extract info from data-* attributes
    const category = button.data('category'); // Extract info from data-* attribute
    const modal = $(this);
    modal.find('#id_medication_name').val(medicine_name) // Populate the form with med name
    modal.find('#id_category').val(category) // Populate the form with med category
    modal.find('#update_btn').attr('value', key_to_edit)
    modal.find('#update_btn').attr('name', 'key_to_edit')
})

// Handling adding new medicine
$('#submit_btn').click(function () {
    let med_name = $('#id_medication_name')[0].value
    let category = $('#id_category')[0].value
    let form = $('#answer_form')
    const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    let data = category + ',' + med_name
    $.post({
        url: "check/",
        data: {data: data},
        headers: {
            "X-CSRFToken": token
        },
        success: function (result) {
            if (result === "True") {  //If medicine already exist
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
