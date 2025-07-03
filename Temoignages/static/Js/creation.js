document.addEventListener('DOMContentLoaded', function () {
    const addQuestionBtn = document.getElementById('addQuestion');
    const deleteQuestionBtn = document.getElementById('deleteQuestion');
    const createQuizBtn = document.getElementById('createQuiz');
    const questionInput = document.getElementById('questionInput');
    const questionList = document.getElementById('questionList');
    const quizTitleInput = document.getElementById('quizTitle');

    let questions = [];
    let selectedQuestionIndex = null;

    //  Récupération depuis localStorage
    const savedTitle = localStorage.getItem('draft_title');
    const savedQuestions = localStorage.getItem('draft_questions');

    if (savedTitle) quizTitleInput.value = savedTitle;
    if (savedQuestions) {
        questions = JSON.parse(savedQuestions);
        renderQuestionList();
    }

    function saveToLocalStorage() {
        localStorage.setItem('draft_title', quizTitleInput.value.trim());
        localStorage.setItem('draft_questions', JSON.stringify(questions));
    }

    quizTitleInput.addEventListener('input', saveToLocalStorage);

    addQuestionBtn.addEventListener('click', () => {
        const text = questionInput.value.trim();
        const requiredCheckbox = document.getElementById('requiredCheckbox');

        if (text) {
            questions.push({ text: text, required: requiredCheckbox.checked });
            questionInput.value = '';
            requiredCheckbox.checked = false;
            saveToLocalStorage();
            renderQuestionList();
        } else {
            alert('Veuillez saisir une question.');
        }
    });

    deleteQuestionBtn.addEventListener('click', () => {
        if (selectedQuestionIndex !== null) {
            questions.splice(selectedQuestionIndex, 1);
            selectedQuestionIndex = null;
            saveToLocalStorage();
            renderQuestionList();
        } else {
            alert("Veuillez sélectionner une question à supprimer.");
        }
    });

    createQuizBtn.addEventListener('click', () => {
        const title = quizTitleInput.value.trim();

        if (!title) {
            alert("Veuillez saisir un titre pour le questionnaire.");
            return;
        }

        if (questions.length === 0) {
            alert("Ajoutez au moins une question.");
            return;
        }

        const isPublic = document.getElementById('isPublicCheckbox')?.checked || false;

        const data = {
            title: title,
            is_public: isPublic,
            questions: questions.map(q => ({
                texte: q.text,
                is_required: q.required
            }))
        };

        if (!createQuestionnaireUrl) {
            console.error("L’URL de création n’est pas définie !");
            return;
        }

        if (!isAuthenticated) {
            alert("Vous devez être connecté pour créer un questionnaire.");
            return;
        }

        fetch(createQuestionnaireUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify(data)
        })
            .then(response => {
                if (!response.ok) throw new Error("Erreur lors de la création");
                return response.json();
            })
            .then(result => {
                alert("Questionnaire créé !");
                localStorage.removeItem('draft_questions');
                localStorage.removeItem('draft_title');
                window.location.href = redirectUrl;
            })
            .catch(error => {
                console.error(error);
                alert("Une erreur est survenue.");
            });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function renderQuestionList() {
        questionList.innerHTML = '';
        questions.forEach((q, index) => {
            const li = document.createElement('li');
            li.className = index === selectedQuestionIndex ? 'selected' : '';
            if (q.required) li.classList.add('required');

            const textSpan = document.createElement('span');
            textSpan.textContent = q.text;

            const label = document.createElement('label');
            label.style.marginLeft = '10px';
            label.className = 'required-label';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'required-checkbox';
            checkbox.checked = q.required;
            checkbox.addEventListener('change', () => {
                q.required = checkbox.checked;
                saveToLocalStorage();
            });

            label.appendChild(checkbox);
            label.appendChild(document.createTextNode('Obligatoire'));

            li.appendChild(textSpan);
            li.appendChild(label);

            li.addEventListener('click', (e) => {
                if (e.target.tagName.toLowerCase() !== 'input') {
                    selectedQuestionIndex = index;
                    renderQuestionList();
                }
            });

            questionList.appendChild(li);
        });
    }
});
