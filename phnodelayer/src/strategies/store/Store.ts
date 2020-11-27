"use strict"

import * as fs from "fs"

export class Store {
    store: any
    protected getRecord(name: string): any {
        let base = process.cwd()
        try {
            fs.statSync(`${base}/dist/models`)
            return require(`${base}/dist/models/${name}.js`).default
        } catch (e) {
            return require(`${base}/lib/models/${name}.js`).default
        }
    }
}

export interface IStore {
    open(): void
    close(): void
    create(type: string, records: any, include: any, meta: any): Promise<any>
    find(type: string, ids: any, options: any, include: any, meta: any): Promise<any>
    update(type: string, updates: any, include: any, meta: any): Promise<any>
    delete(type: string, ids: any, include: any, meta: any): Promise<any>
}
