document.addEventListener('DOMContentLoaded', function () {
    // Add loading state management
    function setLoadingState(isLoading) {
        const tbody = document.querySelector('#golinks tbody');
        if (isLoading) {
            tbody.innerHTML = '<tr><td colspan="5" class="loading">LOADING LINKS...</td></tr>';
        }
    }

    function showError(message) {
        const tbody = document.querySelector('#golinks tbody');
        tbody.innerHTML = `<tr><td colspan="5" class="error">${message}</td></tr>`;
    }

    function fetchGoLinks() {
        setLoadingState(true);
        
        fetch('/api/golinks')
            .then(response => response.json())
            .then(data => {
                const golinksTable = document.querySelector('#golinks tbody');
                golinksTable.innerHTML = '';
                
                if (Object.keys(data).length === 0) {
                    const row = document.createElement('tr');
                    const cell = document.createElement('td');
                    cell.textContent = 'NO LINKS YET - ADD ONE BELOW!';
                    cell.colSpan = 5;
                    cell.style.textAlign = 'center';
                    cell.style.fontWeight = '900';
                    cell.style.textTransform = 'uppercase';
                    cell.style.backgroundColor = 'var(--brutal-orange)';
                    row.appendChild(cell);
                    golinksTable.appendChild(row);
                    return;
                }
                
                Object.keys(data).forEach(key => {
                    const golink = data[key];
                    const row = document.createElement('tr');

                    const linkCell = document.createElement('td');
                    linkCell.textContent = golink.link;
                    linkCell.style.fontWeight = '700';
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
                    timesVisitedCell.style.fontWeight = '700';
                    row.appendChild(timesVisitedCell);

                    const actionsCell = document.createElement('td');
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'DELETE';
                    deleteButton.className = 'delete-button';
                    deleteButton.onclick = function () {
                        // Add brutal confirmation dialog styling
                        if (confirm(`⚠️ DELETE "${golink.link}"?\n\nTHIS ACTION CANNOT BE UNDONE!`)) {
                            deleteButton.textContent = 'DELETING...';
                            deleteButton.disabled = true;
                            
                            fetch(`/api/golink/${golink.link}`, {
                                method: 'DELETE'
                            })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                // Add success feedback
                                showSuccessMessage('LINK DELETED!');
                                fetchGoLinks(); // Reload the GoLinks after deletion
                            })
                            .catch(error => {
                                console.error('Error deleting GoLink:', error);
                                alert('❌ ERROR DELETING LINK!');
                                deleteButton.textContent = 'DELETE';
                                deleteButton.disabled = false;
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
                showError('ERROR LOADING LINKS!');
            });
    }

    function showSuccessMessage(message) {
        // Create temporary success message
        const successDiv = document.createElement('div');
        successDiv.textContent = message;
        successDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: var(--brutal-green);
            color: var(--brutal-black);
            padding: 15px 25px;
            border: 4px solid var(--brutal-black);
            box-shadow: 6px 6px 0px var(--brutal-black);
            font-weight: 900;
            text-transform: uppercase;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }

    function fetchConfig() {
        fetch('/config')
            .then(response => response.json())
            .then(data => {
                console.log('Config loaded:', data);
            });
    }

    // Initialize
    fetchConfig();
    fetchGoLinks();

    // Form handling with enhanced UX
    const form = document.getElementById('golink-form');
    const submitButton = form.querySelector('button[type="submit"]');
    const linkInput = document.getElementById('link');
    const redirectionInput = document.getElementById('redirection');
    
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const link = linkInput.value.trim();
        const redirection = redirectionInput.value.trim();

        // Enhanced validation
        if (!link || !redirection) {
            alert('⚠️ PLEASE FILL ALL FIELDS!');
            return;
        }

        if (!redirection.startsWith('http://') && !redirection.startsWith('https://')) {
            if (!confirm('⚠️ URL DOES NOT START WITH HTTP(S)://\n\nCONTINUE ANYWAY?')) {
                return;
            }
        }

        // Update button state
        const originalText = submitButton.textContent;
        submitButton.textContent = 'ADDING...';
        submitButton.disabled = true;

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
            // Success handling
            linkInput.value = '';
            redirectionInput.value = '';
            showSuccessMessage('LINK ADDED!');
            fetchGoLinks(); // Reload the GoLinks after adding a new one
        })
        .catch(error => {
            console.error('Error adding GoLink:', error);
            alert('❌ ERROR ADDING LINK!');
        })
        .finally(() => {
            // Reset button state
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        });
    });

    // Add keyboard shortcuts for better UX
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + Enter to submit form
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            if (linkInput.value && redirectionInput.value) {
                form.dispatchEvent(new Event('submit'));
            }
        }
    });

    // Add CSS animation for success message
    if (!document.querySelector('#success-animation-style')) {
        const style = document.createElement('style');
        style.id = 'success-animation-style';
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Log initialization
    console.log('🦊 GOLYNX BRUTAL MODE ACTIVATED!');
});
