document.addEventListener('DOMContentLoaded', function() {
    // Show the default page on load
    showPage('home');
});

function showPage(pageId) {
    var pages = document.querySelectorAll('.page');
    pages.forEach(function(page) {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

function openPopup() {
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('popup').style.display = 'none';
}
function toggleTransferForm() {
    var sendSection = document.getElementById('send');
    var popup = document.getElementById('popup');
    
    if (popup.style.display === 'block') {
        popup.style.display = 'none';
        sendSection.style.display = 'block'; // Show the send section
    } else {
        popup.style.display = 'block';
        sendSection.style.display = 'none'; // Hide the send section
    }
}

function submitForm() {
    var fromEmail = document.getElementById('fromEmail').value;
    var toEmail = document.getElementById('toEmail').value;
    var amount = document.getElementById('amount').value;

    fetch('/transfer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fromEmail: fromEmail, toEmail: toEmail, amount: amount }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closePopup();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
