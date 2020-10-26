/// <reference types="node" />
import { StoreEnum } from "./common/StoreEnum";
import DBFactory from "./factory/DBFactory";
import Redis from "./strategies/store/RedisStore";
export declare const logger: import("log4js").Logger;
export declare const store: typeof StoreEnum;
export declare const dbFactory: typeof DBFactory;
export declare const redis: typeof Redis;
export declare const Main: (event: Map<string, any>, db?: any) => Promise<import("http").ServerResponse>;
