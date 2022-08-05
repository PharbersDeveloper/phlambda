import FunctionDelegate from "./functionDelegate"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            return await new FunctionDelegate().run(event)
        } catch (error) {
            throw error
        }
    }
}
