import { SF, Store } from "phnodelayer"
import {InvalidRequestError} from "../errors"
import { Request } from "../request"
import { Response } from "../response"

export class UserInfoHandler {
    async handle(request: Request, response: Response) {
        const authorization = request.get("Authorization")
        const matches = authorization.match(/Bearer\s(\S+)/)

        if (!matches) {
            throw new InvalidRequestError(
                "Invalid request: malformed authorization header",
            )
        }
        const token = matches[1]
        const redis = SF.getInstance.get(Store.Redis)
        const pg = SF.getInstance.get(Store.Postgres)
        const result = await redis.find("access", null, {match: {token}})
        const records = result.payload.records
        if (records.length > 0) {
            const account = await pg.find("account", records[0].uid)
            const userName = account.payload.records[0].name
            response.headers = { "Content-Type": "application/json" }
            response.body = { username: userName }
        } else {
            throw new InvalidRequestError("Invalid request: token invalid")
        }
        return response
    }
}
