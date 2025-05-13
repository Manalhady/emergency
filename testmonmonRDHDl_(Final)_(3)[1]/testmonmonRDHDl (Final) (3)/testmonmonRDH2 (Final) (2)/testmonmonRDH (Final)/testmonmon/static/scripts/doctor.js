// doctor-profile.js

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // 1. Tab Switching Enhancement
    const tabs = document.querySelectorAll('.list-group-item-action');
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();

            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));

            // Add active class to clicked tab
            this.classList.add('active');

            // Hide all tab panes
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('show', 'active');
            });

            // Show the target pane
            const targetPane = document.querySelector(this.getAttribute('href'));
            targetPane.classList.add('show', 'active');
        });
    });

    // 2. Patient List Search Functionality
    const patientSearch = document.getElementById('patient-search');
    if (patientSearch) {
        patientSearch.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('#account-ptlist tbody tr').forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // 3. Responsive Behavior
    function checkScreenSize() {
        const sidebar = document.querySelector('.col-md-3');
        if (sidebar) {
            if (window.innerWidth < 768) {
                sidebar.classList.add('mb-3');
            } else {
                sidebar.classList.remove('mb-3');
            }
        }
    }

    window.addEventListener('resize', checkScreenSize);
    checkScreenSize();

    // 4. Confirmation Dialogs for Actions
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to perform this action?')) {
                e.preventDefault();
            }
        });
    });

    // 5. Sortable Patient Table
    const table = document.querySelector('table');
    if (table) {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                sortTable(index);
            });
        });
    }

    // function sortTable(columnIndex) {
    //     // Implementation for sorting table columns
    //     console.log(`Sorting by column ${columnIndex}`);
    //     // You would implement actual sorting logic here
    // }
});