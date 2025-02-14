// Sample transaction data
const transactions = [
    { type: "Incoming Money", amount: 5000, date: "2024-01-01" },
    { type: "Payments", amount: 1500, date: "2024-01-02" },
    { type: "Airtime", amount: 3000, date: "2024-01-03" },
    { type: "Withdrawals", amount: 20000, date: "2024-01-04" },
    { type: "Internet Bundle", amount: 2000, date: "2024-01-05" }
];

// Function to populate table
function loadTransactions() {
    let tableBody = document.querySelector("#transactionTable tbody");
    tableBody.innerHTML = ""; // Clear previous data

    transactions.forEach(tx => {
        let row = `<tr>
            <td>${tx.type}</td>
            <td>${tx.amount}</td>
            <td>${tx.date}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

// Function to filter table
function filterTable() {
    let input = document.getElementById("search").value.toLowerCase();
    let rows = document.querySelectorAll("#transactionTable tbody tr");

    rows.forEach(row => {
        let text = row.innerText.toLowerCase();
        row.style.display = text.includes(input) ? "" : "none";
    });
}

// Function to generate Chart
function loadChart() {
    let ctx = document.getElementById("transactionChart").getContext("2d");

    let categories = {};
    transactions.forEach(tx => {
        categories[tx.type] = (categories[tx.type] || 0) + tx.amount;
    });

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: Object.keys(categories),
            datasets: [{
                label: "Transaction Amount (RWF)",
                data: Object.values(categories),
                backgroundColor: "blue"
            }]
        }
    });
}

// Load data when the page loads
window.onload = function () {
    loadTransactions();
    loadChart();
};
