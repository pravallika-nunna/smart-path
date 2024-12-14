document.addEventListener("DOMContentLoaded", () => {
    const resultsContainer = document.getElementById("results");
    const quizData = JSON.parse(document.getElementById("quizResultsData").textContent); // Fetch quiz data from Flask's context variable

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

    const categoryDescriptions = {
        "Declarative Knowledge": "Understanding your strengths, weaknesses, and the type of information most important to learn.",
        "Procedural Knowledge": "Knowing how to apply specific strategies effectively during learning.",
        "Conditional Knowledge": "Knowing when and why to apply strategies in different situations.",
        "Planning": "Setting goals, allocating time, and identifying learning requirements before starting tasks.",
        "Information Management Strategies": "Organizing, summarizing, and connecting new information to what you already know.",
        "Comprehension Monitoring": "Regularly checking your understanding and progress during learning.",
        "Debugging Strategies": "Identifying and correcting errors or gaps in comprehension.",
        "Evaluation": "Reflecting on your learning process and outcomes to improve future performance."
    };

    // Define evaluation metrics
    const evaluationMetrics = {
        "Declarative Knowledge": {
            above_half: "You demonstrate a strong understanding of your strengths and weaknesses, prioritize key learning areas, and effectively retain relevant information.",
            below_half: "You struggle with organizing information effectively and may lack clarity on what is most critical to learn."
        },
        "Procedural Knowledge": {
            above_half: "You effectively apply strategies and adjust approaches as needed for successful learning.",
            below_half: "You may not consistently apply effective strategies, which can hinder optimal learning."
        },
        "Conditional Knowledge": {
            above_half: "You excel at adapting strategies to different situations and motivating yourself effectively.",
            below_half: "You may struggle to identify the best moments to apply specific strategies."
        },
        "Planning": {
            above_half: "You carefully allocate time, set specific goals, and evaluate learning requirements before starting tasks.",
            below_half: "You may skip self-questioning or goal-setting, which can reduce learning efficiency."
        },
        "Information Management Strategies": {
            above_half: "You organize and connect new knowledge effectively with prior learning.",
            below_half: "You may not use techniques like diagrams or structured note-taking to manage information effectively."
        },
        "Comprehension Monitoring": {
            above_half: "You regularly check progress and review strategies to ensure effective learning.",
            below_half: "You may overlook evaluating strategy effectiveness or assessing comprehension periodically."
        },
        "Debugging Strategies": {
            above_half: "You proactively identify and resolve errors or gaps in understanding.",
            below_half: "You may struggle to pinpoint issues and adjust strategies when confused."
        },
        "Evaluation": {
            above_half: "You reflect on learning outcomes and adjust strategies for better performance.",
            below_half: "You may lack a structured approach to analyzing performance or refining strategies."
        }
    };

    // Calculate scores for each category and determine feedback
    const scores = {};
    const feedback = {};
    for (const [category, questions] of Object.entries(categories)) {
        const score = questions.reduce((score, questionIndex) => {
            const question = quizData.find(q => q.id === questionIndex);
            return score + (question && question.userAnswer === 1 ? 1 : 0);
        }, 0);

        // Determine feedback based on score
        const totalQuestions = categories[category].length;
        const halfScore = totalQuestions / 2;

        scores[category] = score;
        feedback[category] = score >= halfScore ? evaluationMetrics[category].above_half : evaluationMetrics[category].below_half;
    }

    // Render results
    resultsContainer.innerHTML = Object.entries(scores)
        .map(([category, score]) => {
            const totalQuestions = categories[category].length;
            return `
                <div class="category">
                    <h3>${category} 
                        <span class="info-icon" title="${categoryDescriptions[category]}">ℹ️</span>
                    </h3>
                    <p>Score: <span>${score}/${totalQuestions}</span></p>
                    <p>Feedback: <span>${feedback[category]}</span></p>
                </div>
            `;
        })
        .join("");

    // Add tooltip styles for information icons
    const style = document.createElement("style");
    style.innerHTML = `
        .info-icon {
            cursor: pointer;
            font-size: 14px;
            margin-left: 5px;
            color: #007BFF;
        }
        .info-icon:hover::after {
            content: attr(title);
            position: absolute;
            background: #f8f9fa;
            border: 1px solid #ced4da;
            border-radius: 5px;
            padding: 5px;
            color: #212529;
            white-space: nowrap;
            z-index: 1000;
            top: 20px;
            left: 0;
        }
    `;
    document.head.appendChild(style);
});
