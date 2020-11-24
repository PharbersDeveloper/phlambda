"use strict"
import MongoConf from "./MongoConf"
import MysqlConf from "./MysqlConf"
import PostgresConf from "./PostgresConf"
import RedisConf from "./RedisConf"

export default class ServerConf {
    public project: string = undefined

    public postgres: PostgresConf = undefined

    public mongo: MongoConf = undefined

    public mysql: MysqlConf = undefined

    public redis: RedisConf = undefined

    constructor(project: string, { pg, mongo , mysql, redis }:
        { pg?: PostgresConf, mongo?: MongoConf, mysql?: MysqlConf, redis?: RedisConf } = {}) {
            this.project = project
            this.postgres = pg
            this.mongo = mongo
            this.mysql = mysql
            this.redis = redis
    }
}
