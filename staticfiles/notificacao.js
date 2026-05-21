let ultimoIdNotificacao = null;

function checarNovasMensagens() {
    fetch("/checar-notificacoes/")
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notif-badge');

            if (data.total > 0) {
                badge.innerText = data.total;
                badge.style.display = 'inline-block';

                if (data.nova && data.texto !== ultimoIdNotificacao) {
                    if (Notification.permission === "granted") {
                        new Notification(`Mensagem de ${data.remetente}`, {
                            body: data.texto,
                        });
                    }
                    ultimoIdNotificacao = data.texto;
                }
            } else {
                badge.style.display = 'none';
                ultimoIdNotificacao = null;
            }
        });
}

setInterval(checarNovasMensagens, 5000);