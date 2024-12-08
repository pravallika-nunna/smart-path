document.addEventListener("DOMContentLoaded", () => {
    const resultsContainer = document.getElementById("results");
    const quizData = JSON.parse(localStorage.getItem("quizResults"));

    if (!quizData) {
        resultsContainer.innerHTML = "<p>No results found. Please complete the quiz first.</p>";
        return;
    }

    // Define the categories and their question mappings
    const categories = {
        "Declarative Knowledge": [5, 10, 12, 16, 17, 20, 32, 46],
        "Procedural Knowledge": [3, 14, 15, 18, 26, 27, 29, 33, 35],
        "Conditional Knowledge": [19, 30, 37, 39, 40, 41, 43, 49],
        "Planning": [4, 6, 8, 22, 23, 42, 45],
        "Information Management Strategies": [9, 13, 30, 31, 37, 39, 41, 43, 47, 48],
        "Comprehension Monitoring": [1, 2, 11, 21, 28, 34, 49],
        "Debugging Strategies": [7, 25, 40, 44, 51, 52],
        "Evaluation": [7, 18, 24, 36, 38, 50],
    };

    // Calculate scores for each category
    const scores = {};
    for (const [category, questions] of Object.entries(categories)) {
        scores[category] = questions.reduce((score, questionIndex) => {
            const question = quizData.find(q => q.id === questionIndex);
            return score + (question && question.userAnswer === 1 ? 1 : 0);
        }, 0);
    }

    // Render results
    resultsContainer.innerHTML = Object.entries(scores)
        .map(([category, score]) => {
            const totalQuestions = categories[category].length;
            return `<div class="category">${category}: <span>${score}/${totalQuestions}</span></div>`;
        })
        .join("");
});
