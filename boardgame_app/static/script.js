<!-- Include the existing HTML and CSS above this line -->

<!-- JavaScript Section -->
<script>
    // Simulated data for café listings
    const cafeData = [
        { id: 'cafe1', name: 'Café 1' },
        { id: 'cafe2', name: 'Café 2' },
        // Add more café data as needed
    ];

    // Show/hide sections based on navigation
    const showSection = (sectionId) => {
        const sections = ['home', 'cafes', 'reserve', 'profile'];
        sections.forEach(section => {
            const element = document.getElementById(section);
            element.style.display = section === sectionId ? 'block' : 'none';
        });
    };

    // Handle form submission
    const handleFormSubmit = (event) => {
        event.preventDefault();

        // Get form data
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const cafe = document.getElementById('cafe').value;

        // Simulate data submission (you can replace this with actual AJAX requests)
        console.log(`Reservation Details: Date - ${date}, Time - ${time}, Café - ${cafe}`);
    };

    // Add event listeners for navigation links
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const sectionId = event.target.getAttribute('href').substring(1);
            showSection(sectionId);
        });
    });

    // Add event listener for form submission
    document.getElementById('reservationForm').addEventListener('submit', handleFormSubmit);
document.addEventListener('DOMContentLoaded', function () {
    const currentPage = window.location.pathname.split('/').pop(); // Get the current page filename

    // Highlight the active link in the navigation
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href').split('/').pop();
        if (linkPage === currentPage) {
            link.classList.add('active');
        }
    });
});
</script>

</body>

</html>
