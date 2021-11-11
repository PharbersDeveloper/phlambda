import AWSRequest from "../common/request/AWSRequest"
import IStore from "../common/store/IStore"
import { ServerResponse } from "http"
import { StoreEnum } from "../common/enum/StoreEnum"
import StoreRegister from "../common/factory/StoreRegister"
import PhStore from "../common/store/PhStore"


export default class JSONAPIDelegate {
    /**
     * custom 下的包为编译文件 普通 import 会找不到描述文件，暂时解决方案为require导入
     */
    private fortuneHTTP = require("../../custom/fortune-http")
    private jsonApiSerializer = require("../../custom/fortune-json-api")
    private listener: any
    private store: IStore

    public isFirstInit = true

    public async prepare(jsonApiDB: StoreEnum) {
        this.store = (StoreRegister.getInstance.getData(jsonApiDB) as PhStore)
        this.isFirstInit = false
        this.listener = this.fortuneHTTP(this.store.getStore(), {
            serializers: [[this.jsonApiSerializer]]
        })
        // await this.store.open()
    }

    public async exec(event: any) {
        if(!event.body) {
            event.body = ""
        }
        const paths = event.path.split("/")
        const projectName = paths[0] === "" ? paths[1] : paths[0]
        const request = new AWSRequest(event, projectName)
        const response = new ServerResponse(request)
        const buffer = Buffer.from(event.body)
        // @ts-ignore
        request._readableState.buffer = buffer
        await this.listener(request, response, buffer)
        // await this.store.close()
        return response
    }

}
