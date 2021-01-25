/**
 * An interface representing the client and associated data
 */
// tslint:disable-next-line:interface-name
export interface Client {
    id: string
    redirectUris?: string | string[]
    grants: string | string[]
    accessTokenLifetime?: number
    refreshTokenLifetime?: number
    [key: string]: any
}
