// Sélection des éléments avec typage strict
var addBtn = document.getElementById('addQuestion');
var deleteBtn = document.getElementById('deleteQuestion');
var createBtn = document.getElementById('createQuiz');
var questionInput = document.getElementById('questionInput');
var questionList = document.getElementById('questionList');
var quizTitle = document.getElementById('quizTitle');

// Utilitaire pour récupérer le token CSRF de Django
function getCSRFToken() {
    var csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfElement) {
        return csrfElement.value;
    } else {
        console.warn("Token CSRF non trouvé dans la page.");
        return '';
    }
}

// Fonction d'envoi au serveur
function sendQuestionsToServer(title, questions) {
    fetch('/questionnaire/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({title, questions: questions }),
    })
    .then(response => {
        if (response.ok) {
            alert(`Questionnaire "${title}" créé avec ${questions.length} questions.`);
            // Rediriger vers la liste des questionnaires privés
            window.location.href = redirectUrl;

        } else {
            throw new Error('Erreur lors de l’envoi au serveur.');
        }
    })
    .catch(error => {
        console.error('Erreur :', error);
        alert("Erreur lors de l'envoi du questionnaire.");
    });
}

// Initialisation des boutons
if (addBtn && deleteBtn && createBtn && questionInput && questionList && quizTitle) {
    addBtn.addEventListener('click', function () {
        var questionText = questionInput.value.trim();
        if (questionText !== "") {
            var li = document.createElement('li');
            li.textContent = questionText;
            li.addEventListener('click', function () {
                document.querySelectorAll('#questionList li').forEach(item => item.classList.remove('selected'));
                li.classList.add('selected');
            });
            questionList.appendChild(li);
            questionInput.value = "";
        }
    });

    deleteBtn.addEventListener('click', function () {
        var selected = questionList.querySelector('.selected');
        if (selected) {
            questionList.removeChild(selected);
        } else {
            alert('Veuillez sélectionner une question à supprimer.');
        }
    });

    createBtn.addEventListener('click', function () {
        var title = quizTitle.value.trim() || "Questionnaire sans titre";
        var questions = Array.from(questionList.querySelectorAll('li')).map(li => li.textContent || "");
        if (questions.length > 0) {
            sendQuestionsToServer(title, questions);
        } else {
            alert("Aucune question à enregistrer.");
        }
    });
} else {
    console.error('Un ou plusieurs éléments manquent dans le DOM.');
}
