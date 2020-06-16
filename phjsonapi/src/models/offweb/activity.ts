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
    public title: string = ""

    @JsonProperty("subTitle", String)
    @prop({ default: "", required: false })
    public subTitle: string = ""

    @JsonProperty("startDate", Number)
    @prop({ default: 0, required: true })
    public startDate: number = 0

    @JsonProperty("endDate", Number)
    @prop({ default: 0, required: false })
    public endDate: number = 0

    @JsonProperty("location", String)
    @prop({ default: "", required: true })
    public location: string = ""

    @JsonProperty("city", String)
    @prop({ default: "", required: true })
    public city: string = ""

    @JsonProperty("logo", String)
    @prop({ default: "", required: false })
    public logo: string = ""

    @JsonProperty("logoOnTime", String)
    @prop({ default: "", required: false })
    public logoOnTime: string = ""

    @JsonProperty("type", String)
    @prop({ default: "", required: true })
    public type: string = ""
    
    @JsonProperty("contentTitle", String)
    @prop({ default: "", required: true })
    public contentTitle: string = ""

    @JsonProperty("contentDesc", String)
    @prop({ default: "", required: true })
    public contentDesc: string = ""

    @JsonProperty("gallery", String)
    @prop({ default: [], required: false })
    public gallery: string[] = []

    @arrayProp({ itemsRef: Report, required: false })
    public attachments?: Array<Ref<Report>> = []

    @arrayProp({ itemsRef: Zone, required: false })
    public agendas?: Array<Ref<Zone>> = []

    @arrayProp({ itemsRef: Cooperation, required: false })
    public partners?: Array<Ref<Cooperation>>

    @JsonProperty("language", Number)
    @prop({ default: "", required: true })
    public language: number = 1

    public getModel() {
        return this.getModelForClass(Activity)
    }
}

export default Activity
