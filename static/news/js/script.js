let navToggle = document.querySelector('.nav-btn');
let navBar = document.querySelector('.navbar');

navToggle.addEventListener('click', function() {
    navBar.classList.toggle('active');
    navToggle.classList.toggle('active');
});

document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImg");

    if (!modal || !modalImg) return;

    document.querySelectorAll(".post-image").forEach(img => {
        img.addEventListener("click", function () {
            modal.style.display = "block";
            modalImg.src = this.src;
        });
    });

    modal.addEventListener("click", function () {
        modal.style.display = "none";
    });

});

document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.like-btn').forEach(function(button) {
                button.addEventListener('click', function() {
                    console.log('Клик по лайку');
                    var url = button.dataset.url;
                    var slug = button.dataset.postSlug;

                    fetch(url, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(res => res.json())
                    .then(data => {
                        button.textContent = data.liked ? 'Убрать лайк' : 'Лайк';
                        document.querySelector(`.like-count[data-post-slug="${slug}"]`).textContent = data.count;
                    })
                    .catch(console.error);
                });
            });
        });

        // Функция для получения csrf из cookie
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                let cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    cookie = cookie.trim();
                    if (cookie.startsWith(name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }