const path = require("path");
module.exports = {
  entry: {
    main: "./integreat_compass/static/src/index.ts",
  },
  output: {
    filename: "[name].[contenthash].js",
    path: path.resolve(__dirname, "integreat_compass/static/dist"),
    clean: true,
    assetModuleFilename: "assets/[name]-[hash][ext][query]",
  },
};
