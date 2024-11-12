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
  },
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      Object.assign(args[0], {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
        __VUE_PROD_DEVTOOLS__: false
      })
      return args
    })
  }
})
