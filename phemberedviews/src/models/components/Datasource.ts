"use strict"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"

class Datasource extends Typegoose implements IModelBase<Datasource> {

    @prop({default: "", required: true})
    public target: string

    @prop({default: "", required: true})
    public category: string

    @prop({default: "", required: true})
    public query: string

    public content: string

    public getModel() {
        return this.getModelForClass(Datasource)
    }
}

export default Datasource
