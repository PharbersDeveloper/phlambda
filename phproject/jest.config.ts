import type {Config} from "@jest/types"

const config: Config.InitialOptions = {
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
    moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"]
}
export default config
