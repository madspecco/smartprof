document.addEventListener("DOMContentLoaded", function () {
    const nextRoundButton = document.querySelector('.next-round-button');
    const submitButton = document.querySelector('.finish-button');
    const feedbackLabel = document.getElementById('feedback-label');
    const roundLabel = document.getElementById('round-label');
    const scoreLabel = document.getElementById('score-label');
    const squareContainer = document.getElementById('squareContainer');

    const MAX_ROUNDS = 5;

    function updateFeedbackLabel(message) {
        if (feedbackLabel) {
            feedbackLabel.textContent = message; // Set the feedback message
        } else {
            console.error("Feedback label not found.");
        }
    }

    // Function to fetch a new word and update the display
    function fetchNewWord() {
        const language = getSelectedLanguage(); // Get the selected language from the URL
        fetch(`/next-word?language=${language}`) // Pass the language as a query parameter
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.word) {
                    document.getElementById('word-label').innerText = `Word: ${data.word}`;
                    document.getElementById('context-label').innerText = `Context: ${data.context}`;
                } else {
                    document.getElementById('word-label').innerText = "No word found.";
                    document.getElementById('context-label').innerText = "No context available.";
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }

    // Function to determine the qualitative feedback based on score
    function evaluateScore(score) {
        if (score <= 10) {
            updateFeedbackLabel("You need more practice. Game is over, please restart.");
        } else if (score > 10 && score < 25) {
            updateFeedbackLabel("Pretty good, but you still need training.  Game is over, please restart.");
        } else if (score >= 25) {
            updateFeedbackLabel("Nice! Game is over, please restart.");
        }
    }

    // Function to increment the round and manage the score
    function updateRoundAndScore() {
        if (!feedbackLabel || feedbackLabel.textContent.trim() === "") {
            console.warn("Cannot proceed to the next round: Feedback is empty.");
            updateFeedbackLabel("Please submit your drawing before proceeding."); // Notify the user
            return; // Exit if feedback is empty
        }

        let currentRound = parseInt(roundLabel.textContent.split(":")[1], 10) || 0;
        let currentScore = parseInt(scoreLabel.textContent.split(":")[1], 10) || 0;

        // Check the feedback text
        if (feedbackLabel.textContent.trim() === "Correct!") {
            currentScore += 5; // Increment the score by 5 if the feedback is "Correct!"
        }

        scoreLabel.innerText = `S:${currentScore}`;

        // Check if current round has reached the maximum
        if (currentRound >= MAX_ROUNDS) {
            evaluateScore(currentScore); // Evaluate score and provide feedback at game over
            nextRoundButton.disabled = true;
            submitButton.disabled = true;
            return;
        }

        // Increment the round
        currentRound += 1;

        // Update the Round and Score labels
        roundLabel.innerText = `R:${currentRound}`;
        scoreLabel.innerText = `S:${currentScore}`;

        // Clear the feedback label for the next round
        feedbackLabel.textContent = '';

        // Clear the board (resetting squares)
        clearBoard();

        console.log(`Round updated to: ${currentRound}, Score updated to: ${currentScore}`);

        // Fetch a new word for the next round
        fetchNewWord();
    }

    // Function to clear the board
    function clearBoard() {
        const squares = squareContainer.getElementsByClassName('squares');
        for (let square of squares) {
            square.style.backgroundColor = ''; // Reset the square background color
        }
    }

    // Function to get selected language from the URL
    function getSelectedLanguage() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('language'); // Gets the value of 'language' parameter
    }

    // Add event listener for the Next Round button
    if (nextRoundButton) {
        nextRoundButton.addEventListener('click', updateRoundAndScore);
    } else {
        console.error("Next Round button not found.");
    }
});
