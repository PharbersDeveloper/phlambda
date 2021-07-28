// "use strict"
//
// import PostgresStore from "./PostgresStore"
// import MongoStore from "./MongoStore"
// import RedisStore from "./RedisStore"
// import { StoreEnum } from "../../common/enum/StoreEnum"
// import ConfRegistered from "../../config/ConfRegistered"
// import {IStore, Store} from "./Store"
//
// export default class StoreFactory {
//     private static instance: StoreFactory = null
//     private typeAnalyzerMapping: Map<string, Store> = new Map()
//
//     private constructor() {
//         for (const item in StoreEnum ) {
//             if (StoreEnum.hasOwnProperty(item) && ConfRegistered.getInstance.getConf(`${item}Conf`)) {
//                 switch (item.toLowerCase()) {
//                     case StoreEnum.Postgres:
//                         this.typeAnalyzerMapping.set(StoreEnum.Postgres, new PostgresStore())
//                         break
//                     case StoreEnum.Mongo:
//                         this.typeAnalyzerMapping.set(StoreEnum.Mongo, new MongoStore())
//                         break
//                     case StoreEnum.Redis:
//                         this.typeAnalyzerMapping.set(StoreEnum.Redis, new RedisStore())
//                         break
//                 }
//             }
//         }
//     }
//
//     public static get getInstance() {
//         if (StoreFactory.instance == null) {
//             StoreFactory.instance = new StoreFactory()
//         }
//         return StoreFactory.instance
//     }
//
//     public get(name?: string): RedisStore | Store | IStore{
//         if (name === undefined || name === null || name.length === 0) {
//             if (this.typeAnalyzerMapping.size === 1) {
//                 return [...this.typeAnalyzerMapping.values()][0]
//             } else {
//                 throw new Error(
//                     `存在多个Store, 请使用 get(参数) 获取对应Store，包含参数：${[
//                         ...this.typeAnalyzerMapping.keys(),
//                     ]}`,
//                 )
//             }
//         }
//         return this.typeAnalyzerMapping.get(name)
//     }
// }
