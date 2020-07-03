import Data from "./Generic/Data"
import { DataWithLinksArgs, UrlTemplatesByType } from "./index"
import MaybeDataWithLinks from "./MaybeDataWithLinks"
import Resource from "./Resource"

export default class ResourceSet extends MaybeDataWithLinks<Resource> {

  get ids() {
    return this._data.map((it) => it.id)
  }

  get types() {
    return this._data.map((it) => it.type)
  }

  get isSingular() {
    return super.isSingular as boolean
  }

  public static of(it: DataWithLinksArgs<Resource>) {
    return new this(it)
  }
  protected _data: Data<Resource>

  protected constructor(it: DataWithLinksArgs<Resource>) {
    if (typeof it.data === "undefined") {
      throw new Error("Cannot construct a ResourceSet with missing data.")
    }

    super(it)
  }

  public toJSON(urlTemplates: UrlTemplatesByType) {
    return this.unwrapWith((it) => it.toJSON(urlTemplates[it.type] || {}), {})
  }
}
