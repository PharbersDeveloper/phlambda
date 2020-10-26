import { DBConf } from './DBConf';
export declare class RedisConf extends DBConf {
    db: string;
    getUrl(): string;
}
