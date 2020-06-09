"use strict"
import { prop, Ref, Typegoose } from "typegoose"
import IModelBase from "./modelBase"

class Participant extends Typegoose implements IModelBase<Participant> {

    @prop({ default: "", required: true })
    public name: string

    @prop({ default: "", required: true })
    public title: string

    @prop({ default: "", required: true })
    public occupation: string

    @prop({ default: "", required: true })
    public avatar: string

    public getModel() {
        return this.getModelForClass(Participant)
    }
}

export default Participant
