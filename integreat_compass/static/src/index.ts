import "./css/style.scss";
import "./js/field-validation";
import "./js/display_filenames";
import "./js/image_picker";
import "./js/map";
import { createIconsAt } from "./js/utils/create-icons";
import { handleOfferDetails, countLengthOfReview, setLengthOfReview } from "./js/offer-details";

window.addEventListener("DOMContentLoaded", () => {
    createIconsAt(document.documentElement);
    handleOfferDetails();
    countLengthOfReview();
    const event = new Event("icon-load");
    window.dispatchEvent(event);
});
