import {Serializer} from "jsonapi-serializer"
import Register from "../common/Register"

export default class ModelSerialize {

    serialize(model: string, data: any) {
        const entity = Register.getInstance.getEntity()
        const models = []// data.map((item) => entity.model[model] = item)
        const serializerIns = new Serializer(model, {
            attributes: Object.keys(entity.model[model])
        })
        return serializerIns.serialize(models)
    }
}
