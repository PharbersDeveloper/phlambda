"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const phnodelayer_1 = require("phnodelayer");
const common_1 = require("../constants/common");
const MaxLogHandler_1 = __importDefault(require("../handler/MaxLogHandler"));
class AppLambdaDelegate {
    async exec(event) {
        try {
            phnodelayer_1.ServerRegisterConfig([new phnodelayer_1.DBConfig(common_1.PostgresConf)]);
            const store = phnodelayer_1.Register.getInstance.getData(phnodelayer_1.StoreEnum.POSTGRES);
            await store.open();
            const handler = new MaxLogHandler_1.default(store);
            await handler.exec(event);
            await store.close();
        }
        catch (error) {
            throw error;
        }
    }
}
exports.default = AppLambdaDelegate;
//# sourceMappingURL=appLambdaDelegate.js.map