"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"
import Participant from "./Participant"

@JsonObject("Event")
class Event extends Typegoose implements IModelBase<Event> {

    @JsonProperty("title", String)
    @prop({ default: "", required: true })
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

    @arrayProp({ itemsRef: Participant, required: false })
    public speakers?: Array<Ref<Participant>> = []

    @JsonProperty("id", Number)
    public jid: number

    @JsonProperty("language", Number)
    @prop({ default: "", required: true })
    public language: number = 1

    public getModel() {
        return this.getModelForClass(Event)
    }
}

export default Event
