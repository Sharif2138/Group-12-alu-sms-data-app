// script.js

// Function to fetch data from the backend API
async function fetchData() {
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;

    try {
        // Fetch data from the backend
        const response = await fetch('http://127.0.0.1:5001/transactions');
        const transactions = await response.json();

        // Filter data based on search term and category
        const filteredData = transactions.filter(transaction => {
            const matchesSearch = transaction.description.toLowerCase().includes(searchTerm);
            const matchesCategory = categoryFilter ? transaction.category === categoryFilter : true;
            return matchesSearch && matchesCategory;
        });

        // Update the chart and table
        updateChart(filteredData);
        updateTable(filteredData);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to update the chart
function updateChart(data) {
    const categories = [...new Set(data.map(transaction => transaction.category))];
    const amounts = categories.map(category => {
        return data.filter(transaction => transaction.category === category)
                   .reduce((sum, transaction) => sum + transaction.amount, 0);
    });

    const ctx = document.getElementById('transactionChart').getContext('2d');
    if (window.myChart) {
        window.myChart.destroy(); // Destroy existing chart
    }
    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Total Amount (RWF)',
                data: amounts,
                backgroundColor: ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6610f2', '#6f42c1'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to update the transaction table
function updateTable(data) {
    const tableBody = document.querySelector('#transactionTable tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    data.forEach(transaction => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${transaction.category}</td>
            <td>${transaction.amount}</td>
            <td>${transaction.date}</td>
            <td>${transaction.description}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Initial load
fetchData();