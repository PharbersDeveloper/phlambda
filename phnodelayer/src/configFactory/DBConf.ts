'use strict'

import { JsonObject, JsonProperty } from 'json2typescript'

@JsonObject('DBConf')
export abstract class DBConf {
	@JsonProperty('algorithm', String)
	public algorithm: string = undefined

	@JsonProperty('host', String)
	public host: string = undefined

	@JsonProperty('port', Number)
	public port: number = undefined

	@JsonProperty('dao', String, true)
	public dao: string = undefined

	@JsonProperty('username', String, true)
	public username: string = undefined

	@JsonProperty('pwd', String, true)
	public pwd: string = undefined

	public abstract getUrl(): string
}
