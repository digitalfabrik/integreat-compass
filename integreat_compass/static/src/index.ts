import "./css/style.scss";
import "./js/confirm-deletion";
import "./js/field-validation";
import "./js/display_filenames";
import "./js/image_picker";
import "./js/map";
import { createIconsAt } from "./js/utils/create-icons";
import { handleOfferDetails, countLengthOfReview } from "./js/offer-details";
import { submitFilter } from "./js/filter";
import { openOverlay } from "./js/report-details";

window.addEventListener("DOMContentLoaded", () => {
    createIconsAt(document.documentElement);
    handleOfferDetails();
    countLengthOfReview();
    submitFilter();
    openOverlay();
    const event = new Event("icon-load");
    window.dispatchEvent(event);
});
