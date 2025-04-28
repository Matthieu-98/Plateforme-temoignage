// Sélection des éléments avec typage strict
const addBtn = document.getElementById('addQuestion') as HTMLButtonElement;
const deleteBtn = document.getElementById('deleteQuestion') as HTMLButtonElement;
const createBtn = document.getElementById('createQuiz') as HTMLButtonElement;
const questionInput = document.getElementById('questionInput') as HTMLTextAreaElement;
const questionList = document.getElementById('questionList') as HTMLUListElement;

// Vérification pour éviter les erreurs si jamais un élément n'existe pas
if (addBtn && deleteBtn && createBtn && questionInput && questionList) {
  
  addBtn.addEventListener('click', () => {
    const questionText: string = questionInput.value.trim();
    if (questionText !== "") {
      const li: HTMLLIElement = document.createElement('li');
      li.textContent = questionText;
      questionList.appendChild(li);
      questionInput.value = ""; // Réinitialise le champ après ajout
    }
  });

  deleteBtn.addEventListener('click', () => {
    if (questionList.lastChild) {
      questionList.removeChild(questionList.lastChild);
    }
  });

  createBtn.addEventListener('click', () => {
    const questions: string[] = [];
    questionList.querySelectorAll('li').forEach((li: HTMLLIElement) => {
      questions.push(li.textContent ?? "");
    });

    // Action à faire avec les questions (exemple : les afficher ou les envoyer au serveur)
    alert(`Questionnaire créé avec ${questions.length} questions.`);
    console.log(questions);
  });

} else {
  console.error('Un ou plusieurs éléments n\'ont pas été trouvés dans le DOM.');
}
