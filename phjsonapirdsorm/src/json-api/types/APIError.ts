import { UrlTemplates } from "./index"

export interface APIErrorJSON {
  status?: string
  code?: string
  title?: string
  detail?: string
  links?: any
  source?: { pointer?: string, parameter?: string }
  meta?: object
}

export interface Opts {
  status?: string | number
  title?: string
  detail?: string
  typeUri?: string
  source?: { pointer?: string, parameter?: string }
  meta?: object
  rawError?: Error
}

export const displaySafe = Symbol("isJSONAPIDisplayReady")

export default class APIError extends Error {

  /**
   * Creates a JSON-API Compliant Error Object from a JS Error object
   *
   */
  public static fromError(err: any) {
    const ErrorConstructor = this || APIError // in case `this` isn't bound.
    const fallbackTitle =
      "An unknown error occurred while trying to process this request."

    if (err instanceof APIError) {
      return err
    } else if (this.isDisplaySafe(err)) {
      return new ErrorConstructor({
        status: err.status || err.statusCode || 500,
        title: err.title || fallbackTitle,
        detail: err.detail || err.details || (err.message || undefined),
        typeUri: err.typeUri,
        source: typeof err.source === "object" ? err.source : undefined,
        meta: typeof err.meta === "object" ? err.meta : undefined,
        rawError: err
      })
    } else {
      return new ErrorConstructor({
        status: 500,
        title: fallbackTitle,
        rawError: err
      })
    }
  }

  public static isDisplaySafe(it: any) {
    return it && (it instanceof APIError || it[displaySafe])
  }
  public status?: string
  public title?: string
  public detail?: string
  public source?: Opts["source"]
  public meta?: object

  // Even though an APIError is ready for display, the user may
  // want to process it further (to add more tailed messages, e.g.),
  // so we retain the raw error the APIError was created from (if any)
  // for use in such processing, but we don't serialize it
  public rawError?: Error

  // shape may change. To read for now, call toJSON() and examine `code`.
  protected typeUri?: string

  constructor(opts: Opts = {}) {
    // Extract title specially for super call.
    // Call it with a spread so that arguments in the callee is empty
    // (rather than length 1 with [0] === undefined) when no title is present.
    super(...(opts.title ? [String(opts.title)] : []))

    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor || APIError)
    }

    // Use a Proxy to handle coercing status, code etc.
    // to strings on set (including below in the constructor).
    // Because we're setting the validated properties directly on obj,
    // ownKeys will work correctly.
    const res = new Proxy(this, {
      set(obj, prop, value) {
        const coercePropToString =
          ["status", "typeUri", "title", "detail"].indexOf(prop as string) > -1;

        (obj as any)[prop] = coercePropToString
          ? value == null ? undefined : String(value)
          : value

        return true
      }
    })

    // Construct from object format
    Object.assign(res, opts)

    return res
  }

  public toJSON(urlTemplates?: UrlTemplates): APIErrorJSON {
    const { rawError, typeUri, ...serializableProps } = this as any
    const res = {
      ...serializableProps,
      ...(typeUri ? { code: typeUri } : {})
    }

    if (urlTemplates && urlTemplates.about && !(res.links && res.links.about)) {
      return {
        ...res,
        links: { about: urlTemplates.about(this) }
      }
    }

    return res
  }
}
