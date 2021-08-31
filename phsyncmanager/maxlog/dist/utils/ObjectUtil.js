"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class ObjectUtil {
    static delObjectKeyIsNull(obj) {
        return Object.keys(obj).map((item) => {
            if (!obj[item]) {
                delete obj[item];
            }
            return true;
        });
    }
}
exports.default = ObjectUtil;
//# sourceMappingURL=ObjectUtil.js.map