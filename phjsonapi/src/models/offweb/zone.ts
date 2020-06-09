"use strict"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Participant from "./participant"

class Zone extends Typegoose implements IModelBase<Zone> {

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
    public hosts?: Array<Ref<Participant>>

    public getModel() {
        return this.getModelForClass(Zone)
    }
}

export default Zone
