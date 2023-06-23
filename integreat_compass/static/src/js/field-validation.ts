window.addEventListener("load", () => {
    const urlField = document.getElementById("id_organization-web_address") as HTMLInputElement;
    if (urlField) {
        urlField.addEventListener("blur", () => {
            if (!urlField.value.match(/^https?:/)) {
                urlField.value = `http://${urlField.value}`;
            }
        });
    }
});
