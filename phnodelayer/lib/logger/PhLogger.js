'use strict';
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = __importStar(require("fs"));
const log4js_1 = require("log4js");
class PhLogger {
    constructor() {
        let path = `${process.cwd()}/config/log4js.json`;
        if (!fs.existsSync(path)) {
            path = `${__filename.substring(0, __filename.indexOf('lib'))}config/log4js.json`;
        }
        log4js_1.configure(path);
    }
    startConnectLog(app) {
        // tslint:disable-next-line: max-line-length
        app.use(log4js_1.connectLogger(log4js_1.getLogger('http'), {
            level: 'auto',
            format: (req, res, format) => format(`:remote-addr - :method :url HTTP/:http-version :status :referrer`),
        }));
    }
    getPhLogger() {
        return log4js_1.getLogger();
    }
}
exports.default = new PhLogger().getPhLogger();
