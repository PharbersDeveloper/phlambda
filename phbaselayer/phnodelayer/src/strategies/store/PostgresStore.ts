// "use strict"
//
// import { Store } from "./Store"
// import PostgresAdapter from "fortune-postgres"
// import fortune from "fortune"
// import ConfRegistered from "../../config/ConfRegistered"
// import {StoreEnum} from "../../common/enum/StoreEnum"
//
// export default class PostgresStore extends Store {
//     constructor() {
//         super()
//
//         this.name = StoreEnum.Postgres
//         const conf = ConfRegistered.getInstance.getConf("PostgresConf")
//         if (!conf) { throw new Error("PostgresConf Is Null")}
//         const record = new (this.getRecord(conf.entry))()
//         const option = Object.assign(
//             { adapter: [ PostgresAdapter, { connection: conf.getConnect() } ] },
//             record.operations,
//         )
//
//         this.store = fortune(record.model, option)
//     }
//
// }
