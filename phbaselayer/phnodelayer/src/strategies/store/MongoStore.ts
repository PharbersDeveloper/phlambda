// "use strict"
//
// import { Store } from "./Store"
// import fortune from "fortune"
// import ConfRegistered from "../../config/ConfRegistered"
// import MongodbAdapter from "fortune-mongodb"
// import {StoreEnum} from "../../common/enum/StoreEnum"
//
// export default class MongoStore extends Store {
//     constructor() {
//         super()
//         let BSON = require('bson')
//         this.name = StoreEnum.Mongo
//         const conf = ConfRegistered.getInstance.getConf("MongoConf")
//         if (!conf) { throw new Error("MongoConf Is Null")}
//         const record = new (this.getRecord(conf.entry))()
//         const option = Object.assign(
//             { adapter: [ MongodbAdapter,
//                     {
//                         url: conf.getUrl(),
//                         generateId: () => new BSON.ObjectId()
//                     } ] },
//             record.operations,
//         )
//
//         this.store = fortune(record.model, option)
//     }
//
// }
