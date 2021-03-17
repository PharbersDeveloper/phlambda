abstract class Conf {
     static url: string
     static user: string
     static password: string
     static entry: string
     static port: number
     static db: string
}

// tslint:disable-next-line:max-classes-per-file
export class RedisConf extends Conf {
     static url: string = "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn"
     static user: string = ""
     static password: string = ""
     static entry: string = "token"
     static port: number = 6379
     static db: string = "0"
}

// tslint:disable-next-line:max-classes-per-file
export class PostgresqlConf extends Conf {
     static url: string = "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn"
     // static url: string = "localhost"
     static user: string = "pharbers"
     static password: string = "Abcde196125"
     static entry: string = "ntm"
     static port: number = 5432
     static db: string = "pharbers-ntm-client"
     // static db: string = "phntm"
}
