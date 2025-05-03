let uploadedImageData = null;

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        uploadedImageData = e.target.result;
        const imgElement = document.getElementById('uploaded-image');
        imgElement.src = uploadedImageData;
        imgElement.style.display = 'block';

        // Hide the upload box when image is displayed
        const uploadBox = document.getElementById('upload-box');
        if (uploadBox) {
            uploadBox.style.display = 'none';
        }
    };
    reader.readAsDataURL(file);
}

function applyEdits(edits) {
    if (!uploadedImageData) {
        showToast("Please upload an image first.");
        return;
    }

    fetch('/edit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ image: uploadedImageData, edits: edits })
    })
    .then(response => response.json())
    .then(data => {
        if (data.edited_image) {
            const imgElement = document.getElementById('uploaded-image');
            imgElement.src = data.edited_image;
        } else if (data.error) {
            showToast("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error(error);
        showToast("An error occurred while editing the image.");
    });
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function adjust_brightness() {
    const val = parseFloat(document.getElementById('brightness-slider').value);
    applyEdits({ brightness: val });
}

function adjust_exposure() {
    const val = parseFloat(document.getElementById('exposure-slider').value);
    applyEdits({ exposure: val });
}

function adjust_contrast() {
    const val = parseFloat(document.getElementById('contrast-slider').value);
    applyEdits({ contrast: val });
}

function adjust_highlights() {
    const val = parseFloat(document.getElementById('highlights-slider').value);
    applyEdits({ highlights: val });
}

function adjust_hue() {
    const val = parseInt(document.getElementById('hue-slider').value);
    applyEdits({ hue: val });
}

function adjust_saturation() {
    const val = parseFloat(document.getElementById('saturation-slider').value);
    applyEdits({ saturation: val });
}

function adjust_luminance() {
    const val = parseFloat(document.getElementById('luminance-slider').value);
    applyEdits({ luminance: val });
}

function apply_color_grading() {
    const val = parseFloat(document.getElementById('color-grading-slider').value);
    applyEdits({ color_grading: val });
}

function apply_blur() {
    const val = parseInt(document.getElementById('blur-slider').value);
    applyEdits({ blur: val });
}

function noise_reduction() {
    const val = parseInt(document.getElementById('noise-reduction-slider').value);
    applyEdits({ noise_reduction: val });
}

function smoothness() {
    const val = parseInt(document.getElementById('smoothness-slider').value);
    applyEdits({ smoothness: val });
}

// Effect Tools
document.querySelector('.Grayscale')?.addEventListener('click', () => applyEdits({ grayscale: true }));
document.querySelector('.Sepia')?.addEventListener('click', () => applyEdits({ sepia: true }));
document.querySelector('.Negative')?.addEventListener('click', () => applyEdits({ negative: true }));
document.querySelector('.Fade')?.addEventListener('click', () => applyEdits({ fade: 0.5 }));

// Canvas Tools
document.querySelector('.Aspect11')?.addEventListener('click', () => applyEdits({ aspect_ratio: "1:1" }));
document.querySelector('.Aspect45')?.addEventListener('click', () => applyEdits({ aspect_ratio: "4:5" }));
document.querySelector('.Aspect916')?.addEventListener('click', () => applyEdits({ aspect_ratio: "9:16" }));
document.querySelector('.Aspect169')?.addEventListener('click', () => applyEdits({ aspect_ratio: "16:9" }));

// Filter Tools
document.querySelector('.CustomFilter')?.addEventListener('click', () => applyEdits({ custom_filter: "custom" }));
document.querySelector('.HighlightColor')?.addEventListener('click', () => applyEdits({ custom_filter: "highlight_color" }));
document.querySelector('.Shadows')?.addEventListener('click', () => applyEdits({ custom_filter: "shadows" }));

// Frame Tools
document.querySelector('.AddBorder')?.addEventListener('click', () => applyEdits({ frame: "border" }));

// Tools
// let cropping = false;
// let cropStartX = 0;
// let cropStartY = 0;
// let cropCurrentX = 0;
// let cropCurrentY = 0;

// const cropCanvas = document.getElementById('crop-canvas');
// const uploadedImage = document.getElementById('uploaded-image');
// const ctx = cropCanvas.getContext('2d');

// function enableCrop() {
//     if (!uploadedImage.src) {
//         showToast("Please upload an image first.");
//         return;
//     }

//     cropCanvas.width = uploadedImage.clientWidth;
//     cropCanvas.height = uploadedImage.clientHeight;
//     cropCanvas.style.display = 'block';

//     // Clear previous drawings
//     ctx.clearRect(0, 0, cropCanvas.width, cropCanvas.height);

//     // Add event listeners for cropping
//     cropCanvas.addEventListener('mousedown', startCrop);
//     cropCanvas.addEventListener('mousemove', whileCropping);
//     cropCanvas.addEventListener('mouseup', endCrop);
//     cropCanvas.addEventListener('mouseout', cancelCrop);
// }

// function startCrop(e) {
//     cropping = true;
//     const rect = cropCanvas.getBoundingClientRect();
//     cropStartX = e.clientX - rect.left;
//     cropStartY = e.clientY - rect.top;
// }

// function whileCropping(e) {
//     if (!cropping) return;

//     const rect = cropCanvas.getBoundingClientRect();
//     cropCurrentX = e.clientX - rect.left;
//     cropCurrentY = e.clientY - rect.top;

//     // Draw rectangle
//     ctx.clearRect(0, 0, cropCanvas.width, cropCanvas.height);
//     ctx.strokeStyle = 'red';
//     ctx.lineWidth = 2;
//     ctx.setLineDash([6]);
//     const width = cropCurrentX - cropStartX;
//     const height = cropCurrentY - cropStartY;
//     ctx.strokeRect(cropStartX, cropStartY, width, height);
// }

// function endCrop(e) {
//     if (!cropping) return;
//     cropping = false;

//     // Remove event listeners
//     cropCanvas.removeEventListener('mousedown', startCrop);
//     cropCanvas.removeEventListener('mousemove', whileCropping);
//     cropCanvas.removeEventListener('mouseup', endCrop);
//     cropCanvas.removeEventListener('mouseout', cancelCrop);

//     const rect = cropCanvas.getBoundingClientRect();

//     // Calculate crop rectangle relative to original image
//     const scaleX = uploadedImage.naturalWidth / uploadedImage.clientWidth;
//     const scaleY = uploadedImage.naturalHeight / uploadedImage.clientHeight;

//     let x = Math.min(cropStartX, cropCurrentX) * scaleX;
//     let y = Math.min(cropStartY, cropCurrentY) * scaleY;
//     let width = Math.abs(cropCurrentX - cropStartX) * scaleX;
//     let height = Math.abs(cropCurrentY - cropStartY) * scaleY;

//     // Enforce bounds
//     x = Math.max(0, x);
//     y = Math.max(0, y);
//     width = Math.min(uploadedImage.naturalWidth - x, width);
//     height = Math.min(uploadedImage.naturalHeight - y, height);

//     // Call applyEdits with crop dimensions
//     applyEdits({ crop: { x: Math.floor(x), y: Math.floor(y), width: Math.floor(width), height: Math.floor(height) } });

//     // Hide the crop canvas
//     cropCanvas.style.display = 'none';
// }

// function cancelCrop() {
//     cropping = false;
//     ctx.clearRect(0, 0, cropCanvas.width, cropCanvas.height);
//     cropCanvas.style.display = 'none';
// }

// Call enableCrop when crop tool selected
// document.querySelector('.Crop').addEventListener('click', enableCrop);

document.querySelector('.Rotate')?.addEventListener('click', () => applyEdits({ rotate: 90 }));
document.querySelector('.FlipH')?.addEventListener('click', () => applyEdits({ flip_horizontal: true }));
document.querySelector('.FlipV')?.addEventListener('click', () => applyEdits({ flip_vertical: true }));

function downloadImage() {
    const imgSrc = document.getElementById('uploaded-image').src;
    if (!imgSrc) {
        showToast("No image to download.");
        return;
    }
    const link = document.createElement('a');
    link.href = imgSrc;
    link.download = 'edited_image.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Handling submenu navigation
document.addEventListener("DOMContentLoaded", function () {
    const mainTools = document.querySelector(".editing-tools");
    const uploadedImage = document.getElementById("uploaded-image");
    const subMenus = {
        ".Light": ".light-tools",
        ".Color": ".color-tools",
        ".Water": ".blur-tools",
        ".Sparkle": ".effect-tools",
        ".Zoom": ".detail-tools",
        ".Frame": ".canvas-tools",
        ".Mask": ".filter-tools",
        ".Wrench": ".tool-tools"
    };

    // Show toast function reused
    const showToastLocal = (msg) => {
        const toast = document.getElementById("toast");
        toast.textContent = msg;
        toast.className = "toast show";
        setTimeout(() => {
            toast.className = toast.className.replace("show", "");
        }, 3000);
    };

    function hideAllSubMenus() {
        Object.values(subMenus).forEach(selector => {
            const el = document.querySelector(selector);
            if (el) el.style.display = 'none';
        });
        if (mainTools) mainTools.style.display = 'block';
    }

    // Attach click handlers for main tools
    Object.keys(subMenus).forEach(key => {
        const btn = document.querySelector(key);
        if (btn) {
            btn.onclick = () => {
                if (!uploadedImage || !uploadedImage.src || uploadedImage.src.includes("placeholder")) {
                    showToastLocal("Please upload an image first.");
                    return;
                }
                hideAllSubMenus();
                const submenu = document.querySelector(subMenus[key]);
                if (submenu) submenu.style.display = 'flex';
                if (mainTools) mainTools.style.display = 'none';
            };
        }
    });

    // Back buttons hide submenus
    const backButtons = document.querySelectorAll('.Back');
    backButtons.forEach(backBtn => {
        backBtn.addEventListener('click', () => {
            hideAllSubMenus();
        });
    });
});