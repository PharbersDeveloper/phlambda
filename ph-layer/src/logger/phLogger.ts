"use strict"

import { configure, connectLogger, getLogger } from "log4js"

class PhLogger {
    constructor() {
        configure("config/log4js.json")
    }

    public startConnectLog(app: { use: (arg0: any) => void; }) {
        // tslint:disable-next-line: max-line-length
        app.use(connectLogger(getLogger("http"), { level: "auto", format: (req, res, format) => format(`:remote-addr - :method :url HTTP/:http-version :status :referrer`)}))
    }

    public getPhLogger() {
        return getLogger()
    }
}

export default new PhLogger().getPhLogger()
