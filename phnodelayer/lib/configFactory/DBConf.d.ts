export declare abstract class DBConf {
    algorithm: string;
    host: string;
    port: number;
    dao: string;
    username: string;
    pwd: string;
    abstract getUrl(): string;
}
