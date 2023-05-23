export const handleOfferDetails = () => {
    const allOffers = document.getElementsByClassName("single-offer");
    const offerDetailLayover = document.getElementById("offer-detail-layover");
    const closeDetailLayover = document.getElementById(
        "btn-close-offer-detail-layover",
    );
    for (let offer of allOffers) {
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


export const countLengthOfReview = () => {
    const offerRatingTextarea = <HTMLInputElement> document.getElementById("offer-rating-textarea");
    let amountOfWords = 0;
    if (offerRatingTextarea) {
        offerRatingTextarea.addEventListener("input", () => {
            amountOfWords =  offerRatingTextarea.value.length;
            setLengthOfReview(amountOfWords)
        })
    }
    setLengthOfReview(amountOfWords)
}

export const setLengthOfReview = (length : unknown) => {
    const offerRatingUsedWords = document.getElementById("offer-rating-used-words")
    if (offerRatingUsedWords) {
        offerRatingUsedWords.textContent = length as string;
    }
}