document.addEventListener('DOMContentLoaded', function () {
    // Swap the transparent hero navbar to a solid one once the user scrolls past it
    const nav = document.getElementById('mainNav');
    if (nav && nav.classList.contains('tp-navbar-transparent')) {
        const toggleNav = function () {
            nav.classList.toggle('is-scrolled', window.scrollY > 80);
        };
        window.addEventListener('scroll', toggleNav);
        toggleNav();
    }

    // Back-to-top floating button: only show once the user has scrolled down a bit
    const backToTop = document.getElementById('tpBackToTop');
    if (backToTop) {
        const toggleBackToTop = function () {
            backToTop.classList.toggle('tp-floating-hide', window.scrollY < 300);
        };
        window.addEventListener('scroll', toggleBackToTop);
        toggleBackToTop();
        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Auto-dismiss alerts after a few seconds
    document.querySelectorAll('.alert').forEach(function (alertEl) {
        setTimeout(function () {
            const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
            alert.close();
        }, 5000);
    });

    // Chatbot widget (used on chatbot.html)
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        const chatWindow = document.getElementById('chat-window');
        const chatInput = document.getElementById('chat-input');
        const chatSendBtn = chatForm.querySelector('button[type="submit"]');

        function appendBubble(text, who, isError) {
            const div = document.createElement('div');
            div.className = 'chat-bubble ' + who + (isError ? ' error' : '');
            div.textContent = text;
            chatWindow.appendChild(div);
            chatWindow.scrollTop = chatWindow.scrollHeight;
            return div;
        }

        function showTypingIndicator() {
            const div = document.createElement('div');
            div.className = 'chat-bubble bot typing';
            div.innerHTML = '<span></span><span></span><span></span>';
            chatWindow.appendChild(div);
            chatWindow.scrollTop = chatWindow.scrollHeight;
            return div;
        }

        chatForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;
            appendBubble(message, 'user');
            chatInput.value = '';
            chatInput.disabled = true;
            chatSendBtn.disabled = true;
            const typingBubble = showTypingIndicator();

            try {
                const response = await fetch(chatForm.dataset.endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': chatForm.dataset.csrf,
                    },
                    body: JSON.stringify({ message: message }),
                });
                const data = await response.json();
                typingBubble.remove();
                appendBubble(data.reply, 'bot', !response.ok);
            } catch (err) {
                typingBubble.remove();
                appendBubble('Sorry, something went wrong. Please try again.', 'bot', true);
            } finally {
                chatInput.disabled = false;
                chatSendBtn.disabled = false;
                chatInput.focus();
            }
        });
    }
});
