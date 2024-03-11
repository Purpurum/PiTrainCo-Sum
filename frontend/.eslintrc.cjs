/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
    root: true,
    extends: ['plugin:vue/vue3-essential', 'eslint:recommended', '@vue/eslint-config-prettier'],
    parserOptions: {
        ecmaVersion: 'latest'
    },
    settings: {
        'import/resolver': {
            alias: {
                map: [['@', './src']]
            },
            node: {
                extensions: ['.js', '.jsx', '.ts', '.tsx'],
                moduleDirectory: ['node_modules', 'src/']
            }
        },
        'prettier/prettier': [
            'error',
            {
                tabWidth: 4,
                endOfLine: 'auto'
            }
        ]
    }
}
