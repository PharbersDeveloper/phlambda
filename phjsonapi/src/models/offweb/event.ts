"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Participant from "./participant"

@JsonObject("Event")
class Event extends Typegoose implements IModelBase<Event> {

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

    @JsonProperty("speakers", Array)
    @arrayProp({ itemsRef: Participant, required: true })
    public speakers?: Array<Ref<Participant>>
    
    @JsonProperty("id", Number)
    public id: number

    public getModel() {
        return this.getModelForClass(Event)
    }
}

export default Event
