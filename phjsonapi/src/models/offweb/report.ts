"use strict"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Participant from "./participant"

class Report extends Typegoose implements IModelBase<Report> {

    @prop({ default: "", required: true })
    public title: string

    @prop({ default: "", required: true })
    public subTitle: string

    @prop({ default: "", required: true })
    public description: string

    @prop({ default: "", required: true })
    public cover: string

    @prop({ default: 0, required: true })
    public date: number

    @arrayProp({ itemsRef: Participant, required: false })
    public writers?: Array<Ref<Participant>>

    public getModel() {
        return this.getModelForClass(Report)
    }
}

export default Report
