// Sélection des éléments avec typage strict
var addBtn = document.getElementById('addQuestion');
var deleteBtn = document.getElementById('deleteQuestion');
var createBtn = document.getElementById('createQuiz');
var questionInput = document.getElementById('questionInput');
var questionList = document.getElementById('questionList');
var quizTitle = document.getElementById('quizTitle');
function downloadQuestionsAsHTML(title, questions) {
    var htmlContent = "\n<!DOCTYPE html>\n<html lang=\"fr\">\n<head><meta charset=\"UTF-8\"><title>".concat(title, "</title></head>\n<body>\n  <h1>").concat(title, "</h1>\n  <ul>").concat(questions.map(function (q) { return "<li>".concat(q, "</li>"); }).join(''), "</ul>\n</body>\n</html>");
    var blob = new Blob([htmlContent], { type: 'text/html' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'questions.html';
    a.click();
    URL.revokeObjectURL(url);
}
if (addBtn && deleteBtn && createBtn && questionInput && questionList && quizTitle) {
    addBtn.addEventListener('click', function () {
        var questionText = questionInput.value.trim();
        if (questionText !== "") {
            var li_1 = document.createElement('li');
            li_1.textContent = questionText;
            li_1.addEventListener('click', function () {
                document.querySelectorAll('#questionList li').forEach(function (item) { return item.classList.remove('selected'); });
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
        var title = quizTitle.value.trim() || "Questionnaire sans titre";
        var questions = Array.from(questionList.querySelectorAll('li')).map(function (li) { var _a; return (_a = li.textContent) !== null && _a !== void 0 ? _a : ""; });
        if (questions.length > 0) {
            downloadQuestionsAsHTML(title, questions);
            alert("Questionnaire \"".concat(title, "\" cr\u00E9\u00E9 avec ").concat(questions.length, " questions."));
            console.log({ title: title, questions: questions });
        }
        else {
            alert("Aucune question à enregistrer.");
        }
    });
}
else {
    console.error('Un ou plusieurs éléments manquent dans le DOM.');
}
