import { ServerResponse } from "http"
import ServerConf from "../config/ServerConf"
import StoreFactory from "../strategies/store/StoreFactory"
import AWSReq from "../strategies/AwsRequest"

export default class AppLambdaDelegate {
    /**
     * custom 下的包为编译文件 普通 import 会找不到描述文件，暂时解决方案为require导入
     */
    private fortuneHTTP = require("../../custom/fortune-http")
    private jsonApiSerializer = require("../../custom/fortune-json-api")
    private conf: ServerConf = null
    private key: string = ""

    public store: any
    public listener: any
    public isFirstInit = true

    public prepare(conf: ServerConf, name: string) {
        this.key = name
        this.conf = conf
        const ins = StoreFactory.getInstance(conf).get(name)
        this.store = ins
        this.isFirstInit = false
        this.listener = this.fortuneHTTP(ins.store, {
            serializers: [[this.jsonApiSerializer]],
        })
    }

    public async exec(event: Map<string, any>) {
        if (!event["body"]) {
            event["body"] = ""
        }
        const req = new AWSReq(event, this.conf[this.key]["entry"])
        const response = new ServerResponse(req)
        const buffer = Buffer.from(event["body"])
        // @ts-ignore
        req._readableState.buffer = buffer
        await this.listener(req, response, buffer)
        return response
    }
}
