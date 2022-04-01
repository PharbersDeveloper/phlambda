"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const log4js_1 = require("log4js");
class PhLogger {
    constructor() {
        // configure(process.env.PH_TS_SERVER_HOME + "/log4js.json")
        log4js_1.configure("config/log4js.json");
    }
    startConnectLog(app) {
        // tslint:disable-next-line: max-line-length
        app.use(log4js_1.connectLogger(log4js_1.getLogger("http"), { level: "auto", format: (req, res, format) => format(`:remote-addr - :method :url HTTP/:http-version :status :referrer`) }));
    }
    getPhLogger() {
        return log4js_1.getLogger();
    }
}
exports.default = new PhLogger().getPhLogger();
//# sourceMappingURL=phLogger.js.map