
// Original code but without closing the Nav Menu on click
// const menu = document.querySelector('#mobile-menu')
// const menuLinks = document.querySelector('.navbar-menu')

// menu.addEventListener('click', function() {
//     menu.classList.toggle ('is-active');
//     menuLinks.classList.toggle ('active');
// });

document.addEventListener('DOMContentLoaded', function() {
    // Selecting the hamburger menu icon
    const menuToggle = document.querySelector('.navbar-toggle');
    
    // Selecting the menu itself
    const navMenu = document.querySelector('.navbar-menu');
    
    // Initial state - menu is not active
    let isMenuActive = false;

    // Toggle menu on hamburger icon click
    menuToggle.addEventListener('click', function() {
        isMenuActive = !isMenuActive;
        navMenu.classList.toggle('active');
    });

    // Close menu when a menu item is clicked
    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(event) {
            if (isMenuActive) {
                isMenuActive = false;
                navMenu.classList.remove('active');
                
                // Prevent default navigation if the link leads nowhere
                if (this.getAttribute('href') === '#') {
                    event.preventDefault();
                }
            }
        });
    });
});