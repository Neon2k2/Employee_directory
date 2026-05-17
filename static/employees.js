document.addEventListener("DOMContentLoaded", function () {

  // =========================
  // SEARCH FUNCTIONALITY
  // =========================

  const searchInput = document.getElementById("searchInput");
  const resetSearch = document.getElementById("resetSearch");
  const searchForm = document.getElementById("searchForm");

  // Focus search input safely
  if (searchInput) {
    searchInput.focus();
  }

  // Handle search form submit
  if (searchForm) {
    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();

      // Submit form manually if needed
      searchForm.submit();

      if (searchInput) {
        searchInput.focus();
      }
    });
  }

  // Reset search safely
  if (resetSearch && searchInput && searchForm) {
    resetSearch.addEventListener("click", function (event) {
      event.preventDefault();

      searchInput.value = '';
      searchForm.submit();

      searchInput.focus();
    });
  }


  // =========================
  // FILE UPLOAD TOGGLE
  // =========================

  const fileUploadBtn = document.getElementById('fileUploadBtn');
  const fileUploadForm = document.getElementById('fileUploadForm');

  // Hide upload form initially
  if (fileUploadForm) {
    fileUploadForm.style.display = 'none';
  }

  // Show upload form on button click
  if (fileUploadBtn && fileUploadForm) {
    fileUploadBtn.addEventListener('click', function () {
      fileUploadForm.style.display = 'block';
    });
  }

});


// =========================
// GLOBAL CHANGES ARRAY
// =========================

var changes = [];


// =========================
// TOGGLE EDIT MODE
// =========================

function toggleEditMode() {

  var tableRows = document.getElementsByTagName('tr');
  var editToggle = document.getElementById('edit-toggle');
  var tableHead = document.getElementById('tableHead');

  if (!editToggle) {
    return;
  }

  // =========================
  // SWITCH TO EDIT MODE
  // =========================

  if (editToggle.innerHTML === 'View Mode') {

    if (tableHead) {
      tableHead.style.backgroundColor = 'grey';
    }

    editToggle.innerHTML = 'Edit Mode';

    for (var i = 0; i < tableRows.length; i++) {

      var cells = tableRows[i].getElementsByTagName('td');

      for (var j = 0; j < cells.length; j++) {
        cells[j].setAttribute('contenteditable', 'true');
      }
    }

  }

  // =========================
  // SWITCH TO VIEW MODE
  // =========================

  else {

    editToggle.innerHTML = 'View Mode';

    if (tableHead) {
      tableHead.style.backgroundColor = '#0D4C92';
    }

    for (var i = 0; i < tableRows.length; i++) {

      var cells = tableRows[i].getElementsByTagName('td');

      for (var j = 0; j < cells.length; j++) {
        cells[j].setAttribute('contenteditable', 'false');
      }
    }

    saveChanges();
  }


  // =========================
  // TRACK CELL CHANGES
  // =========================

  var editableCells = document.querySelectorAll('td[contenteditable="true"]');

  editableCells.forEach(function (cell) {

    cell.addEventListener('input', function (event) {

      var element = event.target;
      var row = element.closest('tr');

      if (!row) return;

      var employeeId = row.dataset.employeeId;
      var fieldName = element.dataset.fieldName;
      var fieldValue = element.innerText.trim();

      if (!employeeId || !fieldName) return;

      // Check if change already exists
      var existingChangeIndex = changes.findIndex(function (change) {
        return (
          change.employee_id === employeeId &&
          change.field_name === fieldName
        );
      });

      if (existingChangeIndex > -1) {

        // Update existing change
        changes[existingChangeIndex].field_value = fieldValue;

      } else {

        // Add new change
        changes.push({
          employee_id: employeeId,
          field_name: fieldName,
          field_value: fieldValue
        });
      }

    });

  });

}


// =========================
// SAVE CHANGES
// =========================

function saveChanges() {

  if (changes.length === 0) {
    return;
  }

  var csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');

  if (!csrfElement) {
    console.error('CSRF token not found.');
    return;
  }

  var csrftoken = csrfElement.value;

  var xhr = new XMLHttpRequest();

  xhr.open('PATCH', '/update/', true);

  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.setRequestHeader('X-CSRFToken', csrftoken);

  xhr.onload = function () {

    if (xhr.status === 200) {

      console.log('Changes saved successfully.');

    } else {

      console.error('Error saving changes.');

    }

  };

  xhr.send(JSON.stringify(changes));

}


// =========================
// GLOBAL INPUT TRACKER
// =========================

document.addEventListener('input', function (event) {

  var element = event.target;

  if (element.getAttribute('contenteditable') !== 'true') {
    return;
  }

  var row = element.closest('tr');

  if (!row) {
    return;
  }

  var employeeId = row.dataset.employeeId;
  var fieldName = element.dataset.fieldName;
  var fieldValue = element.innerText.trim();

  if (!employeeId || !fieldName) {
    return;
  }

  // Check if change already exists
  var existingChangeIndex = changes.findIndex(function (change) {
    return (
      change.employee_id === employeeId &&
      change.field_name === fieldName
    );
  });

  if (existingChangeIndex > -1) {

    changes[existingChangeIndex].field_value = fieldValue;

  } else {

    changes.push({
      employee_id: employeeId,
      field_name: fieldName,
      field_value: fieldValue
    });

  }

});
