"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import { arrayProp, prop, Ref, Typegoose } from "typegoose"
import Evaluation from "./Evaluation"
import Hospital from "./Hospital"
import IModelBase from "./modelBase"
import Preset from "./Preset"
import Product from "./Product"
import Requirement from "./Requirement"
import Resource from "./Resource"
import Validation from "./Validation"
// import mongoose = require("mongoose")

@JsonObject("Proposal")
class Proposal extends Typegoose implements IModelBase<Proposal> {

    @JsonProperty("name", String)
    @prop({ required: true })
    public name: string = ""

    @JsonProperty("describe", String)
    @prop({ required: true })
    public describe: string = ""

    @JsonProperty("totalPhase", Number)
    @prop({ required: true })
    public totalPhase: number = 1

    @JsonProperty("case", String)
    @prop({ required: true })
    public case: string = ""

    @JsonProperty("periodStep", String)
    @prop({ required: true })
    public periodStep: string = ""

    @JsonProperty("periodBase", Number)
    @prop({ required: true })
    public periodBase: number = 0

    @arrayProp( { itemsRef: Product, required: false, default: [] } )
    public products: Array<Ref<Product>>

    @arrayProp( { itemsRef: Hospital, required: false, default: [] } )
    public targets: Array<Ref<Hospital>>

    @arrayProp( { itemsRef: Resource, required: false, default: [] } )
    public resources: Array<Ref<Resource>>

    // @arrayProp( { itemsRef: Preset, required: false, default: [] } )
    // public presets: Array<Ref<Preset>>

    @arrayProp( { itemsRef: Evaluation, required: false, default: [] } )
    public evaluations: Array<Ref<Evaluation>>

    @prop({ ref: Requirement, required: false, default: [] })
    public quota: Ref<Requirement>

    @arrayProp({ itemsRef: Validation, required: false, default: [] })
    public validations: Array<Ref<Validation>>

    public getModel() {
        return this.getModelForClass(Proposal)
    }
}

export default Proposal
