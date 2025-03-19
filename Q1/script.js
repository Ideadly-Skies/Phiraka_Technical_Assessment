// script.js
function generateFibonacci(n) {
    let fib = [0, 1];
    for (let i = 2; i < n; i++) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }
    return fib.slice(0, n);
}

// generate fibonnaci table
function generateTable() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('columns').value);
    const totalNumbers = rows + cols + 2;
    const fibSequence = generateFibonacci(totalNumbers);
    console.log(fibSequence)
    const table = document.getElementById('fibTable');
    table.innerHTML = '';

    for (let i = 0; i < rows; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('td');
            const index = i * cols + j;
            // explicitly check if the value is undefined to accept 0 
            cell.textContent = fibSequence[index] !== undefined ? fibSequence[index] : '';
            row.appendChild(cell);
            console.log(cell) // debugging statement
        }
        table.appendChild(row);
    }
}