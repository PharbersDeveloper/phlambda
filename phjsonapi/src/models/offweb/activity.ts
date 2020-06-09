"use strict"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Report from "./report"
import Zone from "./zone"

class Activity extends Typegoose implements IModelBase<Activity> {

    @prop({ default: "", required: true })
    public title: string

    @prop({ default: "", required: true })
    public subTitle: string

    @prop({ default: 0, required: true })
    public startDate: number

    @prop({ default: 0, required: true })
    public endDate: number

    @prop({ default: "", required: true })
    public location: string

    @prop({ default: "", required: true })
    public city: string

    @prop({ default: "", required: true })
    public logo: string

    @prop({ default: "", required: true })
    public logoOnTime: string

    @prop({ default: "", required: true })
    public type: string

    @prop({ default: "", required: true })
    public contentTitle: string

    @prop({ default: "", required: true })
    public contentDesc: string

    @arrayProp({ itemsRef: Report, required: false })
    public attachments?: Array<Ref<Report>>

    @arrayProp({ itemsRef: Zone, required: false })
    public agendes?: Array<Ref<Zone>>

    public getModel() {
        return this.getModelForClass(Activity)
    }
}

export default Activity
