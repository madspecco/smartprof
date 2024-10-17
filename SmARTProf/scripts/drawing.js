// Constants from HTML
const squareContainer = document.querySelector('#squareContainer');
const erasebtn = document.querySelector('#erasebtn');
const clearbtn = document.querySelector('#clearbtn');

// Default Settings
const DEFAULT_COLOR = 'black'; // Drawing color set to black
const DEFAULT_SIZE = 30; // Change to 30 for a 30x30 grid

let currentMode = 'color'; // Default mode set to draw
let currentSize = DEFAULT_SIZE;

let mouseDown = false;
document.body.onmousedown = () => (mouseDown = true);
document.body.onmouseup = () => (mouseDown = false);

// Utility Functions
function setCurrentSize(newSize) {
    currentSize = newSize;
}

function reloadGrid() {
    squareContainer.innerHTML = '';
    createGrid(currentSize);
}

function createGrid(size) {
    squareContainer.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    squareContainer.style.gridTemplateRows = `repeat(${size}, 1fr)`;

    for (let i = 0; i < size * size; i++) {
        const square = document.createElement('div');
        square.classList.add('squares');

        square.addEventListener('mouseover', fill);
        square.addEventListener('mousedown', fill);

        squareContainer.appendChild(square);
    }
}

// Add color to a square (drawing with black)
function fill(e) {
    if (e.type === 'mouseover' && !mouseDown) return;

    if (currentMode === 'color') {
        e.target.style.backgroundColor = DEFAULT_COLOR;
    } else if (currentMode === 'erase') {
        e.target.style.backgroundColor = 'white';
    }
}

// Toggle Erase Mode
erasebtn.onclick = () => {
    if (currentMode === 'color') {
        currentMode = 'erase'; // Switch to erase mode
        erasebtn.classList.add('toggled');
    } else {
        currentMode = 'color'; // Switch back to draw mode
        erasebtn.classList.remove('toggled');
    }
};

// Clear Grid
clearbtn.addEventListener('click', reloadGrid);

// Set up the grid on page load
window.onload = () => {
    createGrid(DEFAULT_SIZE);
};
