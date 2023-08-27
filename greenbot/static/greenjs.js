document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', function() {
        const userMessage = userInput.value;
        addMessage(userMessage, 'user-message');
        userInput.value = '';
        fetchResponse(userMessage);
    });

    function fetchResponse(userMessage) {
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `user_input=${encodeURIComponent(userMessage)}`,
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.response;
            addMessage(botResponse, 'bot-message');
        })
        .catch(error => {
            console.error('Error fetching response:', error);
        });
    }

    function addMessage(message, className) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = message;
        messageDiv.classList.add('chat-message', className);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
