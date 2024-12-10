let currentQuestionIndex = 0;
let questions = [];

// Fetch questions from the JSON file
fetch(`static/questions.json?timestamp=${Date.now()}`) // Prevent caching
    .then((response) => response.json())
    .then((data) => {
        questions = data.questions.map((question, index) => ({
            id: index + 1, // Unique ID for each question
            ...question,
            userAnswer: null, // Initialize userAnswer for each question
        }));
        loadQuestion(currentQuestionIndex); // Load the first question
    })
    .catch((error) => console.error("Error loading questions:", error));

function startQuiz() {
    // Hide the intro card and show the quiz card when the quiz starts
    document.getElementById('intro-card').style.display = 'none';
    document.getElementById('quiz-card').style.display = 'flex';
}

// Function to load a specific question
function loadQuestion(index) {
    const questionText = document.getElementById("question-text");
    const optionsList = document.getElementById("options-list");
    const questionCounter = document.getElementById("question-counter");
    const prevButton = document.getElementById("prev-btn");
    const nextButton = document.getElementById("next-btn");

    document.getElementById("question-card").style.display = "block";
    document.getElementById("thank-you-card").style.display = "none";

    const question = questions[index];

    // Set question text and counter
    questionCounter.innerText = `Question ${index + 1} of ${questions.length}`;
    questionText.innerText = question.question;

    // Clear old options and add new ones
    optionsList.innerHTML = '';
    const options = ["True", "False"];
    options.forEach((option, i) => {
        const listItem = document.createElement("li");
        const radioButton = document.createElement("input");
        radioButton.type = "radio";
        radioButton.name = `q${index + 1}`;
        radioButton.value = i + 1;

        // Retain previously selected answer
        if (question.userAnswer === i + 1) {
            radioButton.checked = true;
        }

        radioButton.addEventListener("change", () => {
            nextButton.disabled = false; // Enable "Next" when an option is selected
        });

        listItem.appendChild(radioButton);
        listItem.appendChild(document.createTextNode(`${option}`));
        optionsList.appendChild(listItem);
    });

    // Disable "Next" button if no answer is selected
    nextButton.disabled = question.userAnswer === null;
    prevButton.style.visibility = index === 0 ? "hidden" : "visible";
    nextButton.innerText = index === questions.length - 1 ? "Finish" : "Next";
}

function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        loadQuestion(currentQuestionIndex);
    }
}

function nextQuestion() {
    const selectedOption = document.querySelector(`input[name="q${currentQuestionIndex + 1}"]:checked`);
    if (!selectedOption) {
        console.log("No option selected for question", currentQuestionIndex + 1); // Debugging log
        alert("Please select an answer before proceeding to the next question."); // Show validation alert
        return;
    }

    // Save the user's answer
    questions[currentQuestionIndex].userAnswer = parseInt(selectedOption.value);

    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion(currentQuestionIndex);
    } else {
        // When on the last question, trigger submit results
        submitResults();
    }
}

function submitResults() {
    // Validate that all questions have been answered
    const unanswered = questions.some(q => q.userAnswer === null);
    if (unanswered) {
        alert("Please answer all questions before submitting.");
        return;
    }

    // Debugging log to ensure correct data is being sent
    console.log("Final Questions Data to Submit:", JSON.stringify(questions, null, 2));

    // Updated: Added additional headers and response handling
    fetch('/submit-results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Ensures Flask reads JSON payload
        },
        body: JSON.stringify(questions), // Send the questions array (with user answers)
    })
    .then(response => {
        if (response.status === 401) {
            // Handle user not logged in
            alert("You must be logged in to submit the quiz. Redirecting to login...");
            window.location.href = "/login"; // Redirect to login page
        } else if (response.ok) {
            // Redirect to results page after submitting
            window.location.href = "/results"; // Redirect to results page
        } else {
            alert("Error submitting results. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error submitting results:", error);
        alert("Error submitting results. Please try again.");
    });
}