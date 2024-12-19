let threadId = null;

document.addEventListener('DOMContentLoaded', async () => {
    // Inicializar el thread al cargar la página
    const response = await fetch('/api/create-thread', {
        method: 'POST'
    });
    const data = await response.json();
    threadId = data.thread_id;
    
    const sendButton = document.getElementById('send-button');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    
    sendButton.addEventListener('click', async () => {
        const message = messageInput.value;
        if (!message.trim()) return;
        
        // Mostrar mensaje del usuario
        addMessage('user', message);
        messageInput.value = '';
        
        // Enviar mensaje al backend
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    threadId: threadId,
                    message: message
                })
            });
            
            const data = await response.json();
            
            // Mostrar respuesta del asistente
            addMessage('assistant', data.response);
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('assistant', 'Lo siento, ha ocurrido un error.');
        }
    });
    
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${role}-message`);
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}); 