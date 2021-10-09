"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const phS3Facade_1 = __importDefault(require("../s3facade/phS3Facade"));
/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
class AppHtmlDelegate {
    constructor() {
        this.tmpFolder = "./";
    }
    queryTemplate(hbs, id) {
        return phS3Facade_1.default.getObject("ph-cli-dag-template", "components/example.hbs");
    }
}
exports.default = AppHtmlDelegate;
//# sourceMappingURL=appHtmlDelegate.js.map