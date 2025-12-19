// Global state
let currentData = null;
let currentFlashcardIndex = 0;
let currentQuestionIndex = 0;
let userAnswers = [];
let quizScore = 0;

// DOM Elements
const topicInput = document.getElementById('topicInput');
const learnBtn = document.getElementById('learnBtn');
const inputSection = document.getElementById('inputSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    learnBtn.addEventListener('click', handleLearn);
    topicInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleLearn();
    });

    // Example topic buttons
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            topicInput.value = btn.dataset.topic;
            handleLearn();
        });
    });

    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            switchTab(btn.dataset.tab);
        });
    });

    // New search button
    document.getElementById('newSearchBtn').addEventListener('click', () => {
        resetApp();
    });
});

// Main function to handle learning
async function handleLearn() {
    const topic = topicInput.value.trim();
    
    if (!topic) {
        showError('Please enter a topic to learn');
        return;
    }

    // Show loading
    inputSection.style.display = 'none';
    loadingSpinner.classList.add('active');
    errorMessage.classList.remove('active');
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/api/learn', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch learning content');
        }

        currentData = data;
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
        inputSection.style.display = 'block';
    } finally {
        loadingSpinner.classList.remove('active');
    }
}

// Display results
function displayResults(data) {
    // Set topic title
    document.getElementById('topicTitle').textContent = data.topic;
    document.getElementById('wikiLink').href = data.wiki_url;

    // Display summary
    document.getElementById('summaryText').textContent = data.summary;

    // Display keywords
    const keywordsList = document.getElementById('keywordsList');
    keywordsList.innerHTML = '';
    data.keywords.forEach(keyword => {
        const tag = document.createElement('span');
        tag.className = 'keyword-tag';
        tag.textContent = keyword;
        keywordsList.appendChild(tag);
    });

    // Setup flashcards
    setupFlashcards(data.flashcards);

    // Setup quiz
    setupQuiz(data.quiz);

    // Display videos
    displayVideos(data.videos);

    // Show results section
    resultsSection.style.display = 'block';
    switchTab('summary');
}

// Tab switching
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.toggle('active', pane.id === `${tabName}Tab`);
    });
}

// Flashcards
function setupFlashcards(flashcards) {
    if (!flashcards || flashcards.length === 0) {
        document.getElementById('flashcardsTab').innerHTML = '<div class="card"><p>No flashcards available for this topic.</p></div>';
        return;
    }

    currentFlashcardIndex = 0;
    displayFlashcard(flashcards[currentFlashcardIndex]);

    // Update counter
    document.getElementById('cardCounter').textContent = `1 / ${flashcards.length}`;

    // Navigation
    const flashcard = document.getElementById('flashcard');
    const prevBtn = document.getElementById('prevCard');
    const nextBtn = document.getElementById('nextCard');

    flashcard.onclick = () => {
        flashcard.classList.toggle('flipped');
    };

    prevBtn.onclick = () => {
        if (currentFlashcardIndex > 0) {
            currentFlashcardIndex--;
            flashcard.classList.remove('flipped');
            displayFlashcard(flashcards[currentFlashcardIndex]);
            document.getElementById('cardCounter').textContent = `${currentFlashcardIndex + 1} / ${flashcards.length}`;
        }
    };

    nextBtn.onclick = () => {
        if (currentFlashcardIndex < flashcards.length - 1) {
            currentFlashcardIndex++;
            flashcard.classList.remove('flipped');
            displayFlashcard(flashcards[currentFlashcardIndex]);
            document.getElementById('cardCounter').textContent = `${currentFlashcardIndex + 1} / ${flashcards.length}`;
        }
    };
}

function displayFlashcard(flashcard) {
    document.getElementById('flashcardQuestion').textContent = flashcard.question;
    document.getElementById('flashcardAnswer').textContent = flashcard.answer;
}

// Quiz
function setupQuiz(quiz) {
    if (!quiz || quiz.length === 0) {
        document.getElementById('quizTab').innerHTML = '<div class="card"><p>No quiz available for this topic.</p></div>';
        return;
    }

    currentQuestionIndex = 0;
    userAnswers = new Array(quiz.length).fill(null);
    quizScore = 0;

    displayQuestion(quiz[currentQuestionIndex]);
    updateQuizNavigation();

    // Navigation
    document.getElementById('prevQuestion').onclick = () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion(quiz[currentQuestionIndex]);
            updateQuizNavigation();
        }
    };

    document.getElementById('nextQuestion').onclick = () => {
        if (currentQuestionIndex < quiz.length - 1) {
            currentQuestionIndex++;
            displayQuestion(quiz[currentQuestionIndex]);
            updateQuizNavigation();
        } else {
            showQuizResults();
        }
    };

    // Retake quiz
    document.getElementById('retakeQuiz').onclick = () => {
        setupQuiz(currentData.quiz);
        document.getElementById('quizResults').style.display = 'none';
        document.getElementById('quizContainer').style.display = 'block';
    };

    document.getElementById('quizTotal').textContent = quiz.length;
}

