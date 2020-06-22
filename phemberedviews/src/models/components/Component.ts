"use strict"
import {prop, Ref, Typegoose} from "typegoose"
import Datasource from "./Datasource"
import IModelBase from "./modelBase"

class Component extends Typegoose implements IModelBase<Component> {

    @prop({default: "", required: true})
    public name: string

    @prop({default: "", required: true})
    public description: string

    @prop({default: "", required: true})
    public owner: string

    @prop({default: "", required: false})
    public cat: string

    @prop({ ref: Datasource, required: false } )
    public dataSource?: Ref<Datasource>

    @prop({ default: "", required: true} )
    public hbs: string

    public getModel() {
        return this.getModelForClass(Component)
    }
}

export default Component
