import BaseModel from "../models/BaseModel"

export default interface IStore extends BaseModel {
    open(): void
    close(): void
    find(type: string, ids?: string|string[], options?: any, include?: any, meta?: any): Promise<any>
    create(type: string, records: any, include?: any, meta?: any): Promise<any>
    update(type: string, updates: any, include?: any, meta?: any): Promise<any>
    delete(type: string, ids: string|string[], include?: any, meta?: any): Promise<any>
    getStore(): any
}