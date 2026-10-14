const dialog = document.getElementById("post-to-modal");
const post_to_btns = document.querySelectorAll(".post-to-option");

// Close modal
dialog.addEventListener("click", function (event) {
    const more_options = document.getElementById("more-options");
    if (event.target === dialog) {
        dialog.close();
        more_options.hidden = true;
    }
});

// Open modal to select which feed to post to
function openPostTo() {
    const button = document.getElementById("post-to-button");

    const rect = button.getBoundingClientRect();

    dialog.style.position = "fixed";
    dialog.style.left = `${rect.left - 80}px`;
    dialog.style.top = `${rect.bottom + 115}px`;
    dialog.style.margin = "0";

    dialog.showModal();
}

// Sends selection to form
function selectPostDestination(value) {
    document.getElementById("post_to").value = value;
    document.getElementById("post-to-modal");
}

Array.from(post_to_btns).forEach(btn => {
    btn.addEventListener("click", function() {
        // Hide all checks
        post_to_btns.forEach(btn => {
            btn.querySelector(".selected").hidden = true;
        });

        // Show the selected button's check
        btn.querySelector(".selected").hidden = false;    
    });
});

// Show more options (sell, create event)
function moreOptions() {
    const more_options = document.getElementById("more-options");

    if (more_options.hidden == true) {
        more_options.hidden = false;
    } else {
        more_options.hidden = true;
    }
    
}

function openEventModal() {
    const postModal = document.getElementById('create-post-modal');
    const eventModal = document.getElementById('create-post-modal');

    if (postModal.open) {
        print("Closing post modal");
        postModal.close();
    }

    if (eventModal && !eventModal.open) {
        print("Opening event modal");
        eventModal.showModal();
    }

}