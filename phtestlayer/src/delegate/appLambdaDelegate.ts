
import { DBFactory, Main, phLogger, Redis, StoreEnum } from "phlayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        return await Main(event, StoreEnum.Postgres)
    }

    // public async DBFactory() {
    //     const redisStore = DBFactory.getInstance.getStore(StoreEnum.Redis)
    //     await redisStore.connect()
    //     redisStore.adapter.redis.set("Fuck", "You", "EX", 1000000)
    //     await redisStore.disconnect()
    // }

    public async redisOperation() {
        const rds = Redis.getInstance
        await rds.open()
        rds.setExpire("Fuck", "You", 1000000)
        await rds.close()
    }
}
