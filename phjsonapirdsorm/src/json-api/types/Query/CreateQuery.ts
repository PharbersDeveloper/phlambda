import { CreationReturning } from "../../db-adapters/AdapterInterface"
import { Result } from "../index"
import Resource, { ResourceWithTypePath } from "../Resource"
import Query, { QueryOptions } from "./Query"
export { Resource, ResourceWithTypePath }
import Data from "../Generic/Data"

export type CreateQueryOptions = QueryOptions & {
  records: Data<ResourceWithTypePath>;
  returning: (result: CreationReturning) => Result | Promise<Result>;
}

export default class CreateQuery extends Query {
  protected query: {
    type: QueryOptions["type"];
    catch: QueryOptions["catch"];
    returning: CreateQueryOptions["returning"];
    records: CreateQueryOptions["records"];
  }

  constructor({ records, ...baseOpts }: CreateQueryOptions) {
    super(baseOpts)
    this.query = {
      ...this.query,
      records
    }
  }

  get records() {
    return this.query.records
  }
}
