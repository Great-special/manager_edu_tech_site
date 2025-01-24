// document.addEventListener('DOMContentLoaded', function() {
//     const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
//     const navLinks = document.querySelector('.nav-links');

//     // Check if elements exist before adding event listeners
//     if (mobileMenuToggle && navLinks) {
//         mobileMenuToggle.addEventListener('click', function() {
//             navLinks.classList.toggle('active');
//         });
//     }
// });

// document.querySelector('.mobile-toggle').addEventListener('click', function() {
//     document.querySelector('.category-nav').classList.toggle('active');
// });


document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    mobileMenuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        this.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.main-nav')) {
            navLinks.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
        }
    });
});