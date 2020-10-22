'use strict'

import * as fs from 'fs'
import * as yaml from 'js-yaml'
import { JsonConvert, ValueCheckingMode } from 'json2typescript'
import { ServerConf } from '../configFactory/ServerConf'
import phLogger from '../logger/PhLogger'

export class InitServerConf {
	private static conf: ServerConf

	private static init() {
		let path = `${process.cwd()}/config/server.yml`
		if (!fs.existsSync(path)) {
			path = `${__filename.substring(0, __filename.indexOf('lib'))}config/server.yml`
		}
		phLogger.debug('加载配置文件地址', path)
		const jsonConvert = new JsonConvert()
		const doc = yaml.safeLoad(fs.readFileSync(path, 'utf8'))
		jsonConvert.ignorePrimitiveChecks = false
		jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL
		InitServerConf.conf = jsonConvert.deserializeObject(doc, ServerConf)
	}

	public static get getConf() {
		if (InitServerConf.conf == null) {
			this.init()
		}
		return InitServerConf.conf
	}
}
