const endTimeSwitch = document.getElementById("add-end-time");
const endTime = document.querySelector(".end-time");
const endDate = document.querySelector(".end-date");

/** Add end time switch */
endTimeSwitch.addEventListener("change", () => {
    console.log("End time flipped");
    showEndDate();
});

function showEndDate() {
    const end_time = document.getElementById("end_time");
    const end_date = document.getElementById("end_date");

    if (endTime.hidden == true) {
        endTime.hidden = false
        endDate.hidden = false;

        end_time.required = true
        end_date.required = true;

    } else {
        endTime.hidden = true
        endDate.hidden = true;

        endTime.required = false
        endDate.required = false;
    }
};

/** Cover photo preview */
const eventImage = document.querySelector(".event-input");
const eventPreviewContainer = document.getElementById("event-preview-container")

eventImage.addEventListener("change", function () {
    eventPreviewContainer.innerHTML = "";

    const file = this.files[0];

    if (file) {
        console.log("File exists")
        const img = document.createElement("img");
        img.className = "h-96 w-sm rounded-lg object-fit";

        const imageURL = URL.createObjectURL(file);
        img.src = imageURL;

        eventPreviewContainer.appendChild(img);
    }    
});

