window.addEventListener("load", () => {
    document.querySelectorAll(".confirm-delete").forEach((node) => {
        const confirmMessage = (node as HTMLElement)?.dataset.confirm;
        node.addEventListener("click", (event) => {
            /* eslint-disable-next-line no-alert */
            const result = window.confirm(confirmMessage);
            if (!result) {
                event.preventDefault();
            }
        });
    });
});
