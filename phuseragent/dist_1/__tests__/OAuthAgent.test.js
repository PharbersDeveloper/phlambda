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
const AgentAccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"));
    event.queryStringParameters.client_id = "fjjnl2uSalHTdrppHG9u";
    event.queryStringParameters.redirect_uri = "http://www.pharbers.com/oauth-callback";
    event.queryStringParameters.client_secret = "2a21aaa08c78eb6f8c7350ac0dbf5f4a823754915c6302cf2ae6b93ac6caa6e2";
    return event;
});
const AgentClientError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"));
    event.queryStringParameters.client_id = "error client id";
    event.queryStringParameters.redirect_uri = "http://www.pharbers.com/oauth-callback";
    event.queryStringParameters.client_secret = "2a21aaa08c78eb6f8c7350ac0dbf5f4a823754915c6302cf2ae6b93ac6caa6e2";
    return event;
});
const AgentSecretError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"));
    event.queryStringParameters.client_id = "fjjnl2uSalHTdrppHG9u";
    event.queryStringParameters.redirect_uri = "http://www.pharbers.com/oauth-callback";
    event.queryStringParameters.client_secret = "error secret";
    return event;
});
const AgentRedirectUriError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"));
    event.queryStringParameters.client_id = "fjjnl2uSalHTdrppHG9u";
    event.queryStringParameters.redirect_uri = "";
    event.queryStringParameters.client_secret = "2a21aaa08c78eb6f8c7350ac0dbf5f4a823754915c6302cf2ae6b93ac6caa6e2";
    return event;
});
const AgentException = jest.fn(() => {
    return new Map();
});
test("Agent Access", () => __awaiter(void 0, void 0, void 0, function* () {
    const app = require("../../app.js");
    const res = yield app.lambdaHandler(new AgentAccess(), undefined);
    expect(res.statusCode).toBe(200);
    expect(typeof res.body).toEqual("string");
    expect(res.body).toContain("DOCTYPE");
}), 1000 * 60 * 2);
test("Agent ClientID Error", () => __awaiter(void 0, void 0, void 0, function* () {
    const app = require("../../app.js");
    const res = yield app.lambdaHandler(new AgentClientError(), undefined);
    expect(res.statusCode).toBe(403);
    expect(typeof res.body).toEqual("string");
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid client, please contact pharbers");
}), 1000 * 60 * 2);
test("Agent Secret Error", () => __awaiter(void 0, void 0, void 0, function* () {
    const app = require("../../app.js");
    const res = yield app.lambdaHandler(new AgentSecretError(), undefined);
    expect(res.statusCode).toBe(501);
    expect(typeof res.body).toEqual("string");
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid parameters");
}), 1000 * 60 * 2);
test("Agent RedirectUri Error By Null", () => __awaiter(void 0, void 0, void 0, function* () {
    const app = require("../../app.js");
    const res = yield app.lambdaHandler(new AgentRedirectUriError(), undefined);
    expect(res.statusCode).toBe(501);
    expect(typeof res.body).toEqual("string");
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid parameters");
}), 1000 * 60 * 2);
test("Agent Error By Exception", () => __awaiter(void 0, void 0, void 0, function* () {
    const app = require("../../app.js");
    const res = yield app.lambdaHandler(new AgentException(), undefined);
    expect(typeof res).toEqual("object");
    console.info(JSON.stringify(res));
}), 1000 * 60 * 2);
//# sourceMappingURL=OAuthAgent.test.js.map