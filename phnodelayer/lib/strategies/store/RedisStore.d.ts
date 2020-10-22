export interface IStore {
    open(): void;
    close(): void;
}
export interface IRedisStore extends IStore {
    setExpire(key: string, value: any, expire: number): any;
}
export default class RedisStore implements IRedisStore {
    private static instance;
    private readonly store;
    constructor();
    static get getInstance(): RedisStore;
    setExpire(key: string, value: any, expire: number): Promise<void>;
    open(): Promise<void>;
    close(): Promise<void>;
}
