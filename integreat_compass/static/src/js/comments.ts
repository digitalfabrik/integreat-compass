window.addEventListener("load", () => {
    const forms = document.querySelectorAll(".comment-form") as NodeListOf<HTMLFormElement>;

    forms.forEach((form) => {
        const textarea = form.querySelector("textarea") as HTMLTextAreaElement;
        const charCounter = form.querySelector(".comment-length") as HTMLElement;
        ["change", "keyup"].forEach((event) => {
            textarea.addEventListener(event, () => {
                charCounter.innerHTML = textarea.value.length.toString();
            });
        });

        form.addEventListener("submit", async (event: SubmitEvent) => {
            event.preventDefault();

            const formData = new FormData(form);

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": formData.get("csrfmiddlewaretoken") as string,
                    },
                });

                const STATUS_CREATED = 201;
                if (response.status !== STATUS_CREATED) {
                    (form.querySelector(".error-message") as HTMLElement)?.classList.remove("hidden");
                } else {
                    const offerId = formData.get("offer_id");
                    const commentText = formData.get("comment");
                    const currentDate = new Date().toLocaleDateString("de-DE", {
                        day: "numeric",
                        month: "short",
                        year: "numeric",
                    });

                    (form.querySelector(".error-message") as HTMLElement)?.classList.add("hidden");
                    form.reset();

                    const newCommentDiv = document.createElement("div");
                    newCommentDiv.innerHTML = `
          <div class="mt-4 bg-green-100 rounded">
            <p>${commentText}</p>
            <p class="text-sm text-gray-500">${currentDate}</p>
          </div>
        `;

                    const commentContainer = document.querySelector(`#comment-container-${offerId}`) as HTMLElement;
                    commentContainer.parentElement?.parentElement?.classList.remove("hidden");

                    commentContainer.prepend(newCommentDiv);
                    const fadeout = 1000;
                    setTimeout(() => {
                        (newCommentDiv.firstElementChild as HTMLElement).style.transition =
                            "background-color 1s ease-in-out";
                        (newCommentDiv.firstElementChild as HTMLElement).style.backgroundColor = "transparent";
                    }, fadeout);
                }
            } catch (error) {
                console.error("An error occurred:", error);
            }
        });
    });
});
