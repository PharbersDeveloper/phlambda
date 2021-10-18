"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const parse_query_params_1 = require("json-api/build/src/steps/pre-query/parse-query-params");
const query_parsing_1 = require("json-api/build/src/util/query-parsing");
function urlEncodeFilterParser(filterOps, rawQuery) {
    return query_parsing_1.getQueryParamValue("filter", decodeURIComponent(rawQuery)).
        map((it) => parse_query_params_1.parseFilter(it, filterOps)).getOrDefault(undefined);
}
exports.urlEncodeFilterParser = urlEncodeFilterParser;
//# sourceMappingURL=urlEncodeFilterParser.js.map