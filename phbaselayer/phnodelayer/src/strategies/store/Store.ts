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

    close(): void {
        throw new Error("super not impl close")
    }

    create(type: string, records: any, include?: any, meta?: any): Promise<any> {
        throw new Error("super not impl create")
    }

    delete(type: string, ids: any, include?: any, meta?: any): Promise<any> {
        throw new Error("super not impl delete")
    }

    find(type: string, ids?: any, options?: any, include?: any, meta?: any): Promise<any> {
        throw new Error("super not impl find")
    }

    open(): void {
        throw new Error("super not impl open")
    }

    update(type: string, updates: any, include?: any, meta?: any): Promise<any> {
        throw new Error("super not impl update")
    }
}


