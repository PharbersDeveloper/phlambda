"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Report from "./report"
import Zone from "./zone"
import Cooperation from "./cooperation"

@JsonObject("Activity")
class Activity extends Typegoose implements IModelBase<Activity> {

    @JsonProperty("title", String)
    @prop({ default: "", required: true })
    public title: string

    @JsonProperty("subTitle", String)
    @prop({ default: "", required: true })
    public subTitle: string

    @JsonProperty("startDate", Number)
    @prop({ default: 0, required: true })
    public startDate: number

    @JsonProperty("endDate", Number)
    @prop({ default: 0, required: true })
    public endDate: number

    @JsonProperty("location", String)
    @prop({ default: "", required: true })
    public location: string

    @JsonProperty("city", String)
    @prop({ default: "", required: true })
    public city: string

    @JsonProperty("logo", String)
    @prop({ default: "", required: true })
    public logo: string

    @JsonProperty("logoOnTime", String)
    @prop({ default: "", required: true })
    public logoOnTime: string

    @JsonProperty("type", String)
    @prop({ default: "", required: true })
    public type: string
    
    @JsonProperty("contentTitle", String)
    @prop({ default: "", required: true })
    public contentTitle: string

    @JsonProperty("contentDesc", String)
    @prop({ default: "", required: true })
    public contentDesc: string

    @JsonProperty("gallery", String)
    @prop({ default: [], required: true })
    public gallery: string[]

    @JsonProperty("attachments", Array)
    @arrayProp({ itemsRef: Report, required: false })
    public attachments?: Array<Ref<Report>>

    @JsonProperty("agendes", Array)
    @arrayProp({ itemsRef: Zone, required: false })
    public agendes?: Array<Ref<Zone>>

    @JsonProperty("partners", Array)
    @arrayProp({ itemsRef: Cooperation, required: false })
    public partners?: Array<Ref<Cooperation>>

    public getModel() {
        return this.getModelForClass(Activity)
    }
}

export default Activity
