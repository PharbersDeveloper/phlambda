"use strict"

import parseQueryParams, { parseFilter, parseSort } from "../json-api/steps/pre-query/parse-query-params"
import { ParserOperatorsConfig } from "../json-api/types"
import { getQueryParamValue } from "../json-api/util/query-parsing"

export function urlEncodeFilterParser( filterOps: ParserOperatorsConfig, rawQuery: string | undefined) {
    return getQueryParamValue("filter", decodeURIComponent(rawQuery)).
        map((it) => parseFilter(it, filterOps)).getOrDefault(undefined)
}
