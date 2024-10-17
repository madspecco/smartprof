document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');

    // Function to save the drawing based on the grid squares
    function saveDrawing() {
        const squareContainer = document.getElementById('squareContainer');
        const squares = squareContainer.getElementsByClassName('squares');

        // Clear the canvas before drawing
        ctx.clearRect(0, 0, canvas.width, canvas.height);

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
        sendDrawingToServer();
    }

    function sendDrawingToServer() {
        const dataURL = canvas.toDataURL('image/png');

        fetch('/upload', {
            method: 'POST',
            body: JSON.stringify({ image: dataURL }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // To trigger the saveDrawing function when the finish button is clicked
    document.querySelector('.finish-button').addEventListener('click', saveDrawing);
});
