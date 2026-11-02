/* =========================
*  FORM DATE AND TIME LOGIC
   ========================= */

const endTimeSwitch = document.getElementById("add-end-time");
const endTime = document.querySelector(".end-time");
const endDate = document.querySelector(".end-date");

endTimeSwitch.addEventListener("change", () => {
    showEndDate();
});

/** Show end date and time */
function showEndDate() {
    const end_time = document.getElementById("end_time");
    const end_date = document.getElementById("end_date");

    if (endTime.hidden == true) {
        // Unhide fields
        endTime.hidden = false
        endDate.hidden = false;

        // Make fields required
        end_time.required = true
        end_date.required = true;

    } else {
        endTime.hidden = true
        endDate.hidden = true;

        endTime.required = false
        endDate.required = false;
    }
};

// function getDefaultEndDateTime(startDate, startTime) {
//     if (!startDate || !startTime) return null;

//     const start = new Date(`${startDate}T${startTime}`);

//     if (Number.isNaN(start.getTime())) return null;

//     const end = new Date(start.getTime() + 60 * 60 * 1000);

//     const year = end.getFullYear();
//     const month = String(end.getMonth() + 1).padStart(2, "0");
//     const day = String(end.getDate()).padStart(2, "0");
//     const hours = String(end.getHours()).padStart(2, "0");
//     const minutes = String(end.getMinutes()).padStart(2, "0");

//     return {
//         date: `${year}-${month}-${day}`,
//         time: `${hours}:${minutes}`
//     };
// }


/* =========================
*  EVENT IMAGE PREVIEW
   ========================= */

/** Preview event image */
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

