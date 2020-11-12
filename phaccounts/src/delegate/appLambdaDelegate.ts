import lambda from "aws-sdk/clients/lambda"
import moment from "moment"
import { logger, redis } from "phnodelayer"
import EmailFacade from "../facade/emailFacade"
import SQSFacade from "../facade/sqsFacade"
import RandomCode from "../utils/randomCode"

export default class AppLambdaDelegate  {
    private rds: any = redis.getInstance
    // @ts-ignore
    public async exec(event: Map<string, any>) {
        // @ts-ignore
        if (event.pathParameters.type === "sendCode") {
            return await this.sendEmailCode(event)
            // @ts-ignore
        } else if (event.pathParameters.type === "verifyCode") {
            return await this.verifyCode(event)
        }
    }

    private async sendEmailCode(event: Map<string, string>) {
        const response = {}
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
            // @ts-ignore
            response.statusCode = 200
            // @ts-ignore
            response.output = [
                "HTTP/1.1 200 OK\r\nContent-Type: application/vnd.api+json\r\nETag: W/9bc30459\r\nDate: Wed, 11 Nov 2020 08:56:07 GMT\r\nConnection: keep-alive\r\n\r\n",
                "success"
            ]
        } catch (e) {
            // @ts-ignore
            response.statusCode = 500
            // @ts-ignore
            response.output = [
                "HTTP/1.1 200 OK\r\nContent-Type: application/vnd.api+json\r\nETag: W/9bc30459\r\nDate: Wed, 11 Nov 2020 08:56:07 GMT\r\nConnection: keep-alive\r\n\r\n",
                "error"
            ]
            throw e
        } finally {
            await this.rds.close()
        }
        return response
    }

    private async verifyCode(event: Map<string, string>) {
        try {
            await this.rds.open()
            const response = {}
            // @ts-ignore
            const codeExist = await this.rds.find("code", null, {match: {key: event.queryStringParameters.key}})
            if (codeExist.payload.records.length > 0 &&
                // @ts-ignore
                event.queryStringParameters.code === codeExist.payload.records[0].value) {
                // @ts-ignore
                response.statusCode = 200
                // @ts-ignore
                response.output = [
                    "HTTP/1.1 200 OK\r\nContent-Type: application/vnd.api+json\r\nETag: W/9bc30459\r\nDate: Wed, 11 Nov 2020 08:56:07 GMT\r\nConnection: keep-alive\r\n\r\n",
                    "success"
                ]
            } else {
                // @ts-ignore
                response.statusCode = 404
                // @ts-ignore
                response.output = [
                    "HTTP/1.1 200 OK\r\nContent-Type: application/vnd.api+json\r\nETag: W/9bc30459\r\nDate: Wed, 11 Nov 2020 08:56:07 GMT\r\nConnection: keep-alive\r\n\r\n",
                    "error"
                ]
            }
            return response
        } catch (e) {
            throw e
        } finally {
            await this.rds.close()
        }
    }
}
