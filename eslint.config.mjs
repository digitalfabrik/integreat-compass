import path from "node:path";
import { fileURLToPath } from "node:url";

import js from "@eslint/js";
import { configs, plugins } from "eslint-config-airbnb-extended";
import preferArrow from "eslint-plugin-prefer-arrow";
import prettierRecommended from "eslint-plugin-prettier/recommended";
import { defineConfig, globalIgnores } from "eslint/config";
import globals from "globals";

const projectDir = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig([
    globalIgnores(["**/dist/", "**/htmlcov/**", "**/node_modules/", "*.config.js", ".venv/", "build/", "docs/"]),

    { name: "js/recommended", ...js.configs.recommended },

    // Airbnb base (JS rules + import-x + stylistic) and its TypeScript layer
    plugins.stylistic,
    plugins.importX,
    ...configs.base.recommended,
    plugins.typescriptEslint,
    ...configs.base.typescript,

    // Airbnb React layer (Preact reuses the React plugins)
    plugins.react,
    plugins.reactHooks,
    plugins.reactA11y,
    ...configs.react.recommended,
    ...configs.react.typescript,

    // Prettier last so it can switch off conflicting formatting rules
    prettierRecommended,

    {
        // Applies to every file (incl. this .mjs config) so it overrides Airbnb's
        // "detect". Preact uses the "h" pragma and there is no "react" package to detect.
        name: "integreat-compass/react-settings",
        settings: {
            react: { pragma: "h", version: "18.3" },
        },
    },

    {
        name: "integreat-compass/project",
        files: ["**/*.{js,jsx,ts,tsx}"],
        languageOptions: {
            globals: { ...globals.browser },
            parserOptions: {
                tsconfigRootDir: projectDir,
                ecmaFeatures: { jsx: true },
            },
        },
        plugins: { "prefer-arrow": preferArrow },
        rules: {
            // Preact: no React import needed in scope
            "react/react-in-jsx-scope": "off",

            // console output is used intentionally for client-side diagnostics
            "no-console": "off",

            // overly strict rules
            "@typescript-eslint/strict-boolean-expressions": "off",
            "function-paren-newline": "off",
            "no-restricted-syntax": "off",
            "react/jsx-props-no-spreading": "off",
            "react/no-unknown-property": "off",

            // unwanted
            "import-x/extensions": "off",
            "import-x/no-extraneous-dependencies": "off",
            "import-x/prefer-default-export": "off",
            "lines-between-class-members": "off",
            "react/jsx-filename-extension": "off",
            "react/jsx-fragments": "off",
            "react/require-default-props": "off",

            // better @typescript-eslint rules are available
            "default-case": "off", // => @typescript-eslint/switch-exhaustiveness-check
            "no-unused-vars": "off", // => @typescript-eslint/no-unused-vars
            "no-use-before-define": "off", // => @typescript-eslint/no-use-before-define

            // project-specific (typescript)
            "@typescript-eslint/await-thenable": "error",
            "@typescript-eslint/ban-ts-comment": "error",
            "@typescript-eslint/consistent-type-definitions": ["error", "type"],
            "@typescript-eslint/no-empty-function": "error",
            "@typescript-eslint/no-unused-vars": [
                "error",
                {
                    argsIgnorePattern: "_(unused)?",
                    varsIgnorePattern: "_(unused)?",
                    ignoreRestSiblings: true,
                },
            ],
            "@typescript-eslint/no-use-before-define": "error",
            "@typescript-eslint/switch-exhaustiveness-check": "error",

            // project-specific (general)
            "curly": ["error", "all"],
            "func-names": "error",
            "no-magic-numbers": [
                "error",
                {
                    ignore: [-1, 0, 1, 2, 100],
                    ignoreArrayIndexes: true,
                },
            ],
            "no-mixed-operators": "error",
            "no-plusplus": ["error", { allowForLoopAfterthoughts: true }],
            "prefer-destructuring": ["error", { array: false }],
            "prefer-arrow/prefer-arrow-functions": "error",
            "prefer-object-spread": "error",
            "prefer-template": "error",
            "react/function-component-definition": ["error", { namedComponents: "arrow-function" }],
            "react-hooks/exhaustive-deps": "error",
            "vars-on-top": "error",
        },
    },

    // officially recommended by TypeScript ESLint
    {
        name: "integreat-compass/typescript-files",
        files: ["**/*.{ts,mts,cts,tsx}"],
        rules: {
            "no-undef": "off",
        },
    },
]);
