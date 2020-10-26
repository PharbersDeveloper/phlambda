import { ServerConf } from '../configFactory/ServerConf';
export declare class InitServerConf {
    private static conf;
    private static init;
    static get getConf(): ServerConf;
}
