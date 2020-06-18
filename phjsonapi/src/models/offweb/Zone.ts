"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import Event from "./Event"
import IModelBase from "./modelBase"
import Participant from "./Participant"

@JsonObject("Zone")
class Zone extends Typegoose implements IModelBase<Zone> {

    @JsonProperty("title", String)
    @prop({ default: "", required: false })
    public title: string = ""

    @JsonProperty("subTitle", String)
    @prop({ default: "", required: false })
    public subTitle: string = ""

    @JsonProperty("description", String)
    @prop({ default: "", required: false })
    public description: string = ""

    @JsonProperty("startDate", Number)
    @prop({ default: 0, required: false })
    public startDate: number = 0

    @JsonProperty("endDate", Number)
    @prop({ default: 0, required: false })
    public endDate: number = 0

    @JsonProperty("hosts", Array)
    @arrayProp({ itemsRef: Participant, required: false })
    public hosts?: Array<Ref<Participant>>

    @arrayProp({ itemsRef: Event, required: true })
    public agendas?: Array<Ref<Event>> = []

    @JsonProperty("id", Number)
    public jid: number

    @JsonProperty("language", Number)
    @prop({ default: "", required: true })
    public language: number = 1

    public getModel() {
        return this.getModelForClass(Zone)
    }
}

export default Zone