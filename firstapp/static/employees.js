
document.addEventListener('DOMContentLoaded', function() {
    debugger;
    const manualEntryBtn = document.getElementById('manualEntryBtn');
    const manualEntryForm = document.getElementById('manualEntryForm');
    const fileUploadBtn = document.getElementById('fileUploadBtn');
    const fileUploadForm = document.getElementById('fileUploadForm');

    // Hide the fileUploadForm initially
    fileUploadForm.style.display = 'none';

    manualEntryBtn.addEventListener('click', function() {
        debugger;
        manualEntryForm.style.display = 'block';
        fileUploadForm.style.visibility = this.hidden;
    });

    fileUploadBtn.addEventListener('click', function() {
        manualEntryForm.style.display = 'none';
        fileUploadForm.style.visibility = true;
    });
});
