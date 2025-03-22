// Custom Cursor Animation
document.addEventListener('mousemove', (e) => {
    const cursor = document.querySelector('.custom-cursor');
    cursor.style.left = `${e.pageX}px`;
    cursor.style.top = `${e.pageY}px`;
});

// Add event listener properly

// dark mode

document.addEventListener('DOMContentLoaded', function () {
    const themeToggleButton = document.getElementById('theme-toggle');
    const body = document.body;

    // Check if dark mode is enabled in localStorage
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    console.log('Initial Dark Mode:', isDarkMode); // Debugging

    // Apply dark mode if enabled
    if (isDarkMode) {
        body.classList.add('dark-mode');
        themeToggleButton.textContent = '☀️ Light Mode';
    } else {
        body.classList.remove('dark-mode');
        themeToggleButton.textContent = '🌙 Dark Mode';
    }

    // Toggle dark mode on button click
    themeToggleButton.addEventListener('click', function () {
        body.classList.toggle('dark-mode');
        const isDarkMode = body.classList.contains('dark-mode');
        console.log('Toggled Dark Mode:', isDarkMode); // Debugging

        // Update button text
        if (isDarkMode) {
            themeToggleButton.textContent = '☀️ Light Mode';
        } else {
            themeToggleButton.textContent = '🌙 Dark Mode';
        }

        // Save preference to localStorage
        localStorage.setItem('darkMode', isDarkMode);
        console.log('Saved Dark Mode:', localStorage.getItem('darkMode')); // Debugging
    });
});