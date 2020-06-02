"use strict"
import { prop, Ref, Typegoose } from "typegoose"
import Metadata from "./Metadata"
import IModelBase from "./modelBase"

class Chart extends Typegoose implements IModelBase<Chart> {

    @prop({ ref: Metadata, default: null, required: true })
    public metadata?: Ref<Metadata>

    @prop({ default: null, required: true })
    public styleConfigs: object

    @prop({ default: null, required: true })
    public dataConfigs: object

    @prop({ default: null, required: true })
    public otherConfigs: object

    public getModel() {
        return this.getModelForClass(Chart)
    }
}

export default Chart
