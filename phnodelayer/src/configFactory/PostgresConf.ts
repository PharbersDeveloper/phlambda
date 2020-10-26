'use strict'
import { JsonObject, JsonProperty } from 'json2typescript'
import { DBConf } from './DBConf'

@JsonObject('PostgresConf')
export class PostgresConf extends DBConf {
	@JsonProperty('dbName', String)
	public dbName: string = undefined

	@JsonProperty('poolMax', Number)
	public poolMax: number = undefined

	@JsonProperty('idleTimeoutMillis', Number)
	public idleTimeoutMillis: number = undefined

	@JsonProperty('connectionTimeoutMillis', Number)
	public connectionTimeoutMillis: number = undefined

	public getUrl(): string {
		return `${this.algorithm}://${this.username}:${this.pwd}@${this.host}:${this.port}/${this.dbName}`
	}

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
