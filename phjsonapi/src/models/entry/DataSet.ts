"use strict"
import * as mongoose from "mongoose"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import Job from "./Job"
import IModelBase from "./modelBase"

class DataSet extends Typegoose implements IModelBase<DataSet> {

    @arrayProp({ items: String, default: [], required: false } )
    public colNames?: string[]

    // @prop({ required: false} )
    // public _id?: any

    @prop({ default: 0, required: false} )
    public length?: number

    @prop({ default: "", required: false } )
    public url?: string

    @prop({ default: "", required: false } )
    public description?: string

    @prop({ default: "", required: false } )
    public tabName?: string

    @prop({ default: "", required: false } )
    public status?: string

    @arrayProp({ itemsRef: DataSet, required: false } )
    public parent?: Array<Ref<DataSet>>

    @prop({ ref: Job, required: false })
    public job?: Ref<Job>

    public getModel() {
        return this.getModelForClass(DataSet)
    }
}

export default DataSet
