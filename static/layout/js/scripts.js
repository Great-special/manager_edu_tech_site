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

document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.hero-indicator');
    let currentSlide = 0;
    const totalSlides = slides.length;

    function changeSlide(newSlide) {
        slides[currentSlide].classList.remove('active');
        indicators[currentSlide].classList.remove('active');
        
        currentSlide = newSlide;
        
        slides[currentSlide].classList.add('active');
        indicators[currentSlide].classList.add('active');
    }

    function nextSlide() {
        let newSlide = (currentSlide + 1) % totalSlides;
        changeSlide(newSlide);
    }

    // Auto-advance slides every 5 seconds
    setInterval(nextSlide, 5000);

    // Indicator click event
    indicators.forEach(indicator => {
        indicator.addEventListener('click', function() {
            const slideIndex = parseInt(this.getAttribute('data-slide'));
            changeSlide(slideIndex);
        });
    });
});