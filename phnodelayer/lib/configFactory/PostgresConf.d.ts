import { DBConf } from './DBConf';
export declare class PostgresConf extends DBConf {
    dbName: string;
    getUrl(): string;
}
