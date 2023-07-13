

document.addEventListener('DOMContentLoaded', function () {

    const fileUploadBtn = document.getElementById('fileUploadBtn');
    const fileUploadForm = document.getElementById('fileUploadForm');

    // Hide the fileUploadForm initially
    fileUploadForm.style.display = 'none';
    fileUploadBtn.addEventListener('click', function () {
      fileUploadForm.style.display = 'block';

    });
  });

function toggleEditMode() {
    var tableRows = document.getElementsByTagName('tr');
    var editToggle = document.getElementById('edit-toggle');
    if (editToggle.innerHTML === 'Toggle Edit Mode') {
      editToggle.innerHTML = 'Toggle View Mode';
      for (var i = 0; i < tableRows.length; i++) {
        var cells = tableRows[i].getElementsByTagName('td');
        for (var j = 0; j < cells.length; j++) {
          cells[j].setAttribute('contenteditable', 'true');
        }
      }
    } else {
      editToggle.innerHTML = 'Toggle Edit Mode';
      for (var i = 0; i < tableRows.length; i++) {
        var cells = tableRows[i].getElementsByTagName('td');
        for (var j = 0; j < cells.length; j++) {
          cells[j].setAttribute('contenteditable', 'false');
        }
      }
    }
  }

  var changes = []; // Global array to store changes

  function toggleEditMode() {
    var tableRows = document.getElementsByTagName('tr');
    var editToggle = document.getElementById('edit-toggle');
    if (editToggle.innerHTML === 'Toggle Edit Mode') {
      editToggle.innerHTML = 'Toggle View Mode';
      for (var i = 0; i < tableRows.length; i++) {
        var cells = tableRows[i].getElementsByTagName('td');
        for (var j = 0; j < cells.length; j++) {
          cells[j].setAttribute('contenteditable', 'true');
        }
      }
    } else {
      editToggle.innerHTML = 'Toggle Edit Mode';
      for (var i = 0; i < tableRows.length; i++) {
        var cells = tableRows[i].getElementsByTagName('td');
        for (var j = 0; j < cells.length; j++) {
          cells[j].setAttribute('contenteditable', 'false');
        }
      }
      saveChanges();
    }

    var cells = document.querySelectorAll('td[contenteditable="true"]');
    cells.forEach(function (cell) {
      cell.addEventListener('input', function (event) {
        var element = event.target;
        var row = element.closest('tr');
        var employeeId = row.dataset.employeeId;
        var fieldName = element.dataset.fieldName;
        var fieldValue = element.innerText.trim();

        // Find if the change already exists in the array
        var existingChangeIndex = changes.findIndex(function (change) {
          return change.employee_id === employeeId && change.field_name === fieldName;
        });

        if (existingChangeIndex > -1) {
          // Update the existing change
          changes[existingChangeIndex].field_value = fieldValue;
        } else {
          // Add a new change to the array
          changes.push({
            employee_id: employeeId,
            field_name: fieldName,
            field_value: fieldValue
          });
          
        }
      });
    });
  }

  function saveChanges() {
    if (changes.length > 0) {
      var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      var xhr = new XMLHttpRequest();
      xhr.open('PATCH', '/update/', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
      xhr.onload = function() {
        if (xhr.status === 200) {
          console.log('Changes saved successfully.');
        } else {
          console.error('Error saving changes.');
        }
      };
      xhr.send(JSON.stringify(changes));
    }
  }

  document.addEventListener('input', function (event) {
    var element = event.target;
    if (element.getAttribute('contenteditable') === 'true') {
      var row = element.closest('tr');
      var employeeId = row.dataset.employeeId;
      var fieldName = element.dataset.fieldName;
      var fieldValue = element.innerText.trim();

      // Find if the change already exists in the array
      var existingChangeIndex = changes.findIndex(function (change) {
        return change.employee_id === employeeId && change.field_name === fieldName;
      });

      if (existingChangeIndex > -1) {
        // Update the existing change
        changes[existingChangeIndex].field_value = fieldValue;
      } else {
        // Add a new change to the array
        changes.push({
          employee_id: employeeId,
          field_name: fieldName,
          field_value: fieldValue
        });
      }
    }
  });