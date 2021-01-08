"use strict"
// import MongoConf from "./MongoConf"
import MysqlConf from "./MysqlConf"
import PostgresConf from "./PostgresConf"
import RedisConf from "./RedisConf"
import ConfRegistered from "./ConfRegistered"

export default class ServerConf {
    public project: string = undefined

    public postgres: PostgresConf = undefined

    // public mongo: MongoConf = undefined

    public mysql: MysqlConf = undefined

    public redis: RedisConf = undefined

    // constructor(project: string, { pg, mysql, redis }:
    //     { pg?: PostgresConf, mysql?: MysqlConf, redis?: RedisConf } = {}) {
    //         this.project = project
    //         this.postgres = pg
    //         this.mysql = mysql
    //         this.redis = redis
    // }
    constructor(project: string) {
        this.project = project
        this.postgres = ConfRegistered.getInstance.getConf("PostgresConf")
        this.mysql = ConfRegistered.getInstance.getConf("MysqlConf")
        this.redis = ConfRegistered.getInstance.getConf("RedisConf")
    }
}
