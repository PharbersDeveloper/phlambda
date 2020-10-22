'use strict'

import * as fs from 'fs'
import { configure, connectLogger, getLogger } from 'log4js'

class PhLogger {
	constructor() {
		let path = `${process.cwd()}/config/log4js.json`
		if (!fs.existsSync(path)) {
			path = `${__filename.substring(0, __filename.indexOf('lib'))}config/log4js.json`
		}
		configure(path)
	}

	public startConnectLog(app: { use: (arg0: any) => void }) {
		// tslint:disable-next-line: max-line-length
		app.use(
			connectLogger(getLogger('http'), {
				level: 'auto',
				format: (req, res, format) => format(`:remote-addr - :method :url HTTP/:http-version :status :referrer`),
			}),
		)
	}

	public getPhLogger() {
		return getLogger()
	}
}

export default new PhLogger().getPhLogger()
