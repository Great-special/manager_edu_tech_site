/* ======================
   PRIVACY POLICY PAGE JAVASCRIPT
   ====================== */

document.addEventListener('DOMContentLoaded', function() {
    
    // ======================
    // Language Toggle
    // ======================
    const langButtons = document.querySelectorAll('.lang-btn');
    const languageContents = document.querySelectorAll('.language-content');
    
    langButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetLang = this.getAttribute('data-lang');
            
            // Update active button
            langButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding content
            languageContents.forEach(content => {
                if (content.getAttribute('data-lang-content') === targetLang) {
                    content.classList.remove('hidden');
                } else {
                    content.classList.add('hidden');
                }
            });
            
            // Save preference to localStorage
            localStorage.setItem('preferredLang', targetLang);
        });
    });
    
    // Load saved language preference
    const savedLang = localStorage.getItem('preferredLang');
    if (savedLang) {
        const savedLangBtn = document.querySelector(`.lang-btn[data-lang="${savedLang}"]`);
        if (savedLangBtn) {
            savedLangBtn.click();
        }
    }
    
    // ======================
    // Table of Contents Navigation
    // ======================
    const tocLinks = document.querySelectorAll('.toc-link');
    const sections = document.querySelectorAll('.privacy-section');
    
    // Smooth scroll to section
    tocLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerOffset = 100;
                const elementPosition = targetSection.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Highlight active section in TOC
    function highlightActiveSection() {
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.pageYOffset >= (sectionTop - 150)) {
                currentSection = section.getAttribute('id');
            }
        });
        
        tocLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }
    
    // Throttle function for scroll performance
    function throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    window.addEventListener('scroll', throttle(highlightActiveSection, 100));
    
    // ======================
    // Back to Top Button
    // ======================
    const backToTopButton = document.getElementById('backToTop');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });
        
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ======================
    // Copy Email/Phone on Click
    // ======================
    const contactLinks = document.querySelectorAll('.contact-method a, .info-card a');
    
    contactLinks.forEach(link => {
        if (link.href.startsWith('mailto:') || link.href.startsWith('tel:')) {
            link.addEventListener('click', function(e) {
                // Allow default action but show copied notification
                const text = link.textContent.trim();
                
                // Create temporary notification
                const notification = document.createElement('div');
                notification.textContent = `Copied: ${text}`;
                notification.style.cssText = `
                    position: fixed;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: #4CAF50;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 5px;
                    z-index: 10000;
                    font-size: 14px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                `;
                
                document.body.appendChild(notification);
                
                // Copy to clipboard
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(text).then(() => {
                        // Show notification
                        setTimeout(() => {
                            notification.style.opacity = '1';
                        }, 10);
                        
                        // Hide and remove notification
                        setTimeout(() => {
                            notification.style.opacity = '0';
                            setTimeout(() => {
                                document.body.removeChild(notification);
                            }, 300);
                        }, 2000);
                    });
                }
            });
        }
    });
    
    // ======================
    // Print Button (Optional)
    // ======================
    const printButton = document.getElementById('printPolicy');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // ======================
    // Expand/Collapse Sections (Mobile)
    // ======================
    if (window.innerWidth <= 767) {
        const sectionHeaders = document.querySelectorAll('.section-header');
        
        sectionHeaders.forEach(header => {
            header.style.cursor = 'pointer';
            
            header.addEventListener('click', function() {
                const content = this.nextElementSibling;
                if (content && content.classList.contains('section-content')) {
                    content.classList.toggle('collapsed');
                    
                    if (content.style.maxHeight) {
                        content.style.maxHeight = null;
                    } else {
                        content.style.maxHeight = content.scrollHeight + 'px';
                    }
                }
            });
        });
    }
    
    // ======================
    // Reading Progress Bar (Optional)
    // ======================
    function createProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.id = 'readingProgress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
            z-index: 9999;
            transition: width 0.1s ease;
        `;
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', function() {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBar.style.width = scrolled + '%';
        });
    }
    
    // Uncomment to enable reading progress bar
    // createProgressBar();
    
    // ======================
    // Anchor Links from External Pages
    // ======================
    function scrollToAnchor() {
        const hash = window.location.hash;
        if (hash) {
            setTimeout(() => {
                const element = document.querySelector(hash);
                if (element) {
                    const headerOffset = 100;
                    const elementPosition = element.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }, 100);
        }
    }
    
    scrollToAnchor();
    
    // Handle hash changes (for single page apps)
    window.addEventListener('hashchange', scrollToAnchor);
    
});

// ======================
// Helper Functions
// ======================

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Animate elements on scroll (optional enhancement)
function animateOnScroll() {
    const animatedElements = document.querySelectorAll('.privacy-section');
    
    animatedElements.forEach(element => {
        if (isInViewport(element)) {
            element.classList.add('animated');
        }
    });
}

// Uncomment to enable scroll animations
// window.addEventListener('scroll', throttle(animateOnScroll, 200));
