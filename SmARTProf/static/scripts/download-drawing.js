document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');

    // Function to update the feedback label with a provided message
    function updateFeedbackLabel(message) {
        const feedbackLabel = document.getElementById('feedback-label');
        if (feedbackLabel) {
            feedbackLabel.textContent = message;
            console.log("Feedback updated:", message);
        } else {
            console.log("Feedback label not found.");
        }
    }

    // Function to get the image data from the canvas as a base64-encoded string
    function getImageData() {
        if (!canvas) {
            console.error("Canvas element not found.");
            return null;
        }
        return canvas.toDataURL('image/png'); // Get the image data as base64
    }

    // Function to save the drawing based on the grid squares
    function saveDrawing() {
        const squareContainer = document.getElementById('squareContainer');
        const squares = squareContainer.getElementsByClassName('squares');

        // Clear the canvas before drawing
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Fill the canvas with white first
        ctx.fillStyle = 'white'; // Set the fill color to white
        ctx.fillRect(0, 0, canvas.width, canvas.height); // Fill the entire canvas

        // Loop through each square to check its color
        for (let i = 0; i < squares.length; i++) {
            const square = squares[i];
            const backgroundColor = window.getComputedStyle(square).backgroundColor;

            // Check if the square is black
            if (backgroundColor === 'rgb(0, 0, 0)') { // black in RGB
                const row = Math.floor(i / 30); // Get the row number
                const col = i % 30; // Get the column number

                // Draw the corresponding square on the canvas
                ctx.fillStyle = 'black'; // Color for drawn squares
                ctx.fillRect(col * 10, row * 10, 10, 10); // Draw 10x10 square
            }
        }

        // Now, send the canvas image to the server
        sendRequestAndUpdateFeedback();
    }

    // Function to send the image data to the server and update feedback
    function sendRequestAndUpdateFeedback() {
        // Get the image data
        const imageData = getImageData();
        if (!imageData) {
            updateFeedbackLabel("Error: Unable to capture image data.");
            return; // Exit if no image data is available
        }

        // Prepare the request payload
        const requestData = {
            image: imageData // Include the image data in the request
        };

        // Send the request to the server
        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.feedback) {
                // Update the feedback label with the server's response
                updateFeedbackLabel(data.feedback);
            } else if (data.error) {
                // Display the error message
                updateFeedbackLabel("Error: " + data.error);
            }
        })
        .catch(error => {
            // Handle network errors or other issues
            console.error("Request failed:", error);
            updateFeedbackLabel("An error occurred during the request.");
        });
    }

    // To trigger the saveDrawing function when the finish button is clicked
    document.querySelector('.finish-button').addEventListener('click', () => {
        console.log("Finish button clicked.");
        saveDrawing();
    });
});
