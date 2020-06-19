"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import Cooperation from "./Cooperation"
import Image from "./Image"
import IModelBase from "./modelBase"
import Report from "./Report"
import Zone from "./Zone"

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

    @prop({ ref: Image, required: false })
    public logo?: Ref<Image>

    @prop({ ref: Image, required: false })
    public logoOnTime?: Ref<Image>

    @JsonProperty("activityType", String)
    @prop({ default: "", required: true })
    public activityType: string = ""

    @JsonProperty("contentTitle", String)
    @prop({ default: "", required: true })
    public contentTitle: string = ""

    @JsonProperty("contentDesc", String)
    @prop({ default: "", required: true })
    public contentDesc: string = ""

    @arrayProp({ itemsRef: Image, default: [], required: false })
    public gallery?: Array<Ref<Image>> = []

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
