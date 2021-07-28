// "use strict"
// import { DBConf } from "./DBConf"
//
// export default class MongoConf extends DBConf {
//     constructor(
//                 protocols: string,
//                 entry: string,
//                 userName: string,
//                 pwd: string,
//                 host: string,
//                 port: number,
//                 dbName: string,
//                 poolMax: number = 1,
//                 idleTimeoutMillis: number = 1000,
//                 connectionTimeoutMillis: number = 1000,
//                 other: string = "") {
//         super()
//         this.protocols = protocols || "mongodb+srv"
//         this.entry = entry
//         this.username = userName
//         this.pwd = pwd
//         this.host = host
//         this.port = port
//         this.dbName = dbName
//         this.other = other
//         this.poolMax = poolMax
//         this.idleTimeoutMillis = idleTimeoutMillis
//         this.connectionTimeoutMillis = connectionTimeoutMillis
//     }
//     public getUrl(): string {
//         if (this.username.length === 0 || this.pwd.length === 0) {
//             return `${this.protocols}://${this.host}:${this.port}/${this.dbName}${this.other}`
//         }
//         return `${this.protocols}://${this.username}:${this.pwd}@${this.host}:${this.port}/${this.dbName}${this.other}`
//     }
// }
