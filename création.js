// Sélection des éléments avec typage strict
var addBtn = document.getElementById('addQuestion');
var deleteBtn = document.getElementById('deleteQuestion');
var createBtn = document.getElementById('createQuiz');
var questionInput = document.getElementById('questionInput');
var questionList = document.getElementById('questionList');
function downloadQuestionsAsHTML(questions) {
    var htmlContent = "\n<!DOCTYPE html>\n<html lang=\"fr\">\n<head><meta charset=\"UTF-8\"><title>Questions g\u00E9n\u00E9r\u00E9es</title></head>\n<body><h1>Liste des questions :</h1><ul>".concat(questions.map(function (q) { return "<li>".concat(q, "</li>"); }).join(''), "</ul></body>\n</html>");
    var blob = new Blob([htmlContent], { type: 'text/html' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'questions.html';
    a.click();
    URL.revokeObjectURL(url);
}
if (addBtn && deleteBtn && createBtn && questionInput && questionList) {
    addBtn.addEventListener('click', function () {
        var questionText = questionInput.value.trim();
        if (questionText !== "") {
            var li_1 = document.createElement('li');
            li_1.textContent = questionText;
            li_1.addEventListener('click', function () {
                document.querySelectorAll('#questionList li')
                    .forEach(function (item) { return item.classList.remove('selected'); });
                li_1.classList.add('selected');
            });
            questionList.appendChild(li_1);
            questionInput.value = "";
        }
    });
    deleteBtn.addEventListener('click', function () {
        var selected = questionList.querySelector('.selected');
        if (selected) {
            questionList.removeChild(selected);
        }
        else {
            alert('Veuillez sélectionner une question à supprimer.');
        }
    });
    createBtn.addEventListener('click', function () {
        var questions = Array.from(questionList.querySelectorAll('li')).map(function (li) { var _a; return (_a = li.textContent) !== null && _a !== void 0 ? _a : ""; });
        if (questions.length > 0) {
            downloadQuestionsAsHTML(questions);
            alert("Questionnaire cr\u00E9\u00E9 avec ".concat(questions.length, " questions."));
            console.log(questions);
        }
        else {
            alert("Aucune question à enregistrer.");
        }
    });
}
else {
    console.error('Un ou plusieurs éléments manquent dans le DOM.');
}
