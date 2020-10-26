import { Main } from "phnodelayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        return await Main(event)
    }
}
