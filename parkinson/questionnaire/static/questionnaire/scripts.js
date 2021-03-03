let i = 0;
const addBtn = document.getElementById("add_answer_btn");
const removeBtn = document.getElementById("remove_answer_btn");
const numberOfAnswers = document.getElementById("number_of_answers")
const option = document.getElementById("id_choice_type")
const answersContainer = document.getElementById("answers_container")
const closeModalBtn = document.getElementById("close_btn")

closeModalBtn.onclick = function () {
    while (answersContainer.hasChildNodes()) {
        answersContainer.removeChild(answersContainer.lastChild);
    }
}

option.onchange = function () {
    if (option.value === 'OpenQuestion') {
        addBtn.style.display = 'none'
        removeBtn.style.display = 'none'
        while (answersContainer.hasChildNodes()) {
            answersContainer.removeChild(answersContainer.lastChild);
        }
        i = 0
    } else {
        addBtn.style.display = 'initial'
        removeBtn.style.display = 'initial'
    }
}

removeBtn.onclick = function () {
    if (answersContainer.hasChildNodes()) {
        answersContainer.removeChild(answersContainer.lastChild);
        i -= 1
    }
}

addBtn.onclick = function () {
    const answer = document.createElement("input");
    answer.type = "text";
    answer.name = i;
    answer.placeholder = "רשום תשובה";
    answer.id = i;
    answer.required = true
    answer.classList.add("form-control")
    answer.classList.add("mb-2")
    numberOfAnswers.value = i;
    answersContainer.appendChild(answer);
    i += 1
}
