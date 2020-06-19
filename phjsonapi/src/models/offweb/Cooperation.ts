"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import Image from "./Image"
import IModelBase from "./modelBase"

@JsonObject("Cooperation")
class Cooperation extends Typegoose implements IModelBase<Cooperation> {

    @JsonProperty("name", String)
    @prop({ default: "", required: true })
    public name: string = ""

    @JsonProperty("companyType", String)
    @prop({ default: "", required: true })
    public companyType: string = ""

    @JsonProperty("logo", Image)
    @prop({ ref: Image, default: "", required: false })
    public logo?: Ref<Image>

    @JsonProperty("id", Number)
    public jid: number

    @JsonProperty("language", Number)
    @prop({ default: "", required: true })
    public language: number = 1

    public getModel() {
        return this.getModelForClass(Cooperation)
    }
}

export default Cooperation