function displayQuestion(question) {
    const container = document.getElementById('quizQuestion');
    container.innerHTML = '';

    // Question text
    const questionText = document.createElement('div');
    questionText.className = 'question-text';
    questionText.textContent = question.question;
    container.appendChild(questionText);

    // Options
    const optionsDiv = document.createElement('div');
    optionsDiv.className = 'quiz-options';

    // Check if already answered
    const userAnswer = userAnswers[currentQuestionIndex];

    question.options.forEach((option, index) => {
        const optionBtn = document.createElement('button');
        optionBtn.className = 'quiz-option';
        optionBtn.textContent = option;
        
        if (userAnswer) {
            optionBtn.classList.add('disabled');
            if (option === userAnswer) {
                optionBtn.classList.add('selected');
                if (option === question.correct_answer) {
                    optionBtn.classList.add('correct');
                } else {
                    optionBtn.classList.add('incorrect');
                }
            }
            if (option === question.correct_answer) {
                optionBtn.classList.add('correct');
            }
        } else {
            optionBtn.onclick = () => selectAnswer(option, question);
        }

        optionsDiv.appendChild(optionBtn);
    });

    container.appendChild(optionsDiv);

    // Show feedback if already answered
    if (userAnswer) {
        showFeedback(userAnswer === question.correct_answer, question.explanation);
    }
}

function selectAnswer(answer, question) {
    userAnswers[currentQuestionIndex] = answer;
    const isCorrect = answer === question.correct_answer;
    
    if (isCorrect) {
        quizScore++;
        document.getElementById('quizScore').textContent = quizScore;
    }

    displayQuestion(question);
}

function showFeedback(isCorrect, explanation) {
    const container = document.getElementById('quizQuestion');
    const feedback = document.createElement('div');
    feedback.className = `quiz-feedback ${isCorrect ? 'correct' : 'incorrect'}`;
    feedback.textContent = isCorrect ? '✓ Correct!' : '✗ Incorrect';
    
    if (explanation) {
        const explainText = document.createElement('p');
        explainText.style.marginTop = '0.5rem';
        explainText.style.fontWeight = 'normal';
        explainText.textContent = explanation;
        feedback.appendChild(explainText);
    }
    
    container.appendChild(feedback);
}

function updateQuizNavigation() {
    const quiz = currentData.quiz;
    document.getElementById('questionCounter').textContent = `Question ${currentQuestionIndex + 1} / ${quiz.length}`;
    
    const prevBtn = document.getElementById('prevQuestion');
    const nextBtn = document.getElementById('nextQuestion');
    
    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.textContent = currentQuestionIndex === quiz.length - 1 ? 'Finish Quiz' : 'Next →';
}

function showQuizResults() {
    const quiz = currentData.quiz;
    const percentage = Math.round((quizScore / quiz.length) * 100);
    
    document.getElementById('quizContainer').style.display = 'none';
    document.getElementById('quizResults').style.display = 'block';
    document.getElementById('finalScore').textContent = `${quizScore} / ${quiz.length} (${percentage}%)`;
    
    let message = '';
    if (percentage >= 90) {
        message = 'Outstanding! You\'ve mastered this topic! 🌟';
    } else if (percentage >= 70) {
        message = 'Great job! You have a solid understanding! 👏';
    } else if (percentage >= 50) {
        message = 'Good effort! Review the materials and try again. 📚';
    } else {
        message = 'Keep learning! Practice makes perfect. 💪';
    }
    
    document.getElementById('scoreMessage').textContent = message;
}

// Videos
function displayVideos(videos) {
    const videosList = document.getElementById('videosList');
    videosList.innerHTML = '';

    if (!videos || videos.length === 0) {
        videosList.innerHTML = '<p>No videos available for this topic.</p>';
        return;
    }

    videos.forEach(video => {
        const videoCard = document.createElement('div');
        videoCard.className = 'video-card';
        videoCard.onclick = () => openVideoModal(video.id);

        videoCard.innerHTML = `
            <img src="${video.thumbnail}" alt="${video.title}" class="video-thumbnail">
            <div class="video-info">
                <h4 class="video-title">${video.title}</h4>
                <p class="video-description">${video.description}</p>
            </div>
        `;

        videosList.appendChild(videoCard);
    });

    // Add modal to body if not exists
    if (!document.getElementById('videoModal')) {
        const modal = document.createElement('div');
        modal.id = 'videoModal';
        modal.className = 'video-modal';
        modal.innerHTML = `
            <div class="video-modal-content">
                <button class="close-modal" onclick="closeVideoModal()">×</button>
                <iframe id="videoIframe" class="video-iframe" frameborder="0" allowfullscreen></iframe>
            </div>
        `;
        document.body.appendChild(modal);
    }
}

function openVideoModal(videoId) {
    const modal = document.getElementById('videoModal');
    const iframe = document.getElementById('videoIframe');
    iframe.src = `https://www.youtube.com/embed/${videoId}`;
    modal.classList.add('active');
}

function closeVideoModal() {
    const modal = document.getElementById('videoModal');
    const iframe = document.getElementById('videoIframe');
    iframe.src = '';
    modal.classList.remove('active');
}

// Utility functions
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('active');
    setTimeout(() => {
        errorMessage.classList.remove('active');
    }, 5000);
}

function resetApp() {
    inputSection.style.display = 'block';
    resultsSection.style.display = 'none';
    topicInput.value = '';
    topicInput.focus();
    currentData = null;
    currentFlashcardIndex = 0;
    currentQuestionIndex = 0;
    userAnswers = [];
    quizScore = 0;
}
