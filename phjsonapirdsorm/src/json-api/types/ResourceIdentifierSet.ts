import Data from "./Generic/Data"
import { DataWithLinksArgs } from "./index"
import MaybeDataWithLinks from "./MaybeDataWithLinks"
import ResourceIdentifier from "./ResourceIdentifier"

/**
 * Used in rare cases where the primary data of a Document is resource identifier
 * objects, and yet those aren't actually part of a relationship (and so have no
 * owner). E.g., resource identifiers in bulk deletion requests.
 *
 * TODO: ResourceIdentifierSets shouldn't actually be allowed to have links.
 * Refactor to accomplish that (which probably means trying again to make
 * pieces of MaybeDataWithLinks into a mixin, but that can get messy in TS,
 * even with "real mixins" support:
 * https://www.typescriptlang.org/docs/handbook/release-notes/typescript-2-2.html)
 */
export default class ResourceIdentifierSet extends MaybeDataWithLinks<ResourceIdentifier> {

  get isSingular() {
    return super.isSingular as boolean
  }

  public static of(it: DataWithLinksArgs<ResourceIdentifier>) {
    return new this(it)
  }
  protected _data: Data<ResourceIdentifier>

  protected constructor(it: DataWithLinksArgs<ResourceIdentifier>) {
    if (typeof it.data === "undefined") {
      throw new Error(
        "Cannot construct a ResourceIdentifierSet with missing data."
      )
    }

    super(it)
  }

  public toJSON() {
    return this.unwrapWith((it) => it.toJSON(), {})
  }
}
