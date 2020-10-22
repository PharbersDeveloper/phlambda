import { DBConf } from './DBConf';
export declare class MysqlConf extends DBConf {
    dbName: string;
    getUrl(): string;
}
