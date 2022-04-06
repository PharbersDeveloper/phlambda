import { DBConfig, IStore, Logger, Register, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { PostgresConf, RedisConf } from "../constants/common"

export default class AppLambdaDelegate {

    private readonly pg: IStore
    private readonly rds: IStore

    public constructor() {
        const configs = [
            new DBConfig(PostgresConf),
            new DBConfig(RedisConf)
        ]
        ServerRegisterConfig(configs)
        this.pg = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        this.rds = Register.getInstance.getData(StoreEnum.REDIS) as IStore
    }

    public async exec(event: any) {
        return await this.verifyEmail(event)
    }

    private response(code: number, message: string) {
        const header = "HTTP/1.1 200 OK\r\nContent-Type: application/vnd.api+json\r\nETag: W/9bc30459\r\nDate: Wed, 11 Nov 2020 08:56:07 GMT\r\nConnection: keep-alive\r\n\r\n"
        return {
            statusCode: code,
            output: [ header, JSON.stringify({status: message}) ]
        }
    }

    private async verifyEmail(event: Map<string, string>) {
        try {
            // @ts-ignore
            const email = event.queryStringParameters.email
            const result = await this.pg.find("account", null, { match: { email } })
            if (result.payload.records.length === 0) {
                return this.response(404, "error")
            }
            return this.response(200, "success")
        } catch (e) {
            Logger.error(e)
            return this.response(500, "error")
        }
    }
}
