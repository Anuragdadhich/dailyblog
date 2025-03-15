// Custom Cursor Animation
document.addEventListener('mousemove', (e) => {
    const cursor = document.querySelector('.custom-cursor');
    cursor.style.left = `${e.pageX}px`;
    cursor.style.top = `${e.pageY}px`;
});

// Click Animations

document.addEventListener("DOMContentLoaded", function() {
    let sound = document.getElementById("clickSound");

    // Find all buttons and links
    let buttons = document.querySelectorAll(".btn");

    buttons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault(); // Prevent link from opening instantly
            sound.currentTime = 0; // Reset sound for fast clicking
            sound.play();

            // Delay navigation for links
            if (this.tagName === "A") {
                let url = this.href;
                setTimeout(() => { window.location.href = url; }, 300); // 300ms delay
            }
        });
    });
});

    // Sidebar Toggle for Mobile
  