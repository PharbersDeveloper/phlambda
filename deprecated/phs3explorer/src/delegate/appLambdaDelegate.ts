import { DBConfig, Logger, ServerRegisterConfig } from "phnodelayer"
import { PostgresConf } from "../constants/common"
import PutAssetDataHandler from "../handler/PutAssetDataHandler"
import S3Handler from "../handler/S3Handler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        Logger.info(event)
        try {
            ServerRegisterConfig([new DBConfig(PostgresConf)])

            const parameters = event.parameters
            const { owner, tempfile, tags } = parameters.puts3_event
            const s3 = new S3Handler()
            const dbOP = new PutAssetDataHandler()
            const key = `user/${owner}/${tempfile}`
            await s3.putFile("ph-origin-files",
                key,
                process.env.PATH_PREFIX + tempfile,
                tags.map(( item ) => `${item.Key}=${encodeURI(item.Value)}`).join("&"))
            await dbOP.PutAssetData(parameters.puts3_event)
        } catch (error) {
            Logger.error(error)
            throw error
        }
    }
}
