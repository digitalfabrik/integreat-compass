export const openOverlay = () => {
    const allElements = document.getElementsByClassName("report-more")
    for (const element of allElements) {
        const id = element.id.replace("report-more-", "");
        const reportDetailOverlay = document.getElementById(`report-detail-${id}`);
        const closeDetailLayover = document.getElementById(`btn-close-report-detail-layover-${id}`);
        element.addEventListener("click", () => {
            if (reportDetailOverlay){
                reportDetailOverlay.classList.toggle("hidden");
            }
        })
        if (closeDetailLayover) {
            closeDetailLayover.addEventListener("click", () => {
                if (reportDetailOverlay) {
                    reportDetailOverlay.classList.toggle("hidden");
                }
            });
        }
    };
}