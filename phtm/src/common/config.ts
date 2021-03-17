abstract class Conf {
    public static url: string
    public static user: string
    public static password: string
    public static entry: string
    public static port: number
    public static db: string
}

// tslint:disable-next-line:max-classes-per-file
export class RedisConf extends Conf {
    public static url: string = "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn"
    public static user: string = ""
    public static password: string = ""
    public static entry: string = "token"
    public static port: number = 6379
    public static db: string = "0"
}

// tslint:disable-next-line:max-classes-per-file
export class MongoConf extends Conf {
    public static url: string = "docdb-2021-03-16-02-36-46.cluster-cngk1jeurmnv.docdb.cn-northwest-1.amazonaws.com.cn"
    public static user: string = "pharbers"
    public static password: string = "Abcde196125"
    public static entry: string = "ntm"
    public static port: number = 27017
    public static db: string = "pharbers-ntm-client"
    public static other: string = "?ssl=true&ssl_ca_certs=rds-combined-ca-cn-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
}
