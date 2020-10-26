'use strict'

import fortune from 'fortune'
import { Adapter } from '../common/Adapter'
import { InitServerConf } from '../common/InitServerConf'
import { ServerConf } from '../configFactory/ServerConf'
import phLogger from '../logger/PhLogger'

export default class DBFactory {
	private static instance: DBFactory = null
	private typeAnalyzerMapping: Map<string, any> = new Map()
	private serverConf: ServerConf = InitServerConf.getConf

	constructor() {
		this.buildStore(this.serverConf)
	}

	public static get getInstance() {
		if (DBFactory.instance == null) {
			DBFactory.instance = new DBFactory()
		}
		return DBFactory.instance
	}

	public getStore(name?: string): any {
		if (name === undefined || name === null || name.length === 0) {
			if (this.typeAnalyzerMapping.size === 1) {
				return [...this.typeAnalyzerMapping.values()][0]
			} else {
				throw new Error(
					`存在多个Store, 请使用 getStore(参数) 获取对应Store，包含参数：${[...this.typeAnalyzerMapping.keys()]}`,
				)
			}
		}
		return this.typeAnalyzerMapping.get(name)
	}

	private buildStore(conf: ServerConf): any {
		const keys = Object.getOwnPropertyNames(conf)
			.map((name: string) => {
				const ins = conf[name]
				if (ins !== undefined && typeof ins !== 'string') {
					return name
				}
			})
			.filter((item) => item !== undefined)

		let filename = null

		for (const key of keys) {
			const ad = Adapter.init.getAdapter(key)
			// const url = conf[key].getUrl()
            const connect = conf[key].getConnect()
			const path = `${process.cwd()}/dist/models`
			if (conf[key].dao !== undefined) {
				filename = `${path}/${conf[key].dao}.js`
			} else {
				filename = `${path}/${conf.project}.js`
			}
			const metaClass = require(filename).default
			const record = new metaClass()
			const options = Object.assign({
				adapter: [ad, { connection: connect }],
			}, record.operations)
			this.typeAnalyzerMapping.set(key, fortune(record.model, options))
		}
	}
}
