import { JSONAPIAdapter } from "./JSONAdapter"

export default class TransformData {

    run(type: string, data: any) {
        return new JSONAPIAdapter(type, data).serialize()
    }
}
