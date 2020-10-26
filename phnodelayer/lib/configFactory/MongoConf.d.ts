import { DBConf } from './DBConf';
export declare class MongoConf extends DBConf {
    coll: string;
    authSource: string;
    auth: boolean;
    other: string;
    getUrl(): string;
}
