"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"

@JsonObject("Cooperation")
class Cooperation extends Typegoose implements IModelBase<Cooperation> {

    @JsonProperty("name", String)
    @prop({ default: "", required: true })
    public name: string

    @JsonProperty("type", String)
    @prop({ default: "", required: true })
    public type: string

    @JsonProperty("logo", String)
    @prop({ default: "", required: true })
    public logo: string

    @JsonProperty("id", Number)
    public id: number

    public getModel() {
        return this.getModelForClass(Cooperation)
    }
}

export default Cooperation
