document.addEventListener('DOMContentLoaded', function() {
    const manualEntryBtn = document.getElementById('manualEntryBtn');
    const manualEntryForm = document.getElementById('manualEntryForm');
    const fileUploadBtn = document.getElementById('fileUploadBtn');
    const fileUploadForm = document.getElementById('fileUploadForm');

    manualEntryBtn.addEventListener('click', function() {
        manualEntryForm.style.display = 'block';
        fileUploadForm.style.display = 'none';
    });

    fileUploadBtn.addEventListener('click', function() {
        manualEntryForm.style.display = 'none';
        fileUploadForm.style.display = 'block';
    });
});