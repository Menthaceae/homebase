const dialog = document.getElementById("post-to-modal");
const post_to_btns = document.querySelectorAll(".post-to-option");


/* ===================
 * MODAL FORM HANDLING 
   =================== */

/** Reusable close form button */
dialog.addEventListener("click", function (event) {
    const more_options = document.getElementById("more-options");
    if (event.target === dialog) {
        dialog.close();
        more_options.hidden = true;
    }
});

/** Post to logic */

function openPostTo() {
    const button = document.getElementById("post-to-button");

    const rect = button.getBoundingClientRect();

    dialog.style.position = "fixed";
    dialog.style.left = `${rect.left - 80}px`;
    dialog.style.top = `${rect.bottom + 115}px`;
    dialog.style.margin = "0";

    dialog.showModal();
}

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

/** Show more options (sell, create event) */
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

/** Open Post Update Modal and send unique post id */
function openUpdatePostModal(button) {
    const modal = document.getElementById("update-post-modal");
    const form = modal.querySelector(".update-post-form");
    const postId = button.dataset.postId;
    const title = button.dataset.postTitle;
    const body = button.dataset.postBody;

    console.log(title)
    console.log(body)

    // Store the ID of the post being edited
    modal.dataset.postId = postId;
    modal.dataset.title = title;
    modal.dataset.body = body;

    form.querySelector('[name="title"]').value = button.dataset.postTitle;
    form.querySelector('[name="body"]').value = button.dataset.postBody;

    form.action = `/posts/${postId}/update/`;
    console.log(postId);

    modal.showModal();
}

function deletePost(button) {
    const postId = button.dataset.postId;
    const form = document.createElement("form");
    form.method = "POST";
    form.action = `/posts/${postId}/delete/`;

    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfToken;

    form.appendChild(csrfInput);
    document.body.appendChild(form);

    form.submit();
}

/* =================
 * TAGS 
   ================= */

const tags = document.querySelectorAll(".tag-option");

tags.forEach((button) => {
    button.addEventListener("click", () => {
        const selected = button.getAttribute("aria-pressed") === "true";
        const tagId = button.dataset.tagId;
        const selectedTags = document.getElementById("selected-tags");

        button.setAttribute("aria-pressed", String(!selected));

        if (!selected) {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "tags";
            input.value = tagId;
            input.dataset.tagId = tagId;

            selectedTags.appendChild(input);
        } else {
            selectedTags
                .querySelector(`input[data-tag-id="${tagId}"]`)
                ?.remove();
        }
    });
});

/* =================
 * IMAGES 
   ================= */

const imageInputs = document.getElementsByClassName("image-input");
const previewContainer = document.getElementById("image-preview-container");

let selectedImages = [];

Array.from(imageInputs).forEach(imageInput => {
    imageInput.addEventListener("change", function () {
        const newImages = Array.from(this.files);

        selectedImages.push(...newImages);
        console.log("Added photo")
        renderImagePreviews();

        // Clear the input so the same file can be selected again
        this.value = "";
    });
});

function renderImagePreviews() {
    console.log("Rendering image...")
    previewContainer.innerHTML = "";

    selectedImages.forEach((file, index) => {
        const wrapper = document.createElement("div");
        wrapper.className = "relative";

        const img = document.createElement("img");
        img.className = "h-32 w-full rounded-lg object-cover";

        const imageURL = URL.createObjectURL(file);
        img.src = imageURL;

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.textContent = "×";
        removeButton.className =
            "absolute right-1 top-1 rounded-full bg-white px-2 py-1 shadow";

        removeButton.addEventListener("click", function () {
            URL.revokeObjectURL(imageURL);
            selectedImages.splice(index, 1);
            renderImagePreviews();
        });

        wrapper.appendChild(img);
        wrapper.appendChild(removeButton);
        previewContainer.appendChild(wrapper);
        console.log("Image appended");
    });
}

document.querySelectorAll("form").forEach(postForm => {
    const imageInput = postForm.querySelector(".image-input");

    if (!imageInput) return;

    postForm.addEventListener("submit", function () {
        const dataTransfer = new DataTransfer();

        selectedImages.forEach(file => {
            dataTransfer.items.add(file);
        });

        imageInput.files = dataTransfer.files;
    });
});

/** Image Carousel */
const images = document.querySelectorAll("[data-carousel-item]");

images.forEach((img) => {
    img.addEventListener("click", () => {
        images.forEach((item) => {
            item.setAttribute("aria-current", "false");
        });

        img.setAttribute("aria-current", "true");
    });
});