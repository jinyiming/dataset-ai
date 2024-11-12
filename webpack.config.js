const webpack = require('webpack')

module.exports = {
  // ... 其他配置
  plugins: [
    new webpack.DefinePlugin({
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
      __VUE_PROD_DEVTOOLS__: JSON.stringify(false)
    })
  ]
} 