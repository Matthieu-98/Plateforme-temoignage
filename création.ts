// Sélection des éléments avec typage strict
const addBtn = document.getElementById('addQuestion') as HTMLButtonElement | null;
const deleteBtn = document.getElementById('deleteQuestion') as HTMLButtonElement | null;
const createBtn = document.getElementById('createQuiz') as HTMLButtonElement | null;
const questionInput = document.getElementById('questionInput') as HTMLTextAreaElement | null;
const questionList = document.getElementById('questionList') as HTMLUListElement | null;

function downloadQuestionsAsHTML(questions: string[]): void {
    const htmlContent = `
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>Questions générées</title></head>
<body><h1>Liste des questions :</h1><ul>${questions.map(q => `<li>${q}</li>`).join('')}</ul></body>
</html>`;

    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'questions.html';
    a.click();
    URL.revokeObjectURL(url);
}

if (addBtn && deleteBtn && createBtn && questionInput && questionList) {
    addBtn.addEventListener('click', () => {
        const questionText = questionInput.value.trim();
        if (questionText !== "") {
            const li = document.createElement('li');
            li.textContent = questionText;
            li.addEventListener('click', () => {
                document.querySelectorAll<HTMLLIElement>('#questionList li')
                        .forEach(item => item.classList.remove('selected'));
                li.classList.add('selected');
            });
            questionList.appendChild(li);
            questionInput.value = "";
        }
    });

    deleteBtn.addEventListener('click', () => {
        const selected = questionList.querySelector<HTMLLIElement>('.selected');
        if (selected) {
            questionList.removeChild(selected);
        } else {
            alert('Veuillez sélectionner une question à supprimer.');
        }
    });

    createBtn.addEventListener('click', () => {
        const questions: string[] = Array.from(questionList.querySelectorAll('li')).map(li => li.textContent ?? "");
        if (questions.length > 0) {
            downloadQuestionsAsHTML(questions);
            alert(`Questionnaire créé avec ${questions.length} questions.`);
            console.log(questions);
        } else {
            alert("Aucune question à enregistrer.");
        }
    });
} else {
    console.error('Un ou plusieurs éléments manquent dans le DOM.');
}
