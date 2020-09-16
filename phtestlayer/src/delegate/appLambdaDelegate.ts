
import { DBFactory, Main, phLogger, StoreEnum } from "phlayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        return await Main(event, StoreEnum.Postgres)
    }

    // public async getRedis() {
    //     const redisStore = DBFactory.getInstance.getStore(StoreEnum.Redis)
    //     await redisStore.connect()
    //     redisStore.adapter.redis.set("Fuck", "You", "EX", 1000000)
    //     await redisStore.disconnect()
    // }
}
