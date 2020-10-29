'use strict'

import { JsonObject, JsonProperty } from 'json2typescript'

@JsonObject('DBConf')
export abstract class DBConf {
	@JsonProperty('algorithm', String)
	public algorithm: string = undefined

	@JsonProperty('dbName', String)
	public dbName: string = undefined

	@JsonProperty('host', String)
	public host: string = undefined

	@JsonProperty('port', Number)
	public port: number = undefined

	@JsonProperty('poolMax', Number, true)
	public poolMax: number = undefined

	@JsonProperty('idleTimeoutMillis', Number, true)
	public idleTimeoutMillis: number = undefined

	@JsonProperty('connectionTimeoutMillis', Number, true)
	public connectionTimeoutMillis: number = undefined

	@JsonProperty('dao', String, true)
	public dao: string = undefined

	@JsonProperty('username', String, true)
	public username: string = undefined

	@JsonProperty('pwd', String, true)
	public pwd: string = undefined

	public abstract getUrl(): string

	public getConnect(): any {
		return {
			database: this.dbName,
			user: this.username,
			password: this.pwd,
			host: this.host,
			port: this.port,
			ssl: false,
			max: this.poolMax,
			idleTimeoutMillis: this.idleTimeoutMillis,
			connectionTimeoutMillis: this.connectionTimeoutMillis
		}
	}
}
