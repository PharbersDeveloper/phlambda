"use strict"
import { prop, Ref, Typegoose } from "typegoose"
import IModelBase from "./modelBase"

class Metadata extends Typegoose implements IModelBase<Metadata> {

    @prop({ default: "", required: true })
    public type?: string

    @prop({ default: true, required: true })
    public canSave?: boolean

    @prop({ default: true, required: true })
    public canEdit?: boolean

    @prop({ default: "", required: true })
    public url: string

    @prop({ default: "", required: true })
    public expires?: string

    @prop({ default: "", required: true })
    public created?: string

    @prop({ default: "", required: true })
    public updated: string

    @prop({ default: 0, required: true })
    public version: number

    @prop({ default: "", required: true })
    public description: string

    public getModel() {
        return this.getModelForClass(Metadata)
    }
}

export default Metadata
