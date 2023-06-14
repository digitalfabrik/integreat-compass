// Since the module does not export the replaceElement function, we have to declare it here
declare module "lucide/dist/esm/replaceElement" {
    const replaceElement: (element: Element, { nameAttr, icons, attrs }: ReplaceElementOptions) => void;
    export default replaceElement;
}
