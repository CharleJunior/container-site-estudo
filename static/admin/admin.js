document.addEventListener('change', function(event) {
    if (event.target.classList.contains('status-toggle')) {
        const checkbox = event.target;
        const userId = checkbox.getAttribute('data-user-id') || checkbox.closest('.switch-container').getAttribute('data-user-id');
        const loader = document.getElementById(`loader-${userId}`);

        checkbox.disabled = true;
        loader.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i>'; 

        fetch(`/alternar-status/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log("Salvo!");
                loader.innerHTML = '<i class="fa-solid fa-check" style="color: #2ecc71;"></i>';
            } else {
                checkbox.checked = !checkbox.checked;
                loader.innerHTML = '<i class="fa-solid fa-xmark" style="color: #e74c3c;"></i>';
            }
        })
        .catch(error => {
            checkbox.checked = !checkbox.checked;
            loader.innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color: #f1c40f;"></i>';
        })
        .finally(() => {
            setTimeout(() => {
                loader.innerHTML = '';
                checkbox.disabled = false;
            }, 800);
        });
    }
});