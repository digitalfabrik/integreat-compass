window.addEventListener("load", () => {
    const titleImagePicker = document.querySelector("#title-image-picker") as HTMLInputElement;
    const titleImagePreview = document.querySelector("#title-image-preview") as HTMLImageElement;
    const titleImageReset = document.querySelector("#title-image-reset") as HTMLElement;
    const hiddenReset = document.querySelector("#offer_version-title_image-clear_id") as HTMLInputElement;

    if (!titleImagePicker || !titleImagePreview || !titleImageReset || !hiddenReset) {
        return;
    }

    titleImagePicker.addEventListener("change", () => {
        if (!titleImagePicker.files) {
            return;
        }
        const src = URL.createObjectURL(titleImagePicker.files[0]);
        titleImagePreview.src = src;
        (titleImagePreview.parentNode as HTMLElement)?.classList.remove("hidden");
        hiddenReset.checked = false;
    });

    titleImageReset.addEventListener("click", () => {
        const dt = new DataTransfer();
        titleImagePicker.files = dt.files;
        titleImagePreview.src = "";
        (titleImagePreview.parentNode as HTMLElement)?.classList.add("hidden");
        hiddenReset.checked = true;
    });
});
