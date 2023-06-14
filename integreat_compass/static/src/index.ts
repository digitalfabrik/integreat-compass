import "./css/style.scss";
import "./js/map";
import { createIconsAt } from "./js/utils/create-icons";

window.addEventListener("DOMContentLoaded", () => {
    createIconsAt(document.documentElement);
    const event = new Event("icon-load");
    window.dispatchEvent(event);
});
