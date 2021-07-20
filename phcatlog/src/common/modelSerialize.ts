import {Serializer} from "jsonapi-serializer"
import Register from "./register"

export default class ModelSerialize {

    public serialize(model: string, data: any) {
        const entity = Register.getInstance.getEntity()
        const models = data.map((item) => entity.model[model] = item)
        const serializerIns = new Serializer(model, {
            attributes: Object.keys(entity.model[model])
        })
        return serializerIns.serialize(models)
    }
}
