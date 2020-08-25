"use strict"

import fortune from "fortune"
import PostgresAdapter from "fortune-postgres"
import { ServerConf } from "../configFactory/serverConf"
import { SingletonInitConf } from "../configFactory/singletonConf"
import { IStoreInterface } from "./StoreFactory"

export class PostgresFactory implements IStoreInterface {
    private conf: ServerConf
    constructor() {
        this.conf = new SingletonInitConf().getConf()
    }

    public getStore(): any {
        const url = this.conf.postgres.getUrl()
        const filename = `${process.cwd()}/dist/models/${this.conf.project}.js`
        const record = require(filename).default
        const adapter = [PostgresAdapter, {url}]
        return fortune(record, {adapter})
    }
}
