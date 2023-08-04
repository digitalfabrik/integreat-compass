export const submitFilter = () => {
    const filterElements = Array.from(document.getElementsByClassName("filter-element"));
    const filterForm = <HTMLFormElement>document.getElementById("filter-form");
    filterElements.forEach((element) => {
        (element as HTMLInputElement).addEventListener("change", () => {
            filterForm?.submit();
        });
    });
};
