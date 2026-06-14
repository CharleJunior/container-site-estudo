document.addEventListener("DOMContentLoaded", function () {
    const msgBox = document.getElementById("msg-box");
    const btnVoltar = document.getElementById("btn-voltar-contatos");
    const chatWrapper = document.querySelector(".chat-wrapper");

    if (msgBox) {
        msgBox.scrollTop = msgBox.scrollHeight;
    }

 
    function checarResponsividade() {
        if (window.innerWidth <= 768) {
            if (btnVoltar) btnVoltar.style.display = "block";
        } else {
            if (btnVoltar) btnVoltar.style.display = "none";
        }
    }

 
    checarResponsividade();
    window.addEventListener("resize", checarResponsividade);

    if (btnVoltar) {
        btnVoltar.addEventListener("click", function () {
            if (chatWrapper) {
                chatWrapper.classList.remove("chat-ativo");
            }
 
            const novaUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
            window.history.pushState({ path: novaUrl }, '', novaUrl);
        });
    }
});