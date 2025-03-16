// Custom Cursor Animation
document.addEventListener('mousemove', (e) => {
    const cursor = document.querySelector('.custom-cursor');
    cursor.style.left = `${e.pageX}px`;
    cursor.style.top = `${e.pageY}px`;
});

function validateSearch(event) {
    const input = document.getElementById('searchInput');
    if (input.value.trim().length < 2) {
        alert('Please enter at least 2 characters for search');
        event.preventDefault(); // Prevent form submission
        return false;
    }
    // Play click sound if needed
    const clickSound = document.getElementById('clickSound');
    clickSound.play();
    return true; // Allow form submission
}

// Add event listener properly
document.getElementById('searchForm').addEventListener('submit', validateSearch);

// Sidebar toggle functionality
document.getElementById('sidebarToggle').addEventListener('click', function() {
    const sidebarContent = document.getElementById('sidebarContent');
    sidebarContent.classList.toggle('show');
});