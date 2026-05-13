/* ======================
   IMPRINT PAGE JAVASCRIPT
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
    // Copy Contact Information on Click
    // ======================
    const contactLinks = document.querySelectorAll('.contact-link');
    
    contactLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // For mailto: and tel: links, also copy to clipboard
            if (this.href.startsWith('mailto:') || this.href.startsWith('tel:')) {
                const text = this.textContent.trim();
                
                // Copy to clipboard
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(text).then(() => {
                        showCopyNotification(text);
                    }).catch(err => {
                        console.error('Copy failed:', err);
                    });
                }
            }
        });
    });
    
    // ======================
    // Show Copy Notification
    // ======================
    function showCopyNotification(text) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'copy-notification';
        notification.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>Copied: ${text}</span>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            bottom: ${window.innerWidth <= 767 ? '80px' : '30px'};
            right: ${window.innerWidth <= 767 ? '20px' : '30px'};
            background: #4CAF50;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            z-index: 10000;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            gap: 10px;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        }, 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(20px)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // ======================
    // Smooth Scroll for Internal Links
    // ======================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 100;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ======================
    // Print Page Function
    // ======================
    const printButton = document.getElementById('printImprint');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // ======================
    // Animate Sections on Scroll (Optional)
    // ======================
    function animateOnScroll() {
        const sections = document.querySelectorAll('.imprint-section');
        
        sections.forEach(section => {
            const sectionTop = section.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (sectionTop < windowHeight * 0.85) {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Initialize sections with starting animation state
    document.querySelectorAll('.imprint-section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // Run animation on load and scroll
    animateOnScroll();
    window.addEventListener('scroll', throttle(animateOnScroll, 100));
    
    // ======================
    // Throttle Function for Performance
    // ======================
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
    
    // ======================
    // Add External Link Icons
    // ======================
    document.querySelectorAll('a[target="_blank"]').forEach(link => {
        if (!link.querySelector('i')) {
            const icon = document.createElement('i');
            icon.className = 'fas fa-external-link-alt';
            icon.style.marginLeft = '5px';
            icon.style.fontSize = '0.8em';
            link.appendChild(icon);
        }
    });
    
    // ======================
    // Click to Call Analytics (Optional)
    // ======================
    document.querySelectorAll('a[href^="tel:"]').forEach(link => {
        link.addEventListener('click', function() {
            console.log('Phone call initiated:', this.href);
            // Add analytics tracking here if needed
            // e.g., gtag('event', 'phone_call', { phone_number: this.href });
        });
    });
    
    document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
        link.addEventListener('click', function() {
            console.log('Email link clicked:', this.href);
            // Add analytics tracking here if needed
            // e.g., gtag('event', 'email_click', { email: this.href });
        });
    });
    
    // ======================
    // Detect and Warn about Ad Blockers (Optional)
    // ======================
    function checkAdBlocker() {
        // This is a basic check - you can enhance it
        const testAd = document.createElement('div');
        testAd.innerHTML = '&nbsp;';
        testAd.className = 'adsbox';
        testAd.style.position = 'absolute';
        testAd.style.top = '-1px';
        testAd.style.left = '-1px';
        document.body.appendChild(testAd);
        
        setTimeout(() => {
            if (testAd.offsetHeight === 0) {
                console.log('Ad blocker detected');
                // Handle ad blocker detection if needed
            }
            document.body.removeChild(testAd);
        }, 100);
    }
    
    // Uncomment if you need ad blocker detection
    // checkAdBlocker();
    
});

// ======================
// Helper Functions
// ======================

// Format phone numbers (optional enhancement)
function formatPhoneNumber(phoneNumber) {
    // Remove all non-numeric characters
    const cleaned = phoneNumber.replace(/\D/g, '');
    
    // Format: +49 173 936 2898
    if (cleaned.startsWith('49')) {
        const match = cleaned.match(/^(\d{2})(\d{3})(\d{3})(\d{4})$/);
        if (match) {
            return `+${match[1]} ${match[2]} ${match[3]} ${match[4]}`;
        }
    }
    
    return phoneNumber;
}

// Validate email format (optional enhancement)
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Export functions if needed in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatPhoneNumber,
        isValidEmail
    };
}
