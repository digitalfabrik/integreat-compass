export const handleOfferDetails = () => {
    const allOffers = document.getElementsByClassName("single-offer");
    for (const offer of allOffers) {
        const id = offer.id.replace("offer-", "");
        const offerDetailLayover = document.getElementById(`offer-detail-layover-${id}`);
        const closeDetailLayover = document.getElementById(`btn-close-offer-detail-layover-${id}`);
        offer.addEventListener("click", () => {
            if (offerDetailLayover) {
                offerDetailLayover.classList.toggle("hidden");
            }
        });
        if (closeDetailLayover) {
            closeDetailLayover.addEventListener("click", () => {
                if (offerDetailLayover) {
                    offerDetailLayover.classList.toggle("hidden");
                }
            });
        }
    }
};

export const setLengthOfReview = (length: number) => {
    const offerRatingUsedWords = document.getElementById("offer-rating-used-words");
    if (offerRatingUsedWords) {
        offerRatingUsedWords.textContent = length.toString();
    }
};

export const countLengthOfReview = () => {
    const offerRatingTextarea = <HTMLInputElement>document.getElementById("offer-rating-textarea");
    let amountOfWords = 0;
    if (offerRatingTextarea) {
        offerRatingTextarea.addEventListener("input", () => {
            amountOfWords = offerRatingTextarea.value.length;
            setLengthOfReview(amountOfWords);
        });
    }
    setLengthOfReview(amountOfWords);
};
