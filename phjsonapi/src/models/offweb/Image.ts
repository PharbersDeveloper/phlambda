"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import {arrayProp, prop, Ref, Typegoose} from "typegoose"
import IModelBase from "./modelBase"

@JsonObject("Image")
class Image extends Typegoose implements IModelBase<Image> {
    @JsonProperty("path", String)
    @prop({ default: "", required: false })
    public path: string = ""

    @JsonProperty("tag", String)
    @prop({ default: "", required: false })
    public tag: string = ""

    public getModel() {
        return this.getModelForClass(Image)
    }
}

export default Image
