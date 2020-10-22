'use strict'
import { JsonObject, JsonProperty } from 'json2typescript'
import { DBConf } from './DBConf'

@JsonObject('MongoConf')
export class MongoConf extends DBConf {
	@JsonProperty('coll', String)
	public coll: string = undefined

	@JsonProperty('authSource', String)
	public authSource: string = undefined

	@JsonProperty('auth', Boolean)
	public auth: boolean = false

	@JsonProperty('other', String)
	public other: string = undefined

	public getUrl(): string {
		return `${this.algorithm}://${this.username}:${this.pwd}@${this.host}/${this.coll}${this.other}`
	}
}
