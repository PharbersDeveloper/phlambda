import * as Errors from "../../util/errors"
import { isPlainObject } from "../../util/misc"

export default async function(body) {
  if (!isPlainObject(body) || !Object.prototype.hasOwnProperty.call(body, "data")) {
    throw Errors.missingDataKey()
  }
}
