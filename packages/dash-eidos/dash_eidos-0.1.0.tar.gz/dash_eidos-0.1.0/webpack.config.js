const path = require("path");
const webpack = require("webpack");
const WebpackDashDynamicImport = require("@plotly/webpack-dash-dynamic-import");
const packagejson = require("./package.json");

const dashLibraryName = packagejson.name.replace(/-/g, "_");

module.exports = (env, argv) => {
  let mode;

  const overrides = module.exports || {};

  // if user specified mode flag take that value
  if (argv && argv.mode) {
    mode = argv.mode;
  }

  // else if configuration object is already set (module.exports) use that value
  else if (overrides.mode) {
    mode = overrides.mode;
  }

  // else take webpack default (production)
  else {
    mode = "production";
  }

  let filename = (overrides.output || {}).filename;
  if (!filename) {
    const modeSuffix = mode === "development" ? "dev" : "min";
    filename = `${dashLibraryName}.${modeSuffix}.js`;
  }

  const entry = overrides.entry || { main: "./src/lib/index.js" };

  const devtool = overrides.devtool || "source-map";

  const externals =
    "externals" in overrides
      ? overrides.externals
      : {
          react: "React",
          "react-dom": "ReactDOM",
          "plotly.js": "Plotly",
          "prop-types": "PropTypes",
        };

  return {
    mode,
    entry,
    output: {
      path: path.resolve(__dirname, dashLibraryName),
      chunkFilename: "[name].js",
      filename,
      library: dashLibraryName,
      libraryTarget: "global",
    },
    devtool,
    externals,
    resolve: {
      alias: {
        process: "process/browser",
      },
    },
    module: {
      rules: [
        {
          test: /\.jsx|\.js?$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
          },
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: "style-loader",
              // options: {
              //     insert: 'top',
              // },
            },
            {
              loader: "css-loader",
            },
          ],
        },
        {
          test: /\.js$/,
          enforce: "pre",
          use: ["source-map-loader"],
        },
      ],
    },
    optimization: {
      minimize: mode === "production",
      splitChunks: {
        name: "vendor",
      },
    },
    plugins: [
      new WebpackDashDynamicImport(),
      new webpack.SourceMapDevToolPlugin({
        filename: "[file].map",
        exclude: ["async-plotlyjs"],
      }),
      new webpack.ProvidePlugin({
        process: "process/browser",
      }),
    ],
  };
};
