module.exports = {
    root: true,
    env: {
        node: true,
    },
    extends: ['plugin:vue/vue3-essential', 'eslint:recommended', '@vue/prettier'],
    parserOptions: {
        parser: '@babel/eslint-parser',
    },
    rules: {
        'prettier/prettier': [
            'warn',
            {
                semi: true,
                singleQuote: true,
                trailingComma: 'all',
                printWidth: 100,
                tabWidth: 4,
                bracketSpacing: true,
                arrowParens: 'avoid',
                endOfLine: 'lf',
                vueIndentScriptAndStyle: true,
                htmlWhitespaceSensitivity: 'strict',
                singleAttributePerLine: false,
            },
        ],
        'vue/multi-word-component-names': 'off',
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    },
};
