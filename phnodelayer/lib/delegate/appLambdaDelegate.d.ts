/// <reference types="node" />
import { ServerResponse } from "http";
export default class AppLambdaDelegate {
    /**
     * custom 下的包为编译文件 普通 import 会找不到描述文件，暂时解决方案为require导入
     */
    private fortuneHTTP;
    private jsonApiSerializer;
    private conf;
    store: any;
    listener: any;
    isFirstInit: boolean;
    prepare(name?: string): Promise<void>;
    cleanUp(): Promise<void>;
    exec(event: Map<string, any>): Promise<ServerResponse>;
}
