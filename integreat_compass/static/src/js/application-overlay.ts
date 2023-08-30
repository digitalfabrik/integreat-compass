const toggleModal = (modal: HTMLElement, closeButton: HTMLElement, openButton: HTMLElement) => {
    closeButton.addEventListener("click", () => {
        modal.classList.toggle("hidden");
    });
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.toggle("hidden");
        }
    });
    openButton.addEventListener("click", () => {
        modal.classList.toggle("hidden");
    });
};

const handleSingluarModal = (mode: string, buttonCollection: HTMLCollection) => {
    for (const button of buttonCollection) {
        const id = button.id.replace("offer-", "");
        const modal = document.getElementById(`application-modal-${mode}-${id}`);
        const cancelButton = document.getElementById(`application-modal-${mode}-cancel-${id}`);
        if (modal && cancelButton && button) {
            toggleModal(modal, cancelButton, button as HTMLElement);
        }
    }
};

export const handleModal = () => {
    const acceptButtons = document.getElementsByClassName("open-accept-modal");
    const declineButtons = document.getElementsByClassName("open-decline-modal");
    handleSingluarModal("decline", declineButtons);
    handleSingluarModal("accept", acceptButtons);
};
