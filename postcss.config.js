module.exports = {
  plugins: {
    // Tailwind CSS v4 handles CSS imports and vendor prefixing itself,
    // so autoprefixer / postcss-preset-env are no longer needed.
    "@tailwindcss/postcss": {},
  },
};
