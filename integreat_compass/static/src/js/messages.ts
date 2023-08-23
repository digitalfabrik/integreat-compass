const minDisplayTime = 4000;
const fadeOutOffset = 700;

const fadeMessages = (
    messages: NodeListOf<HTMLDivElement> | HTMLDivElement[],
    index: number,
    offsetOverwrite?: number,
) => {
    if (index >= messages.length) {
        return;
    }

    setTimeout(() => {
        /* eslint-disable-next-line no-param-reassign */
        messages[messages.length - 1 - index].style.opacity = "0";
        fadeMessages(messages, index + 1);
        setTimeout(() => {
            messages[messages.length - 1 - index].remove();
        }, fadeOutOffset);
    }, offsetOverwrite ?? fadeOutOffset);
};

window.addEventListener("load", () => {
    const messagesContainer = document.getElementById("messages");
    if (!messagesContainer) {
        return;
    }
    const messages = messagesContainer.querySelectorAll("div");

    messages.forEach((message) => {
        message.querySelector(".message-close")?.addEventListener("click", () => {
            fadeMessages([message], 0, 0);
        });
    });

    setTimeout(() => {
        fadeMessages(messages, 0);
    }, minDisplayTime);
});
