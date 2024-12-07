let currentQuestionIndex = 0;
let questions = [];

// Fetch questions from the JSON file
fetch('questions.json')
    .then(response => response.json())
    .then(data => {
        questions = data.questions; // Assign the loaded questions
        loadQuestion(currentQuestionIndex); // Load the first question
    })
    .catch(error => console.error("Error loading questions:", error));

// Function to load a specific question
function loadQuestion(index) {
    const questionText = document.getElementById("question-text");
    const optionsList = document.getElementById("options-list");

    // Get the current question
    const question = questions[index];

    // Update question text
    questionText.innerText = `Question ${index + 1}: ${question.question}`;

    // Clear old options and populate new ones
    optionsList.innerHTML = '';
    const options = ["True", "False"]; // Example options
    options.forEach((option, i) => {
        const listItem = document.createElement("li");
        const radioButton = document.createElement("input");
        radioButton.type = "radio";
        radioButton.name = `q${index + 1}`;
        radioButton.value = i + 1;
        listItem.appendChild(radioButton);
        listItem.appendChild(document.createTextNode(option));
        optionsList.appendChild(listItem);
    });

    // Update button states
    document.getElementById("prev-btn").disabled = index === 0;
    document.getElementById("next-btn").disabled = index === questions.length - 1;
}

// Button handlers
function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        loadQuestion(currentQuestionIndex);
    }
}

function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion(currentQuestionIndex);
    }
}