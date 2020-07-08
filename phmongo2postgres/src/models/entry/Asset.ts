"use strict"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import DataSet from "./DataSet"
import DbSource from "./DbSource"
import File from "./File"
import Mart from "./Mart"
import IModelBase from "./modelBase"

class Asset extends Typegoose implements IModelBase<Asset> {

    // @prop({ default: "", required: true })
    // public traceId: string

    @prop({default: "", required: true})
    public name: string

    @prop({default: "", required: false})
    public description: string

    @prop({default: "auto robot", required: true})
    public owner: string

    @prop({default: "", required: true})
    public accessibility: string

    @prop({default: "0.0.0", required: true})
    public version: string

    @prop({default: true, required: true})
    public isNewVersion: boolean

    @prop({ default: "file", required: true } )
    public dataType: string // candidate: database, file, stream, application, mart, cube

    @prop({ ref: File, required: false } )
    public file?: Ref<File>

    @prop({ ref: DbSource, required: false } )
    public dbs?: Ref<DbSource>

    @arrayProp({ itemsRef: DataSet, required: false } )
    public dfs: Array<Ref<DataSet>>

    @prop({ ref: Mart, required: false } )
    public mart?: Ref<Mart>

    @arrayProp({ items: String, default: [], required: false } )
    public martTags: string[]

    @arrayProp({ items: String, default: [], required: true } )
    public providers: string[]

    @arrayProp({ items: String, default: [], required: true } )
    public markets: string[]

    @arrayProp({ items: String, default: [], required: true } )
    public molecules: string[]

    @arrayProp({ items: String, default: [], required: true } )
    public dataCover: string[]

    @arrayProp({ items: String, default: [], required: true } )
    public geoCover: string[]

    @arrayProp({ items: String, default: [], required: true } )
    public labels: string[]

    @prop({ default: 0, required: false })
    public createTime: number

    public getModel() {
        return this.getModelForClass(Asset)
    }
}

export default Asset
