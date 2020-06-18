"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import { prop, Ref, Typegoose } from "typegoose"
import Image from "./image"
import IModelBase from "./modelBase"

@JsonObject("Participant")
class Participant extends Typegoose implements IModelBase<Participant> {

    @JsonProperty("name", String)
    @prop({ default: "", required: true })
    public name: string = ""

    @JsonProperty("title", String)
    @prop({ default: "", required: false })
    public title: string = ""

    @JsonProperty("occupation", String)
    @prop({ default: "", required: true })
    public occupation: string = ""

    @prop({ ref: Image, required: false })
    public avatar: Ref<Image>

    @JsonProperty("avatar", String)
    public avatarPath?: string = ""

    @JsonProperty("id", Number)
    public jid: number = 0

    @JsonProperty("language", Number)
    @prop({ default: "", required: true })
    public language: number = 1

    public getModel() {
        return this.getModelForClass(Participant)
    }
}

export default Participant
