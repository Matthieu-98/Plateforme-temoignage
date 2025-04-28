// Sélection des éléments avec typage strict
var addBtn = document.getElementById('addQuestion');
var deleteBtn = document.getElementById('deleteQuestion');
var createBtn = document.getElementById('createQuiz');
var questionInput = document.getElementById('questionInput');
var questionList = document.getElementById('questionList');
// Vérification pour éviter les erreurs si jamais un élément n'existe pas
if (addBtn && deleteBtn && createBtn && questionInput && questionList) {
    addBtn.addEventListener('click', function () {
        var questionText = questionInput.value.trim();
        if (questionText !== "") {
            var li = document.createElement('li');
            li.textContent = questionText;
            questionList.appendChild(li);
            questionInput.value = ""; // Réinitialise le champ après ajout
        }
    });
    deleteBtn.addEventListener('click', function () {
        if (questionList.lastChild) {
            questionList.removeChild(questionList.lastChild);
        }
    });
    createBtn.addEventListener('click', function () {
        var questions = [];
        questionList.querySelectorAll('li').forEach(function (li) {
            var _a;
            questions.push((_a = li.textContent) !== null && _a !== void 0 ? _a : "");
        });
        // Action à faire avec les questions (exemple : les afficher ou les envoyer au serveur)
        alert("Questionnaire cr\u00E9\u00E9 avec ".concat(questions.length, " questions."));
        console.log(questions);
    });
}
else {
    console.error('Un ou plusieurs éléments n\'ont pas été trouvés dans le DOM.');
}
