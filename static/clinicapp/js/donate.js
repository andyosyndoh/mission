// Toggle between Bank Transfer and M-Pesa forms
document.querySelectorAll('input[name="paymentMethod"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        if (e.target.value === 'bank') {
            document.getElementById('bankTransferForm').style.display = 'block';
            document.getElementById('mpesaForm').style.display = 'none';
        } else {
            document.getElementById('bankTransferForm').style.display = 'none';
            document.getElementById('mpesaForm').style.display = 'block';
        }
    });
});

// Handle bank donation form submission
document.getElementById('bankDonationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const response = await fetch('/donate/bank/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                country: document.getElementById('country').value,
                amount: document.getElementById('amount').value,
                currency: document.getElementById('currency').value
            })
        });
        const data = await response.json();
        if (data.status === 'success') {
            alert('Bank details have been generated. Please check your email.');
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
});

// Handle M-Pesa form submission
document.getElementById('mpesaDonationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const response = await fetch('/donate/mpesa/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                name: document.getElementById('mpesaName').value,
                phone_number: document.getElementById('mpesaPhone').value,
                amount: document.getElementById('mpesaAmount').value
            })
        });
        const data = await response.json();
        if (data.status === 'success') {
            alert('Please check your phone for the M-Pesa prompt');
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}