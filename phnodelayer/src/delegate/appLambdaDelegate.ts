import { ServerResponse } from "http"
import { Adapter } from "../common/Adapter"
import { InitServerConf } from "../common/InitServerConf"
import { ServerConf } from "../configFactory/ServerConf"
import DBFactory from "../factory/DBFactory"
import AWSReq from "../strategies/AwsRequest"

export default class AppLambdaDelegate {
    /**
     * custom 下的包为编译文件 普通 import 会找不到描述文件，暂时解决方案为require导入
     */
    private fortuneHTTP = require("../../custom/fortune-http")
    private jsonApiSerializer = require("../../custom/fortune-json-api")
    private conf: ServerConf = InitServerConf.getConf

    public store: any
    public listener: any
    public isFirstInit = true

    public async prepare(name?: string) {
        // tslint:disable-next-line:no-unused-expression
        Adapter.init
        this.store = DBFactory.getInstance.getStore(name)
        await this.store.connect()
        this.isFirstInit = false
        this.listener = this.fortuneHTTP(this.store, {
            serializers: [[this.jsonApiSerializer]],
        })
    }

    public async cleanUp() {
        await this.store.disconnect()
    }

    public async exec(event: Map<string, any>) {
        if (!event["body"]) {
            event["body"] = ""
        }
        const req = new AWSReq(event, this.conf.project)
        const response = new ServerResponse(req)
        const buffer = Buffer.from(event["body"])
        // @ts-ignore
        req._readableState.buffer = buffer
        await this.listener(req, response, buffer)
        return response
    }
}
