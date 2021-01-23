import { ServerResponse } from "http"
import {  Logger } from "phnodelayer"
import { IHandler } from "./IHandler"
export default class UserInfoHandler implements IHandler {

    public async  execute(event: any, response: ServerResponse, pg: any, redis: any) {
        Logger.info(JSON.stringify(event))
        const token  = event.headers.Authorization.replace("bearer ", "")
        const result = await redis.find("access", null, {match: {token}})
        const records = result.payload.records
        if (records.length > 0) {
            const account = await pg.find("account", records[0].uid)
            const userName = account.payload.records[0].name
            // @ts-ignore
            response.statusCode = 200
            // @ts-ignore
            response.headers = { "Content-Type": "application/json" }
            // @ts-ignore
            response.body = { username: userName }
        } else {
            throw new Error("user is null")
        }
        return response
    }
}
