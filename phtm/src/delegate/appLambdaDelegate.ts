// import { identify } from "phauthlayer"
import { ConfigRegistered, JsonApiMain, Logger, MongoConfig, RedisConfig, SF, Store } from "phnodelayer"
import { MongoConf } from "../common/config"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        Logger.info("Run")

        const mongoConf = new MongoConfig(
            "mongodb",
            MongoConf.entry,
            MongoConf.user,
            MongoConf.password,
            MongoConf.url,
            MongoConf.port,
            MongoConf.db,
            1,
            1000,
            1000,
            MongoConf.other
        )
        ConfigRegistered.getInstance.registered(mongoConf)
        const dbIns = SF.getInstance.get(Store.Mongo)
        await dbIns.open()
        const result = await JsonApiMain({event, db: dbIns})
        await dbIns.close()
        return result
    }
}
