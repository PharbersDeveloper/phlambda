
import { PhAccessToUnauthorized, PhAccess, errors2response } from "./errors/pherrors"
import Identify from "./Identify"

export const Errors2response = errors2response

export const identify = (event: Map<string, any>,scope: string): any => {
    if (!new Identify().verify(event, scope)) {
        return PhAccessToUnauthorized
    }
    return PhAccess
}
