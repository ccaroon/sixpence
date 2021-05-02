module.exports = {
  root: true,
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: 'babel-eslint',
    sourceType: 'module'
  },
  env: {
    browser: true,
    node: true
  },
  extends: [
    'standard',
    'plugin:vue/essential'
  ],
  globals: {
    __static: true
  },
  plugins: [],
  // 0 = OFF | 1 = WARN | 2 = ERR
  'rules': {
    'arrow-parens': 0,
    'generator-star-spacing': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    "space-before-function-paren": ["warn", {
      "anonymous": "always",
      "named": "ignore",
      "asyncArrow": "always"
    }],
    'lines-between-class-members': ["warn", "always", {
      'exceptAfterSingleLine': true
    }],
    // ----- VUE -----
    'vue/no-mutating-props': 0
  }
}
