const endTime = document.querySelector(".endTime");
const endDate = document.querySelector(".endDate");

function showEndDate() {
    if (endTime.hidden == true) {
        endTime.hidden = false;
        endDate.hidden = false;
    } else {
        endTime.hidden = true;
        endDate.hidden = true;
    }
}