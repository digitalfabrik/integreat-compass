import { createIconsAt } from "./utils/create-icons";

window.addEventListener("load", () => {
    const fileInput: HTMLInputElement | null = document.querySelector("#document-upload-zone");
    const fileInputLabel = fileInput?.labels?.[0];
    const fileNameList: HTMLElement | null = document.querySelector("#file-name-list");

    if (!fileInput || !fileInputLabel || !fileNameList) {
        return;
    }

    const dt = new DataTransfer();

    const fileNameEntry = (name: string) =>
        `<div><i data-name="${name}" icon-name="minus-circle" class="w-4 h-4 remove-file cursor-pointer text-red-700"></i> ${name}</div>\n`;

    const refreshFileNameList = () => {
        fileNameList.innerHTML = "";
        for (let i = 0; i < dt.files.length; i++) {
            fileNameList.innerHTML += fileNameEntry(dt.files[i].name);
        }
        createIconsAt(fileNameList);
        /* eslint-disable-next-line @typescript-eslint/no-use-before-define */
        addFileRemovalListeners();
    };

    const addFileRemovalListeners = () => {
        document.querySelectorAll(".remove-file").forEach((node) => {
            node.addEventListener("click", ({ currentTarget }) => {
                const fileName = (currentTarget as HTMLElement).dataset.name;
                for (let i = 0; i < dt.files.length; i++) {
                    if (dt.files[i].name === fileName) {
                        dt.items.remove(i);
                    }
                }
                refreshFileNameList();
                fileInput.files = dt.files;
            });
        });
    };

    const addFiles = () => {
        if (!fileInput.files) {
            return;
        }

        for (let i = 0; i < fileInput.files.length; i++) {
            dt.items.add(fileInput.files[i]);
        }
        refreshFileNameList();
        fileInput.files = dt.files;
    };

    fileInput.addEventListener("change", addFiles);
    fileInput.dispatchEvent(new Event("change"));

    fileInputLabel.addEventListener("dragenter", () => {
        fileInputLabel.classList.add("text-gray-600");
        fileInputLabel.classList.add("border-gray-400");
    });
    fileInputLabel.addEventListener("dragleave", () => {
        fileInputLabel.classList.remove("text-gray-600");
        fileInputLabel.classList.remove("border-gray-400");
    });
    fileInputLabel.addEventListener("dragover", (e) => {
        e.preventDefault();
    });
    fileInputLabel.addEventListener("drop", (e) => {
        fileInputLabel.classList.remove("text-gray-600");
        fileInputLabel.classList.remove("border-gray-400");
        fileInput.files = e.dataTransfer?.files || null;
        addFiles();
    });
    document.addEventListener("drop", (e) => {
        e.preventDefault();
        e.stopPropagation();
    });

    document.querySelectorAll(".document-deletion-checkbox svg").forEach((node) => {
        node.addEventListener("click", ({ currentTarget }) => {
            const input = (currentTarget as HTMLElement).parentNode?.querySelector("input");
            if (input) {
                input.checked = true;
            }

            const parent = (currentTarget as HTMLElement).parentNode;
            if (parent) {
                (parent as HTMLElement).classList.add("hidden");
            }
        });
    });
});
