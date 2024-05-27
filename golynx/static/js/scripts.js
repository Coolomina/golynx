var ws = null;

function connect() {
    ws = new WebSocket("ws://" + window.location.host + "/cable");

    ws.onopen = function(event) {
        console.log("WebSocket connected!");
    };

    ws.onmessage = function(event) {
        var messagesDiv = document.getElementById("messages");
        messagesDiv.innerHTML += "<p>" + event.data + "</p>";
    };
}

function disconnect() {
    if (ws !== null) {
        ws.close();
        ws = null;
        console.log("WebSocket disconnected!");
    }
}

function sendMessage() {
    var messageInput = document.getElementById("messageInput");
    var message = messageInput.value;
    if (ws !== null && message !== "") {
        ws.send(message);
        messageInput.value = "";
    }
}
document.addEventListener('DOMContentLoaded', function () {
    fetch('/api')
        .then(response => response.json())
        .then(data => {
            const golinksContainer = document.getElementById('golinks');

            Object.keys(data).forEach(key => {
                const golink = data[key];

                const linkDiv = document.createElement('div');
                linkDiv.className = 'golink-item';

                const linkLabel = document.createElement('label');
                linkLabel.textContent = 'Link: ';
                linkDiv.appendChild(linkLabel);

                const linkSpan = document.createElement('span');
                linkSpan.textContent = golink.link;
                linkDiv.appendChild(linkSpan);

                golinksContainer.appendChild(linkDiv);

                const redirectionDiv = document.createElement('div');
                redirectionDiv.className = 'golink-item';

                const redirectionLabel = document.createElement('label');
                redirectionLabel.textContent = 'Redirection: ';
                redirectionDiv.appendChild(redirectionLabel);

                const redirectionLink = document.createElement('a');
                redirectionLink.textContent = golink.redirection;
                redirectionLink.href = golink.redirection;
                redirectionLink.target = '_blank';
                redirectionDiv.appendChild(redirectionLink);

                golinksContainer.appendChild(redirectionDiv);

                const createdByDiv = document.createElement('div');
                createdByDiv.className = 'golink-item';

                const createdByLabel = document.createElement('label');
                createdByLabel.textContent = 'Created By: ';
                createdByDiv.appendChild(createdByLabel);

                const createdBySpan = document.createElement('span');
                createdBySpan.textContent = golink.created_by;
                createdByDiv.appendChild(createdBySpan);

                golinksContainer.appendChild(createdByDiv);

                const separator = document.createElement('hr');
                golinksContainer.appendChild(separator);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            const golinksContainer = document.getElementById('golinks');
            golinksContainer.textContent = 'Error loading data';
        });

    // Handle form submission
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
            alert('GoLink added successfully!');
            location.reload(); // Reload the page to show the new GoLink
        })
        .catch(error => {
            console.error('Error adding GoLink:', error);
            alert('Error adding GoLink');
        });
    });
});