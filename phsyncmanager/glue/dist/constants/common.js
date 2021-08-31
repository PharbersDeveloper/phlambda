"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AWSRegion = exports.PostgresConf = void 0;
const phnodelayer_1 = require("phnodelayer");
exports.PostgresConf = {
    name: phnodelayer_1.StoreEnum.POSTGRES,
    entity: "index",
    database: "phentry",
    user: "pharbers",
    password: "Abcde196125",
    host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
    // host: "127.0.0.1",
    port: 5432,
    poolMax: 2
};
exports.AWSRegion = "cn-northwest-1";
//# sourceMappingURL=common.js.map