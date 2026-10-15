const endTime = document.querySelector(".end-time");
const endDate = document.querySelector(".end-date");

function showEndDate() {
    if (endTime.clicked == true) {
        endTime.hidden = false;
        endDate.hidden = false;
    } else {
        endTime.hidden = true;
        endDate.hidden = true;
    }
};