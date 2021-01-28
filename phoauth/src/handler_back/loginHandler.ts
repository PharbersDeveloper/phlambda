// import { ServerResponse } from "http"
// import { errors2response, PhInvalidPassword, PhNotFoundError, PhRecordLoss } from "../errors/pherrors"
// import { IHandler } from "./IHandler"
//
// // TODO 兼容产品的登入注册前端页面走向逻辑
// export default class LoginHandler implements IHandler {
//     public async execute(event: any, response: ServerResponse, pg: any, redis: any) {
//         const email = event.queryStringParameters.email
//         const result = await pg.find("account", null, { match: { email } })
//         if (result.payload.records.length === 0) {
//             errors2response(PhNotFoundError, response)
//             return response
//         }
//         const records = result.payload.records
//         if (records.length === 1 && (records.password !== "" || records.password !== null)) {
//             const account = records[0]
//             // @ts-ignore
//             if (account.password === event.queryStringParameters.password) {
//                 response.statusCode = 200
//                 // @ts-ignore
//                 response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
//                 // @ts-ignore
//                 response.body = { message: "login success", uid: account.id }
//             } else {
//                 errors2response(PhInvalidPassword, response)
//             }
//         } else {
//             errors2response(PhRecordLoss, response)
//         }
//         return response
//     }
// }
