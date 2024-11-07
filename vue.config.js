const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  configureWebpack: {
    resolve: {
      fallback: {
        "stream": require.resolve("stream-browserify"),
        "buffer": require.resolve("buffer/")
      }
    }
  },
  devServer: {
    historyApiFallback: true
  }
})
