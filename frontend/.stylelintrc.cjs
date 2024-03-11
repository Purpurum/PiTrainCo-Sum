const propertyGroups = require("stylelint-config-recess-order/groups");

module.exports = {
    extends: [
        "stylelint-config-standard-scss",
        "stylelint-config-recess-order",
        "stylelint-config-recommended-vue/scss",
    ],
    plugins: ["stylelint-scss", "stylelint-order"],
    rules: {
        "no-descending-specificity": null,
        "at-rule-no-unknown": null,
        "scss/at-rule-no-unknown": true,
        "declaration-empty-line-before": null,
        "order/properties-order": propertyGroups.map((group) => ({
            ...group,
            emptyLineBefore: "always",
            noEmptyLineBetween: false,
        })),
        "selector-pseudo-class-no-unknown": [
            true,
            {
                ignorePseudoClasses: ["global", "deep", "v-deep", "slotted"],
            },
        ],
        "selector-pseudo-element-no-unknown": [
            true,
            {
                ignorePseudoElements: ["v-deep"],
            },
        ],
        "color-function-notation": "modern",
        "selector-class-pattern": [
            "^([a-z][a-z0-9]*)(-[a-z0-9]+)*((__([a-z][a-z0-9]*)(-[a-z0-9]+)*)?(--([a-z][a-z0-9]*)(-[a-z0-9]+)*)?)*$",
            {
                message: "Expected custom property name to be kebab-case",
            },
        ],
        "selector-id-pattern": [
            "^([a-z][a-z0-9]*)(-[a-z0-9]+)*((__([a-z][a-z0-9]*)(-[a-z0-9]+)*)?(--([a-z][a-z0-9]*)(-[a-z0-9]+)*)?)*$",
            {
                message: "Expected custom property name to be kebab-case",
            },
        ],
        "custom-property-pattern": [
            "^([a-z][a-z0-9]*)(-[a-z0-9]+)*((__([a-z][a-z0-9]*)(-[a-z0-9]+)*)?(--([a-z][a-z0-9]*)(-[a-z0-9]+)*)?)*$",
            {
                message: "Expected custom property name to be kebab-case",
            },
        ],
        "scss/operator-no-newline-after": null,
        indentation: null,
        "value-keyword-case": [
            "lower",
            {
                ignoreFunctions: "v-bind",
            },
        ],
        "scss/no-global-function-names": null,
    },
};
