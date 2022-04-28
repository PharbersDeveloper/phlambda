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
    roots: [
        "<rootDir>/tests"
    ],
    testRegex: "(tests/.*|(\\.|/)(test|spec))\\.(jsx?|tsx?)$",
    moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"],
    reporters: [
        "default",
        [ "jest-junit", {
            outputDirectory: "../../phoauth-report-directory",
            outputName: "phoauth-report-file.xml",
        } ]
    ],
    testTimeout: 1000 * 60 * 60
};
module.exports = config;
