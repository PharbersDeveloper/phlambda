import { Request } from "../../types"
import * as Errors from "../../util/errors"

export async function checkBodyExistence(request: Request) {
  const hasBody = typeof request.body !== "undefined"

  const needsBody =
    ["post", "patch"].indexOf(request.method as string) !== -1 ||
    (request.method === "delete" && request.aboutRelationship) ||
    (request.method === "delete" && !request.id)

  if (hasBody === needsBody) {
    return
  }

  throw Errors.genericValidation({
    detail: needsBody
      ? "This request needs a body, but didn't have one."
      : "This request should not have a body, but does."
  })
}

export async function checkMethod({ method }: Request) {
  if (["patch", "post", "delete", "get"].indexOf(method) === -1) {
    const detail =
      `The method "${method}" is not supported.` +
      (method === "put" ? " See http://jsonapi.org/faq/#wheres-put" : "")

    throw Errors.generic405({ detail })
  }
}
