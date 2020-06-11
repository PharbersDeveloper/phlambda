"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Participant from "./participant"
import Event from "./event"

@JsonObject("Zone")
class Zone extends Typegoose implements IModelBase<Zone> {

    @JsonProperty("title", String)
    @prop({ default: "", required: true })
    public title: string

    @JsonProperty("subTitle", String)
    @prop({ default: "", required: true })
    public subTitle: string

    @JsonProperty("description", String)
    @prop({ default: "", required: true })
    public description: string

    @JsonProperty("startDate", Number)
    @prop({ default: 0, required: true })
    public startDate: number

    @JsonProperty("endDate", Number)
    @prop({ default: 0, required: true })
    public endDate: number

    @JsonProperty("hosts", Array)
    @arrayProp({ itemsRef: Participant, required: true })
    public hosts?: Array<Ref<Participant>>

    @JsonProperty("agendas", Array)
    @arrayProp({ itemsRef: Event, required: true })
    public agendas?: Array<Ref<Event>>

    @JsonProperty("id", Number)
    public id: number
    

    public getModel() {
        return this.getModelForClass(Zone)
    }
}

export default Zone
