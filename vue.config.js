const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  pluginOptions: {
    electronBuilder: {
      // chainWebpackMainProcess: (config) => {
      //   config.module
      //     .rule('style')
      //     .test(/\.(sass|scss|css)$/)
      //     .use(['style-loader', 'css-loader', 'sass-loader'])
      //     .loader(['style-loader', 'css-loader', 'sass-loader'])
      //     .end()
      // },
      // chainWebpackRenderProcess: (config) => { },
      preload: 'src/main/preload.js',
      mainProcessFile: 'src/main/main.js',
      rendererProcessFile: 'src/renderer/main.js',
      nodeIntegration: false,
      builderOptions: {
        // options here will be merged with default electron-builder options
        // https://www.electron.build/configuration/configuration
      }
    }
  },
  transpileDependencies: [
    'vuetify'
  ]
})
