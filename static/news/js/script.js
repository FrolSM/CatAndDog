let navToggle = document.querySelector('.nav-btn');
let navBar = document.querySelector('.navbar');

navToggle.addEventListener('click', function() {
    navBar.classList.toggle('active');
    navToggle.classList.toggle('active');
});