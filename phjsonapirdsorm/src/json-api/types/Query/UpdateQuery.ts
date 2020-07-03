import { UpdateReturning } from "../../db-adapters/AdapterInterface"
import Resource, { ResourceWithId, ResourceWithTypePath } from "../Resource"
import Query, { QueryOptions } from "./Query"
export { Resource, ResourceWithTypePath, ResourceWithId }
import Data from "../Generic/Data"
import { Result } from "../index"

export type UpdateQueryOptions = QueryOptions & {
  patch: Data<ResourceWithId & ResourceWithTypePath>;
  returning: (result: UpdateReturning) => Result | Promise<Result>;
}

export default class UpdateQuery extends Query {
  protected query: {
    type: QueryOptions["type"];
    catch: QueryOptions["catch"];
    returning: UpdateQueryOptions["returning"];
    patch: UpdateQueryOptions["patch"];
  }

  constructor({ patch, ...baseOpts }: UpdateQueryOptions) {
    super(baseOpts)

    this.query = {
      ...this.query,
      patch
    }
  }

  get patch() {
    return this.query.patch
  }
}
