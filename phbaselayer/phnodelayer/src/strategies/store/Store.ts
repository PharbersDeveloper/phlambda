"use strict"

import * as fs from "fs"


export interface IStore {
    open(): void
    close(): void
    create(type: string, records: any, include?: any, meta?: any): Promise<any>
    find(type: string, ids?: any, options?: any, include?: any, meta?: any): Promise<any>
    update(type: string, updates: any, include?: any, meta?: any): Promise<any>
    delete(type: string, ids: any, include?: any, meta?: any): Promise<any>
}

export class Store implements IStore {
    store: any
    name: string
    protected getRecord(name: string): any {
        let base = process.cwd()
        try {
            fs.statSync(`${base}/dist/models`)
            return require(`${base}/dist/models/${name}.js`).default
        } catch (e) {
            return require(`${base}/lib/models/${name}.js`).default
        }
    }

    async open() {
        await this.store.connect()
    }

    async close() {
        await this.store.disconnect()
    }

    async create(type: string, records: any, include?: any, meta?: any): Promise<any> {
        return await this.store.create(type, records, include, meta)
    }

    async delete(type: string, ids: any, include?: any, meta?: any): Promise<any> {
        return await this.store.delete(type, ids, include, meta)
    }

    async find(type: string, ids?: any, options?: any, include?: any, meta?: any): Promise<any> {
        return await this.store.find(type, ids, options, include, meta)
    }

    async update(type: string, updates: any, include?: any, meta?: any): Promise<any> {
        return await this.store.update(type, updates, include, meta)
    }

}


