// TheBitverse JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add some simple ASCII animations to the landing page
    const asciiArt = document.createElement('div');
    asciiArt.classList.add('ascii-art');
    
    const artFrames = [
        `
 ╔══════════════════════════╗
 ║  ▄▄▄▄▄ ▄ ▄    ▄▄▄  ▄ ▄   ║
 ║  █ █ █ █▀█    █▄█  █ █   ║
 ║  █   █ █ █    █    █▄█   ║
 ║                          ║
 ║      ♫  TheBitverse  ♪   ║
 ║                          ║
 ╚══════════════════════════╝
        `,
        `
 ╔══════════════════════════╗
 ║  ▄▄▄▄▄ ▄▄▄    ▄▄▄  ▄▄▄   ║
 ║  █ █ █ █▄█    █▄█  █▄█   ║
 ║  █   █ █ █    █    █ █   ║
 ║                          ║
 ║      ♪  TheBitverse  ♫   ║
 ║                          ║
 ╚══════════════════════════╝
        `
    ];
    
    // Insert ASCII art after the header
    const header = document.querySelector('header');
    header.after(asciiArt);
    
    // Animate ASCII art
    let currentFrame = 0;
    setInterval(() => {
        asciiArt.textContent = artFrames[currentFrame];
        currentFrame = (currentFrame + 1) % artFrames.length;
    }, 1000);
    
    // Add click event to launch button
    const launchBtn = document.querySelector('.btn');
    launchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Show an alert indicating this would normally launch the Python app
        alert("This button would normally launch the Python application.\n\nSince web browsers can't directly run Python files, please run the application by executing the Python script directly.");
    });
    
    // Add hover effects for feature cards
    const features = document.querySelectorAll('.feature');
    features.forEach(feature => {
        feature.addEventListener('mouseover', function() {
            this.style.borderColor = getRandomColor();
        });
        
        feature.addEventListener('mouseout', function() {
            this.style.borderColor = '#00ffff';
        });
    });
    
    // Random color generator for hover effects
    function getRandomColor() {
        const colors = ['#00ff00', '#ff00ff', '#00ffff', '#ffff00', '#ff0000'];
        return colors[Math.floor(Math.random() * colors.length)];
    }
});