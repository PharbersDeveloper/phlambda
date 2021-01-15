import { ServerResponse } from "http"
import {  Logger } from "phnodelayer"
import { IHandler } from "./IHandler"
export default class UserInfoHandler implements IHandler {

    public async  execute(event: any, response: ServerResponse, pg: any, redis: any) {
        Logger.info(JSON.stringify(event))
    }

}
