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
    removedImageIds = [];
    const title = button.dataset.postTitle;
    const body = button.dataset.postBody;
    const images = JSON.parse(button.dataset.postImages || "[]");

    const previewContainer = form.querySelector(".image-preview-container");
    console.log(images);

    console.log(title)
    console.log(body)

    // Render images
    renderImagePreviews(previewContainer, images, true);

    // Store the ID of the post being edited
    modal.dataset.postId = postId;
    modal.dataset.title = title;
    modal.dataset.body = body;

    form.querySelector('[name="title"]').value = button.dataset.postTitle;
    form.querySelector('[name="body"]').value = button.dataset.postBody;

    form.action = `/posts/${postId}/update/`;
    console.log(postId);

    form.querySelector("#removed-image-ids").value = JSON.stringify(removedImageIds);

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
 * IMAGES 
   ================= */


let selectedImages = [];
let existingImages = [];
let removedImageIds = [];

const imageInputs = document.getElementsByClassName("image-input");

const formImageState = new Map();

Array.from(imageInputs).forEach(imageInput => {
    const form = imageInput.closest("form");
    const previewContainer = form.querySelector(".image-preview-container");

    const state = {
        selectedImages: [],
        existingImages: [],
        removedImageIds: []
    };

    formImageState.set(form, state);

    imageInput.addEventListener("change", function () {
        const newImages = Array.from(this.files);

        state.selectedImages.push(...newImages);

        renderImagePreviews(
            previewContainer,
            state.selectedImages
        );

        this.value = "";
    });

    form.addEventListener("submit", function () {
        const dataTransfer = new DataTransfer();

        state.selectedImages.forEach(file => {
            dataTransfer.items.add(file);
        });

        imageInput.files = dataTransfer.files;
    });
});

/** Image preview */
function renderImagePreviews(previewContainer, images, isExisting = false) {
    console.log("Rendering image...")
    previewContainer.innerHTML = "";

    images.forEach((image, index) => {
        const wrapper = document.createElement("div");
        wrapper.className = "relative";

        const img = document.createElement("img");
        img.className = "h-32 w-full rounded-lg object-cover";

        const imageURL = isExisting
            ? image
            : URL.createObjectURL(image);

        img.src = imageURL;

        console.log(img);

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.textContent = "×";
        removeButton.className =
            "absolute right-1 top-1 rounded-full bg-white px-2 py-1 shadow";

        removeButton.addEventListener("click", function () {
            if (isExisting) {
                removedImageIds.push(image.id);
                images.splice(index, 1);
            } else {
                URL.revokeObjectURL(imageURL);
                images.splice(index, 1);
            }

            renderImagePreviews(previewContainer, images, isExisting);
        });

        wrapper.appendChild(img);
        wrapper.appendChild(removeButton);
        previewContainer.appendChild(wrapper);
        console.log(wrapper);
        console.log("Image appended");
    });
    console.log("Container:", previewContainer, "Children:", previewContainer.children.length);
}

document.querySelectorAll("form").forEach(postForm => {
    const imageInput = postForm.querySelector(".image-input");

    if (!imageInput) return;

    postForm.addEventListener("submit", function () {
        const dataTransfer = new DataTransfer();

        selectedImages.forEach(file => {
            dataTransfer.items.add(file);
        });

        console.log("Images being submitted:", state.selectedImages);
        console.log("Files attached:", dataTransfer.files.length);

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

/* =================
 * TAGS 
   ================= */

document.querySelectorAll("form").forEach(form => {
    const tags = form.querySelectorAll(".tag-option");
    const selectedTags = form.querySelector(".selected-tags");

    if (!selectedTags || !tags.length) return;

    tags.forEach(button => {
        button.addEventListener("click", () => {
            const selected = button.getAttribute("aria-pressed") === "true";
            const tagId = button.dataset.tagId;

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

            console.log(
                "Selected tag IDs:",
                Array.from(selectedTags.querySelectorAll('input[name="tags"]'))
                    .map(input => input.value)
            );
        });
    });
});

/** Extract dominant image color and apply it to the image container */
document.querySelectorAll('[data-image-color]').forEach(container => {
    const img = container.querySelector('img');

    function extractColor() {
        // Create a small canvas to sample the image
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = 32;
        canvas.height = 32;

        try {
            ctx.drawImage(img, 0, 0, 32, 32);

            const pixels = ctx.getImageData(
                0, 0, 32, 32
            ).data;

            const colors = {};

            // Examine the image pixels
            for (let i = 0; i < pixels.length; i += 4) {
                const r = pixels[i];
                const g = pixels[i + 1];
                const b = pixels[i + 2];

                // Group similar colours together
                const color = [
                    Math.round(r / 32) * 32,
                    Math.round(g / 32) * 32,
                    Math.round(b / 32) * 32
                ].map(value => Math.min(value, 255));

                const key = color.join(',');

                colors[key] = (colors[key] || 0) + 1;
            }

            // Find the most frequently occurring colour
            const dominantColor = Object.entries(colors)
                .sort((a, b) => b[1] - a[1])[0][0];

            container.style.backgroundColor = `rgb(${dominantColor})`;

        } catch (error) {
            console.error('Could not extract image colour:', error);
        }
    }

    // Wait until the image has loaded
    if (img.complete && img.naturalWidth > 0) {
        extractColor();
    } else {
        img.addEventListener('load', extractColor, { once: true });
    }
});