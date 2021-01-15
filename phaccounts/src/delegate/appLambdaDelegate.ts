import moment from "moment"
import { dbFactory, logger, redis, store } from "phnodelayer"
import EmailFacade from "../facade/emailFacade"
import RandomCode from "../utils/randomCode"

export default class AppLambdaDelegate {
    private rds: any = redis.getInstance

    // @ts-ignore
    public async exec(event: Map<string, any>) {
        // @ts-ignore
        if (event.pathParameters.type === "sendCode") {
            return await this.sendEmailCode(event)
            // @ts-ignore
        } else if (event.pathParameters.type === "verifyCode") {
            return await this.verifyCode(event)
            // @ts-ignore
        } else if (event.pathParameters.type === "verifyEmail") {
            return await this.verifyEmail(event)
            // @ts-ignore
        } else if (event.pathParameters.type === "forgotPassword") {
            return await this.forgotPassword(event)
        }
    }

    private response(code: number, message: string) {
        const header = "HTTP/1.1 200 OK\r\nContent-Type: application/vnd.api+json\r\nETag: W/9bc30459\r\nDate: Wed, 11 Nov 2020 08:56:07 GMT\r\nConnection: keep-alive\r\n\r\n"
        return {
            statusCode: code,
            output: [ header, JSON.stringify({status: message}) ]
        }
    }

    private async sendEmailCode(event: Map<string, string>) {
        try {
            const time = 10
            const now = new Date()
            const exp = moment(now).add(time, "m").toDate()
            const seconds = (exp.getTime() - now.getTime()) / 1000
            await this.rds.open()
            // @ts-ignore
            const codeExist = await this.rds.find("code", null, {match: {key: event.queryStringParameters.to}})
            let r
            if (codeExist.payload.records.length > 0) {
                r = codeExist.payload.records[0].value
            } else {
                r = RandomCode.random(6)
                // @ts-ignore
                const res = await this.rds.create("code", {key: event.queryStringParameters.to, value: r})
                // @ts-ignore
                this.rds.setExpire(`code:${res.payload.records[0].id}`,
                    JSON.stringify(res.payload.records[0]),
                    seconds.toFixed(0))
            }
            const email = new EmailFacade()
            // @ts-ignore
            await email.sendEmail(event.queryStringParameters.to, "", "text/plain", r)
            return this.response(200, "success")
        } catch (e) {
            logger.error(e)
            return this.response(500, "error")
        } finally {
            await this.rds.close()
        }
    }

    private async verifyCode(event: Map<string, string>) {
        try {
            await this.rds.open()
            // @ts-ignore
            const codeExist = await this.rds.find("code", null, {match: {key: event.queryStringParameters.key}})
            if (codeExist.payload.records.length > 0 &&
                // @ts-ignore
                event.queryStringParameters.code === codeExist.payload.records[0].value) {
                return this.response(200, "success")
            } else {
                return this.response(404, "error")
            }
        } catch (e) {
            logger.error(e)
            return this.response(500, "error")
        } finally {
            await this.rds.close()
        }
    }

    private async forgotPassword(event: Map<string, string>) {
        const dbIns = dbFactory.getInstance.getStore(store.Postgres)
        try {
            // @ts-ignore
            const email = JSON.parse(event.body).email
            const result = await dbIns.find("account", null, { match: { email } })
            if (result.payload.records.length === 0) {
                return this.response(404, "error")
            } else {
                const account = [
                    {
                        id: result.payload.records[0].id,
                        // @ts-ignore
                        replace: { password: JSON.parse(event.body).password }
                    }
                ]
                await dbIns.update("account", account)
                return this.response(200, "success")
            }
        } catch (e) {
            logger.error(e)
            return this.response(500, "error")
        } finally {
            await dbIns.disconnect()
        }
    }

    private async verifyEmail(event: Map<string, string>) {
        const dbIns = dbFactory.getInstance.getStore(store.Postgres)
        try {
            // @ts-ignore
            const email = event.queryStringParameters.email
            const result = await dbIns.find("account", null, { match: { email } })
            if (result.payload.records.length === 0) {
                return this.response(404, "error")
            }
            return this.response(200, "success")
        } catch (e) {
            logger.error(e)
            return this.response(500, "error")
        } finally {
            await dbIns.disconnect()
        }
    }
}