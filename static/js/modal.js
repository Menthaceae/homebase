/* ===============================
*   Reusable logic for modal forms
   =============================== */

/** Close modal when clicking outside of dialog */
function closeOnOutsideClick(dialog) {
    dialog.addEventListener("click", function(event) {
        if (event.target === dialog) {
            dialog.close();
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const dialogs = document.querySelectorAll("dialog");

    dialogs.forEach(dialog => {
        closeOnOutsideClick(dialog);
    });
});