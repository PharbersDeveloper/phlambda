"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import Image from "./image"
import IModelBase from "./modelBase"
import Participant from "./participant"

@JsonObject("Report")
class Report extends Typegoose implements IModelBase<Report> {
    @JsonProperty("title", String)
    @prop({ default: "", required: true })
    public title: string = ""

    @JsonProperty("subTitle", String)
    @prop({ default: "", required: false })
    public subTitle: string = ""

    @JsonProperty("description", String)
    @prop({ default: "", required: true })
    public description: string = ""

    @prop({  ref: Image, default: [], required: false })
    public cover?: Ref<Image>

    @JsonProperty("date", Number)
    @prop({ default: 0, required: true })
    public date: number = 0

    @JsonProperty("writers", Array)
    @arrayProp({ itemsRef: Participant, required: false })
    public writers?: Array<Ref<Participant>>

    @JsonProperty("id", Number)
    public jid: number

    @JsonProperty("language", Number)
    @prop({ default: "", required: true })
    public language: number = 1

    public getModel() {
        return this.getModelForClass(Report)
    }
}

export default Report
