import { createIcons, icons } from "lucide";

// This function renders all <i icon-name="..."> children of `root`
export const createIconsAt = (root: HTMLElement) => {
    createIcons({
        icons,
        nameAttr: "icon-name",
        attrs: { class: "inline-block" },
        root,
    });
};
