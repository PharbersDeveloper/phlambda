"use strict"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"

class Cooperation extends Typegoose implements IModelBase<Cooperation> {

    @prop({ default: "", required: true })
    public name: string

    @prop({ default: "", required: true })
    public type: string

    @prop({ default: "", required: true })
    public logo: string

    public getModel() {
        return this.getModelForClass(Cooperation)
    }
}

export default Cooperation
