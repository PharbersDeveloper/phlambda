export interface IPhConf {
    url: string
    user: string
    password: string
    entry: string
    port: number
    db: string
}

export const MS_IN_S = 1_000

export const RedisConf: IPhConf = {
    // url: "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn",
    url: "127.0.0.1",
    user: "",
    password: "",
    entry: "db/token",
    port: 6379,
    db: "0"
}

export const PostgresConf: IPhConf = {
    url: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
    user: "pharbers",
    password: "Abcde196125",
    entry: "db/oauth",
    port: 5432,
    db: "phcommon"
}

export const AccountUri = {
    uri: "http://accounts.pharbers.com/welcome"
}
