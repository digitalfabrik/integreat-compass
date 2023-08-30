import "./css/style.scss";
import "./js/comments";
import "./js/confirm-deletion";
import "./js/field-validation";
import "./js/display-filenames";
import "./js/image_picker";
import "./js/map";
import "./js/messages";
import { createIconsAt } from "./js/utils/create-icons";
import { handleOfferDetails } from "./js/offer-details";
import { submitFilter } from "./js/filter";
import { handleModal } from "./js/application-overlay";

window.addEventListener("DOMContentLoaded", () => {
    createIconsAt(document.documentElement);
    handleOfferDetails();
    submitFilter();
    handleModal();
    const event = new Event("icon-load");
    window.dispatchEvent(event);
});
