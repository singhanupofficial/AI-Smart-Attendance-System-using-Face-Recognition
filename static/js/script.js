// Global JS utilities if needed
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 4 seconds
    setTimeout(() => {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 4000);
});