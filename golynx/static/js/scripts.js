document.addEventListener('DOMContentLoaded', function () {
    function fetchGoLinks() {
        fetch('/api/golinks')
            .then(response => response.json())
            .then(data => {
                const golinksTable = document.querySelector('#golinks tbody');
                golinksTable.innerHTML = '';
                Object.keys(data).forEach(key => {
                    const golink = data[key];
                    const row = document.createElement('tr');

                    const linkCell = document.createElement('td');
                    linkCell.textContent = golink.link;
                    row.appendChild(linkCell);

                    const redirectionCell = document.createElement('td');
                    const redirectionLink = document.createElement('a');
                    redirectionLink.textContent = golink.redirection;
                    redirectionLink.href = golink.redirection;
                    redirectionLink.target = '_blank';
                    redirectionCell.classList.add('break-words');
                    redirectionCell.appendChild(redirectionLink);
                    row.appendChild(redirectionCell);

                    const createdByCell = document.createElement('td');
                    createdByCell.textContent = golink.created_by;
                    row.appendChild(createdByCell);

                    const timesVisitedCell = document.createElement('td');
                    timesVisitedCell.textContent = golink.times_used;
                    row.appendChild(timesVisitedCell);

                    const actionsCell = document.createElement('td');
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.className = 'delete-button';
                    deleteButton.onclick = function () {
                        if (confirm('Are you sure you want to delete this GoLink?')) {
                            fetch(`/api/golink/${golink.link}`, {
                                method: 'DELETE'
                            })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                fetchGoLinks(); // Reload the GoLinks after deletion
                            })
                            .catch(error => {
                                console.error('Error deleting GoLink:', error);
                                alert('Error deleting GoLink');
                            });
                        }
                    };
                    actionsCell.appendChild(deleteButton);
                    row.appendChild(actionsCell);

                    golinksTable.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                const golinksTable = document.querySelector('#golinks tbody');
                const row = document.createElement('tr');
                const cell = document.createElement('td');
                cell.textContent = 'Error loading data';
                cell.colSpan = 4;
                row.appendChild(cell);
                golinksTable.appendChild(row);
            });
    }

    function fetchConfig() {
        fetch('/config')
            .then(response => response.json())
            .then(data => {
                console.log(data);
            });
    }
    fetchConfig();
    fetchGoLinks();
    const form = document.getElementById('golink-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const link = document.getElementById('link').value;
        const redirection = document.getElementById('redirection').value;

        fetch('/api/golink', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ link, redirection })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            fetchGoLinks(); // Reload the GoLinks after adding a new one
        })
        .catch(error => {
            console.error('Error adding GoLink:', error);
            alert('Error adding GoLink');
        });
    });

    // Log a message to the console
    console.log('Page loaded and script executed.');
});