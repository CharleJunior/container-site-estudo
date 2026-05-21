document.addEventListener('DOMContentLoaded', function() {
    scrollFinal();
});

function scrollFinal() {
    const chatBox = document.getElementById('msg-box');
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}