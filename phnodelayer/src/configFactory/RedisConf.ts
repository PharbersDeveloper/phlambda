'use strict'
import { JsonObject, JsonProperty } from 'json2typescript'
import { DBConf } from './DBConf'

@JsonObject('RedisConf')
export class RedisConf extends DBConf {

	public getUrl(): string {
		return `${this.algorithm}://${this.host}:${this.port}/${this.dbName}`
	}
}
