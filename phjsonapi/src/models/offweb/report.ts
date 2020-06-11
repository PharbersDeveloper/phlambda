"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Participant from "./participant"

@JsonObject("Report")
class Report extends Typegoose implements IModelBase<Report> {
    @JsonProperty("title", String)
    @prop({ default: "", required: true })
    public title: string

    @JsonProperty("subTitle", String)
    @prop({ default: "", required: true })
    public subTitle: string

    @JsonProperty("description", String)
    @prop({ default: "", required: true })
    public description: string

    @JsonProperty("cover", String)
    @prop({ default: "", required: true })
    public cover: string

    @JsonProperty("date", Number)
    @prop({ default: 0, required: true })
    public date: number

    @JsonProperty("writers", Array)
    @arrayProp({ itemsRef: Participant, required: false })
    public writers?: Array<Ref<Participant>>

    public getModel() {
        return this.getModelForClass(Report)
    }
}

export default Report
