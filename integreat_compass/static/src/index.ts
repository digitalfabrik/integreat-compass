import "./css/style.scss";
import "./js/confirm-deletion";
import "./js/field-validation";
import "./js/display_filenames";
import "./js/image_picker";
import "./js/map";
import { createIconsAt } from "./js/utils/create-icons";

window.addEventListener("DOMContentLoaded", () => {
    createIconsAt(document.documentElement);
    const event = new Event("icon-load");
    window.dispatchEvent(event);
});
