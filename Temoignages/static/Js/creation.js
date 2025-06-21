document.addEventListener('DOMContentLoaded', function() {
    const addQuestionBtn = document.getElementById('addQuestion');
    const deleteQuestionBtn = document.getElementById('deleteQuestion');
    const createQuizBtn = document.getElementById('createQuiz');
    const questionInput = document.getElementById('questionInput');
    const questionList = document.getElementById('questionList');

    let questions = [];
    let selectedQuestionIndex = null;

    // Ajouter une question
    addQuestionBtn.addEventListener('click', () => {
        const text = questionInput.value.trim();
        const requiredCheckbox = document.getElementById('requiredCheckbox');
        if (text) {
            questions.push({ text: text, required: requiredCheckbox.checked }); // Par défaut "obligatoire"
            questionInput.value = '';
            renderQuestionList();
        }
    });

    // Supprimer la question sélectionnée
    deleteQuestionBtn.addEventListener('click', () => {
        if (selectedQuestionIndex !== null) {
            questions.splice(selectedQuestionIndex, 1);
            selectedQuestionIndex = null;
            renderQuestionList();
        }
    });

    // Créer le questionnaire
    createQuizBtn.addEventListener('click', () => {
        // Ici tu peux envoyer les questions via AJAX ou un POST classique
        console.log('Questions:', questions);

        // Exemple : simple alert + redirection
        alert('Le questionnaire a été créé avec ' + questions.length + ' question(s).');
        window.location.href = redirectUrl;
    });

    // Afficher la liste des questions
    function renderQuestionList() {
        questionList.innerHTML = '';
        questions.forEach((q, index) => {
            const li = document.createElement('li');
            li.className = index === selectedQuestionIndex ? 'selected' : '';

            if (q.required) {
            li.classList.add('required');  // Ajoute classe si obligatoire
            }

            // Texte de la question
            const textSpan = document.createElement('span');
            textSpan.textContent = q.text;

            // Checkbox "Obligatoire"
            const label = document.createElement('label');
            label.style.marginLeft = '10px';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'required-checkbox';
            checkbox.checked = q.required;
            checkbox.addEventListener('change', () => {
                q.required = checkbox.checked;
            });

            label.appendChild(checkbox);
            label.appendChild(document.createTextNode('Obligatoire'));

            // Sélectionner une question au clic
            li.addEventListener('click', (e) => {
                // On évite que le clic sur la checkbox sélectionne l'élément
                if (e.target.tagName.toLowerCase() !== 'input') {
                    selectedQuestionIndex = index;
                    renderQuestionList();
                }
            });

            li.appendChild(textSpan);
            li.appendChild(label);
            questionList.appendChild(li);
        });
    }
});
