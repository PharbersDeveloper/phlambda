import { IStore, Logger, Register, StoreEnum } from "phnodelayer"
import { errors2response, PhInvalidPassword, PhNotFoundError, PhRecordLoss} from "../errors/pherrors"
import { Request } from "../request"
import { Response } from "../response"

export class LoginHandler {
    /**
     * Login Handle
     * @param request
     * @param response
     */
    async handle(request: Request, response: Response) {
        const account = request.body.account || request.query.account
        const password = request.body.password || request.query.password

        const pg = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        const result = await pg.find("account", null, { match: { email: account } })
        if (result.payload.records.length === 0) {
            errors2response(PhNotFoundError, response)
            return response
        }
        const records = result.payload.records
        if (records.length === 1 && (records.password !== "" || records.password !== null)) {
            const acc = records[0]
            if (acc.password === password) {
                response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
                response.body = { message: "login success", uid: acc.id }
            } else {
                errors2response(PhInvalidPassword, response)
            }
        } else {
            errors2response(PhRecordLoss, response)
        }
        return response
    }
}
