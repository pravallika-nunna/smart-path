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
            above_half: "Individuals demonstrate a strong understanding of their intellectual strengths and weaknesses, prioritize learning topics they find interesting, and effectively remember information relevant to the topic.",
            below_half: "Individuals struggle with organizing information effectively and lack clarity on what kind of information is most critical to learn."
        },
        "Procedural Knowledge": {
            above_half: "Individuals use purposeful strategies and are aware of the techniques they apply when studying, ensuring they can adjust approaches as needed.",
            below_half: "Individuals lack consistency in applying powerful strategies and do not always automatically use helpful learning methods."
        },
        "Conditional Knowledge": {
            above_half: "Individuals excel at adapting strategies to different situations and can motivate themselves effectively when needed.",
            below_half: "Individuals face challenges in recognizing the most effective moments to apply specific strategies."
        },
        "Planning": {
            above_half: "Individuals carefully allocate time, set specific goals, and evaluate learning requirements before starting tasks.",
            below_half: "Individuals often begin tasks without proper self-questioning or goal-setting, which hinders efficient learning."
        },
        "Information Management Strategies": {
            above_half: "Individuals focus on key information, create meaningful examples, and connect new knowledge with prior learning effectively.",
            below_half: "Individuals rarely use visual aids like diagrams and struggle with breaking information into manageable parts."
        },
        "Comprehension Monitoring": {
            above_half: "Individuals regularly evaluate their progress, review their strategies, and ensure comprehension through periodic checks.",
            below_half: "Individuals do not frequently analyze strategy effectiveness or pause to assess understanding during learning."
        },
        "Debugging Strategies": {
            above_half: "Individuals seek help proactively, reassess assumptions when confused, and adjust strategies to correct errors effectively.",
            below_half: "Individuals fail to identify and resolve comprehension gaps or performance issues efficiently."
        },
        "Evaluation": {
            above_half: "Individuals reflect critically on their performance and adjust strategies based on outcomes to enhance future learning.",
            below_half: "Individuals lack a structured approach to analyzing their performance or refining their strategies after learning sessions."
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

    // Style tooltips
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