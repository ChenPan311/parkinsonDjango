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

$('#submit_btn').click(function (){
    let med_name = $('#id_medication_name') // Populate the form with med name
    let category = $('#id_category')
    let form = $('#answer_form')
    const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    console.log(token)
    let data = {'med_name': med_name, 'category': category}
    const dataString = JSON.stringify(data);
    $.post({
        url: "check/",
        data: dataString ,
        headers: {
                    "X-CSRFToken": token
               },
        success: function (result){
            if(result === "True" ){
                alert("תרופה כבר קיימת")
            } else {
                form.submit()
            }
        }
    })
})
