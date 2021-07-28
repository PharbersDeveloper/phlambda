// import { ServerResponse } from "http"
// import StoreFactory from "../strategies/store/StoreFactory"
// import AWSReq from "../strategies/AwsRequest"
// import ConfRegistered from "../config/ConfRegistered"
// import { Store } from "../strategies/store/Store"
//
// export default class AppLambdaDelegate {
//     /**
//      * custom 下的包为编译文件 普通 import 会找不到描述文件，暂时解决方案为require导入
//      */
//     private fortuneHTTP = require("../../custom/fortune-http")
//     private jsonApiSerializer = require("../../custom/fortune-json-api")
//     private storeIns: Store
//
//     public listener: any
//     // public isFirstInit = true
//
//     public prepare(storeIns: Store) {
//         this.storeIns = storeIns
//         // this.isFirstInit = false
//         this.listener = this.fortuneHTTP(storeIns.store, {
//             serializers: [[this.jsonApiSerializer]],
//         })
//     }
//
//     public async exec(event: Map<string, any>) {
//         if (!event["body"]) {
//             event["body"] = ""
//         }
//         const conf = ConfRegistered.getInstance.getConf(`${this.storeIns["name"]}Conf`)
//         if (!conf) {throw new Error("Config Is Null")}
//         const req = new AWSReq(event, conf.entry)
//         const response = new ServerResponse(req)
//         const buffer = Buffer.from(event["body"])
//         // @ts-ignore
//         req._readableState.buffer = buffer
//         await this.listener(req, response, buffer)
//         return response
//     }
// }
