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
    reporters: [
        'default',
        [ 'jest-junit', {
            outputDirectory: './phtm-report-directory',
            outputName: 'phtm-report-file.xml',
        } ]
    ],
    testTimeout: 1000 * 3
};
module.exports = config;
