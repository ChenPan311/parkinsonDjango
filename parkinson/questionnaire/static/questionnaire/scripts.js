let i = 0;
const addBtn = document.querySelectorAll("#add_answer_btn");
const removeBtn = document.querySelectorAll("#remove_answer_btn");
const option = document.querySelectorAll("#id_choice_type")
const answers_p = document.querySelectorAll("#answers_p")
const numberOfAnswers = document.getElementById("number_of_answers")
const editNumberOfAnswers = document.getElementById("edit_number_of_answers")
const answersContainer = document.getElementById("answers_container")
const editAnswersContainer = document.getElementById("edit_answers_container")

function handleOptions(toAdd) { // Handling changes in options select, toAdd(boolean) - Add modal/Edit modal
    if (toAdd) {
        if (option[0].value === 'OpenQuestion') {
            addBtn[0].style.display = 'none'
            removeBtn[0].style.display = 'none'
            answers_p[0].style.display = 'none'
            while (answersContainer.hasChildNodes()) {
                answersContainer.removeChild(answersContainer.lastChild);
            }
            i = 0
        } else {
            addBtn[0].style.display = 'initial'
            removeBtn[0].style.display = 'initial'
            answers_p[0].style.display = 'block'
        }
    } else {
        if (option[1].value === 'OpenQuestion') {
            addBtn[1].style.display = 'none'
            removeBtn[1].style.display = 'none'
            answers_p[1].style.display = 'none'
            while (editAnswersContainer.hasChildNodes()) {
                editAnswersContainer.removeChild(editAnswersContainer.lastChild);
            }
            editNumberOfAnswers.value = -1;
        } else {
            addBtn[1].style.display = 'initial'
            removeBtn[1].style.display = 'initial'
            answers_p[1].style.display = 'block'
        }
    }
}

function removeAnswers(toAdd) { // Handling removing answers' input to both modals, toAdd(boolean) - Add modal/Edit modal
    if (toAdd) {
        if (answersContainer.hasChildNodes()) {
            answersContainer.removeChild(answersContainer.lastChild);
            i -= 1
        }
    } else {
        if (editAnswersContainer.hasChildNodes()) {
            editAnswersContainer.removeChild(editAnswersContainer.lastChild);
            editNumberOfAnswers.value = parseInt(editNumberOfAnswers.value) - 1;
        }
    }
}

function addAnswers(toAdd) { // Handling adding answers' input to both modals, toAdd(boolean) - Add modal/Edit modal
    const answer = document.createElement("input");
    answer.type = "text";
    answer.name = i;
    answer.placeholder = "רשום תשובה";
    answer.id = i;
    answer.required = true
    answer.classList.add("form-control")
    answer.classList.add("mb-2")
    if (toAdd) {
        numberOfAnswers.value = i;
        answersContainer.appendChild(answer);
        i += 1
    } else {
        editNumberOfAnswers.value = parseInt(editNumberOfAnswers.value) + 1;
        answer.name = editNumberOfAnswers.value;
        answer.id = editNumberOfAnswers.value;
        editAnswersContainer.appendChild(answer);
    }

}

addBtn[0].addEventListener('click', addAnswers.bind(null, true)) // Bind for passing parameters to function
addBtn[1].addEventListener('click', addAnswers.bind(null, false))

removeBtn[0].addEventListener('click', removeAnswers.bind(null, true))
removeBtn[1].addEventListener('click', removeAnswers.bind(null, false))

option[0].addEventListener('change', handleOptions.bind(null, true))
option[1].addEventListener('change', handleOptions.bind(null, false))

$('#add-modal-bg').on('hidden.bs.modal', function () { // Handling closing the modal, remove all inputs
    while (answersContainer.hasChildNodes()) {
        answersContainer.removeChild(answersContainer.lastChild);
    }
})

//  Handling the edit functionality
$('#edit-modal-bg').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget); // Button that triggered the modal
    const key_to_edit = button.data('key-to-edit');
    const title = button.data('title'); // Extract info from data-* attributes
    const type = button.data('type'); // Extract info from data-* attributes
    let answers = button.data('answers'); // Extract info from data-* attributes
    const modal = $(this);
    if (type !== 'OpenQuestion') {
        addBtn[1].style.display = 'initial'
        removeBtn[1].style.display = 'initial'
        answers = answers.toString()
            .substring(1, answers.length - 1)
            .replaceAll('\'', '')
            .split(',') // Split the answers and make an array from it

        function addInput(item, index) { // Init the existing answers to the Edit modal
            const answer = document.createElement("input");
            answer.type = "text";
            answer.name = index;
            answer.value = item;
            answer.id = index;
            answer.required = true
            answer.classList.add("form-control")
            answer.classList.add("mb-2")
            editNumberOfAnswers.value = index;
            editAnswersContainer.appendChild(answer);
        }
        answers.forEach(addInput)
    } else {
        addBtn[1].style.display = 'none'
        removeBtn[1].style.display = 'none'
    }
    modal.find('#id_title').val(title) // Populate the form with data
    modal.find('#id_choice_type').val(type) // Populate the form with data
    modal.find('#update_btn').attr('value', key_to_edit)
    modal.find('#update_btn').attr('name', 'key_to_edit')

}).on('hidden.bs.modal', function () { // Handling closing the modal, remove all inputs
    while (editAnswersContainer.hasChildNodes()) {
        editAnswersContainer.removeChild(editAnswersContainer.lastChild);
    }
    i = 0;
})