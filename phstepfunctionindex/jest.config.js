const config = {
    verbose: true,
    transform: {
        ["^.+\\.(t)sx?$"]: "ts-jest"
    },
    collectCoverage: true,
    testEnvironment: "node",
    coveragePathIgnorePatterns: [
        "<rootDir>/node_modules/",
        "<rootDir>/app.js"
    ],
    testRegex: "(/__tests__/.*|(\\.|/)(test|spec))\\.(jsx?|tsx?)$",
    moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"],
    testTimeout: 1000 * 60 * 60
};
module.exports = config;
