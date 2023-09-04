export const submitFilter = () => {
    const filterElements = Array.from(document.getElementsByClassName("filter-element"));
    const filterForm = <HTMLFormElement>document.getElementById("filter-form");
    filterElements.forEach((element) => {
        (element as HTMLInputElement).addEventListener("change", () => {
            // keep unnecessary fields out of the URL
            const candidates = ["search", "radius", "id_location-lat", "id_location-long"];
            candidates.forEach((candidate) => {
                const element = filterForm.querySelector(`#${candidate}`) as HTMLInputElement;
                if (element && !element.value) {
                    element.disabled = true;
                }
            });
            (document.querySelector("#filter-address") as HTMLInputElement).disabled = true;
            filterForm?.submit();
        });
    });
};
