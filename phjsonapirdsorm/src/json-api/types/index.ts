import { IncomingMessage, ServerResponse } from "http"
import { ParsedStandardQueryParams } from "../steps/pre-query/parse-query-params"
import APIError from "./APIError"
import Document, { DocumentData } from "./Document"
import Data from "./Generic/Data"
import Resource, { ResourceJSON } from "./Resource"
import ResourceIdentifier, { ResourceIdentifierJSON } from "./ResourceIdentifier"
import { UrlTemplate } from "./UrlTemplate"

// A helper type to capture the ability of
// a given type T to appear singularly or in an array.
export type DataOf<T> = null | T | T[]

// Another global helper.
export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>

// Types used in the code as function arguments for JSON:API structures.
export type PrimaryData = DataOf<Resource> | DataOf<ResourceIdentifier>
export type ErrorOrErrorArray = Error | APIError | Array<APIError | Error>
export interface DataWithLinksArgs<T> {
  data: T | T[] | null | Data<T>
  links?: UrlTemplates
}

// Types for JSON values
export type LinkageJSON = DataOf<ResourceIdentifierJSON>
export type PrimaryDataJSON = DataOf<ResourceJSON> | LinkageJSON
export interface Links { [linkName: string]: any }

// Types for convenience, for built-in js array helpers.
export type Reducer<T, U = any> = (acc: U, it: T, i: number, arr: T[]) => U
export type PredicateFn<T> = (it: T, i: number, arr: T[]) => boolean
export type Mapper<T, U> = (it: T, i: number, arr: T[]) => U
export type AsyncMapper<T, U> = (it: T, i: number, arr: T[]) => U | Promise<U>
export interface Reduceable<T, U> { reduce: (fn: Reducer<T, U>, init?: U) => U }

// Types for interacting with the underlying server
export type ServerReq = IncomingMessage
export type ServerRes = ServerResponse

// Types for generalizing/defining protocols between the internal types.
export interface StrictDictMap<T> { [it: string]: T | undefined }

// Types related to queries
export type SortDirection = "ASC" | "DESC"
export interface FieldSort { field: string; direction: SortDirection }
export interface ExpressionSort { expression: FieldExpression, direction: SortDirection }
export type Sort = FieldSort | ExpressionSort

// Parameter values
export type ParsedFilterParam = FieldExpression[]
export type ParsedSortParam = Sort[]
export type ParsedQueryParams = ParsedStandardQueryParams & {
  sort?: ParsedSortParam,
  filter?: ParsedFilterParam
}

/**
 * A function that receives the parse result for a set of args for a
 * FieldExpression and transforms the args from parse result form to a form
 * usable by consumers, or throws if the args are invalid.
 */
export type FinalizeArgs = (
  operatorsConfig: ParserOperatorsConfig,
  operator: string,
  args: any[]
) => any

export interface OperatorDesc {
  legalIn?: Array<"sort" | "filter">
  arity?: number
  finalizeArgs?: FinalizeArgs
}

// An operator descriptor after we've applied any defaults
// to set arity, finalizeArgs, and legalIn.
export type FinalizedOperatorDesc = Required<OperatorDesc>

// The type each adapter must provide.
// Map from operatorName to { arity, finalizeArgs, legalIn } object.
export type SupportedOperators = StrictDictMap<OperatorDesc>

// The adapter-provided info about supported operators, post finalization.
export type FinalizedSupportedOperators = StrictDictMap<FinalizedOperatorDesc>

// The information about supported operators that we give to each parser.
// We've already filtered out the illegal operators, so we don't pass `legalIn`.
export type ParserOperatorsConfig =
  StrictDictMap<Omit<FinalizedOperatorDesc, "legalIn">>

export type AndExpression =
  FieldExpression & { operator: "and", args: FieldExpression[] }

export interface Identifier { type: "Identifier", value: string }

export type FieldExpression = ({
  operator: "or",
  args: FieldExpression[]
} | {
  operator: "and",
  args: FieldExpression[]
} | {
  operator: "eq" | "neq" | "ne"; // ne and neq are synonyms
  args: [Identifier, any]
} | {
  operator: "in" | "nin";
  args: [Identifier, string[] | number[]]
} | {
  operator: "lt" | "gt" | "lte" | "gte";
  args: [Identifier, string | number];
} | {
  operator: string;
  args: any[];
}/* | {
  operator: '$like'; // not supported in our mongo transform yet
  args: string;
}*/) & {
  type: "FieldExpression"
}

export interface UrlTemplatesByType {
  [typeName: string]: UrlTemplates
}

export interface UrlTemplates {
  [linkName: string]: UrlTemplate | undefined
}

// I'm gonna start introducing more intermediate representations
// so that Request and Response aren't so overloaded/constantly mutated.
export interface Request {
  // The parsed json of the body; undefined if the HTTP body is an empty string.
  body: any | undefined

  // Basic http fields/headers for the request
  method: string
  uri: string
  contentType: string | undefined
  accepts: string | undefined
  rawQueryString: string | undefined

  // The query params on the request, parsed (likely with qs initially).
  // (May be further parsed post creation with JSON:API specific parsers.)
  queryParams: { [paramName: string]: any }

  // JSON:API specific parameters from the url.

  // Note: because of requests like /people/1/author, the type and id
  // stored here may not be that of the returned resourses.
  type: string
  id: string | undefined

  // The relationship name provided in the request's url. This is the
  // "author" part in the example /people/1/author request noted above.
  relationship: string | undefined

  // Whether the target of the request is a relationship (object), as opposed
  // to a resource object or collection. This effects how incoming data is
  // parsed. E.g., this is true for /people/1/relationships/author but not
  // for /people/1/author
  aboutRelationship: boolean

  // The prop below will be used in the future with the JSON:API ext system.
  // ext: string[];
}

// A request, with its query parameters parsed for their
// JSON:API-specific format, and the body (if any) parsed into a Document.
export type FinalizedRequest = Request & {
  queryParams: ParsedQueryParams;
  document: Document | undefined;
}

// Result is different than HTTPResponse in that it contains details of the
// result that are salient for JSON:API, not structured in HTTP terms.
export interface Result {
  // headers should not include Content-Type,
  // which is assumed to be JSON:API.
  headers?: { [headerName: string]: string }
  ext?: string[]
  status?: number
  document?: Document
}

export interface HTTPResponse {
  // Note: header names are all lowercase.
  // I've enumerated them here to get better type checking.
  // If you're adding custom headers, you probably want to extend this type.
  headers: {
    "content-type"?: string;
    vary?: string;
  }
  status: number
  body?: string
}

export type makeDocument = (data: DocumentData) => Document
