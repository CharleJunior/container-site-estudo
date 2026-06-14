document.addEventListener("DOMContentLoaded", function() {
        const btnToggle = document.getElementById("btn-toggle-post");
        const formContainer = document.getElementById("form-postagem-container");
        const iconToggle = document.getElementById("icon-toggle-post");
        const textToggle = document.getElementById("text-toggle-post");

        if (btnToggle && formContainer) {
            btnToggle.addEventListener("click", function() {
                if (formContainer.style.display === "none") {
                    formContainer.style.display = "block";
                    textToggle.textContent = "Fechar";
                    btnToggle.classList.replace("btn-primary", "btn-secondary");
                    iconToggle.className = "fa-solid fa-circle-xmark";
                } else {
                    formContainer.style.display = "none";
                    textToggle.textContent = "Nova Postagem";
                    btnToggle.classList.replace("btn-secondary", "btn-primary");
                    iconToggle.className = "fa-solid fa-circle-plus";
                }
            });
        }
    });