"use strict";
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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = __importStar(require("fs"));
const http_1 = require("http");
const phS3Facade_1 = __importStar(require("../s3facade/phS3Facade"));
const phnodelayer_1 = require("phnodelayer");
const pherrors_1 = require("../errors/pherrors");
class AppLambdaDelegate {
    constructor() {
        this.dbIns = phnodelayer_1.dbFactory.getInstance.getStore(phnodelayer_1.store.Postgres);
    }
    exec(event) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.dbIns.connect();
            try {
                const req = new phnodelayer_1.AWSRequest(event, "common");
                const response = new http_1.ServerResponse(req);
                //@ts-ignore
                const clientId = event.queryStringParameters.client_id;
                // @ts-ignore
                const redirectUri = event.queryStringParameters.redirect_uri;
                // @ts-ignore
                const secret = event.queryStringParameters.client_secret;
                const hbs = fs.readFileSync("config/login.hbs");
                const client = yield this.dbIns.find("client", [clientId], {});
                if (client.payload.records.length === 0) {
                    pherrors_1.errors2response(pherrors_1.PhInvalidClient, response);
                    return response;
                }
                if (client.payload.records[0].secret !== secret) {
                    pherrors_1.errors2response(pherrors_1.PhInvalidParameters, response);
                    return response;
                }
                if (redirectUri === "" || redirectUri === undefined) {
                    pherrors_1.errors2response(pherrors_1.PhInvalidParameters, response);
                    return response;
                }
                //@ts-ignore
                response.headers = { "Content-Type": "text/x-handlebars-template" };
                const result = String(hbs).replace("{{client_id}}", clientId).replace("{{redirect_uri}}", redirectUri).replace("{{client_secret}}", secret);
                response.statusCode = 200;
                // @ts-ignore
                response.body = result;
                return response;
            }
            catch (e) {
                throw e;
            }
            finally {
                yield this.dbIns.disconnect();
            }
        });
    }
}
exports.default = AppLambdaDelegate;
//# sourceMappingURL=appLambdaDelegate.js.map