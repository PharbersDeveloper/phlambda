"use strict"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Participant from "./participant"

class Event extends Typegoose implements IModelBase<Event> {

    @prop({ default: "", required: true })
    public title: string

    @prop({ default: "", required: true })
    public subTitle: string

    @prop({ default: "", required: true })
    public description: string

    @prop({ default: 0, required: true })
    public startDate: number

    @prop({ default: 0, required: true })
    public endDate: number

    @arrayProp({ itemsRef: Participant, required: true })
    public speakers?: Array<Ref<Participant>>

    public getModel() {
        return this.getModelForClass(Event)
    }
}

export default Event
