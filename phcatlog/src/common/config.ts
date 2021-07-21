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