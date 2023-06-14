const colors = require("tailwindcss/colors");

module.exports = {
  content: ["./integreat_compass/cms/templates/**/*.html", "./integreat_compass/static/src/js/**/*.{js,ts,tsx}"],
  theme: {
    colors: {
      transparent: "transparent",
      current: "currentColor",
      black: colors.black,
      white: colors.white,
      gray: colors.slate,
      red: colors.red,
      orange: colors.orange,
      yellow: colors.yellow,
      green: colors.green,
      blue: colors.blue,
      violet: colors.violet,
      primary: "#d55854",
    },
    extend: {
      colors: {
        water: {
          50: "#fefeff",
          100: "#fcfdff",
          200: "#f8fafe",
          300: "#f4f7fe",
          400: "#ecf1fd",
          500: "#e4ebfc",
          600: "#cdd4e3",
          700: "#abb0bd",
          800: "#898d97",
          900: "#70737b",
        },
        background: {
          50: "#fafafa",
          900: "#0a0011ab",
        },
      },
      backgroundImage: {
        "integreat-icon": "url('../images/favicon.svg')",
        "integreat-logo": "url('../images/logo-integreat-compass.svg')",
      },
      fontFamily: {
        "default": ["Roboto", "Raleway", "Lateef", "Noto Sans SC", "sans-serif", "Noto Sans Ethiopic"],
        "content": ["Open Sans", "sans-serif"],
        "content-rtl": ["Lateef", "sans-serif"],
        "content-sc": ["Noto Sans SC", "sans-serif"],
        "content-am": ["Noto Sans Ethiopic", "sans-serif"],
      },
      maxHeight: {
        15: "3.75rem",
        116: "29rem",
        160: "40rem",
      },
      gridTemplateColumns: {
        gallery: "repeat(auto-fill, minmax(180px, 1fr))",
      },
      width: {
        120: "30rem",
        136: "34rem",
        160: "40rem",
      },
      screens: {
        "3xl": "1700px",
        "4xl": "2100px",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
