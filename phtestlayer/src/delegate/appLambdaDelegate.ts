
import { Main, phLogger, StoreEnum } from "phlayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        return await Main(StoreEnum.Postgres, event)
    }
}
