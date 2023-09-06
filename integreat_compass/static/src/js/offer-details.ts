export const handleOfferDetails = () => {
    const allOffers = document.getElementsByClassName("open-details");
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
        if (offerDetailLayover) {
            // Close window by clicking on backdrop.
            offerDetailLayover.addEventListener("click", (e) => {
                if (e.target === offerDetailLayover) {
                    offerDetailLayover.classList.toggle("hidden");
                }
            });
        }
    }
};
