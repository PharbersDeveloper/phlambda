import { SupportedOperators } from "../types"
import Data from "../types/Generic/Data"
import AddToRelationshipQuery from "../types/Query/AddToRelationshipQuery"
import CreateQuery from "../types/Query/CreateQuery"
import DeleteQuery from "../types/Query/DeleteQuery"
import FindQuery from "../types/Query/FindQuery"
import RemoveFromRelationshipQuery from "../types/Query/RemoveFromRelationshipQuery"
import UpdateQuery from "../types/Query/UpdateQuery"
import Relationship from "../types/Relationship"
import { ResourceWithId, ResourceWithTypePath } from "../types/Resource"

export type ReturnedResource = ResourceWithTypePath & ResourceWithId

export interface RelationshipUpdateReturning { before?: Relationship, after?: Relationship }

export interface FindReturning {
  primary: Data<ReturnedResource>,
  // Below, using a required property with `| undefined` plays better with
  // destructuring in TS than an optional property without undefined.
  included: ReturnedResource[] | undefined,
  collectionSize: number | undefined
}

export interface CreationReturning { created: Data<ReturnedResource> }

export interface UpdateReturning { updated: Data<ReturnedResource> }

export interface DeletionReturning { deleted?: Data<ReturnedResource> }

export type QueryReturning =
  FindReturning | CreationReturning | UpdateReturning | DeletionReturning | RelationshipUpdateReturning

export interface TypeInfo { typePath: string[]; extra?: any }
export interface TypeIdMapOf<T> {
  [type: string]: { [id: string]: T | undefined } | undefined
}

export interface AdapterInstance<T extends new (...args: any[]) => any> {
  constructor: T
  find(query: FindQuery): Promise<FindReturning>
  create(query: CreateQuery): Promise<CreationReturning>
  update(update: UpdateQuery): Promise<UpdateReturning>
  delete(query: DeleteQuery): Promise<DeletionReturning>
  addToRelationship(query: AddToRelationshipQuery): Promise<RelationshipUpdateReturning>
  removeFromRelationship(query: RemoveFromRelationshipQuery): Promise<RelationshipUpdateReturning>
  getModel(typeName: string): any
  getRelationshipNames(typeName: string): string[]
  getTypePaths(items: Array<{type: string, id: string}>): Promise<TypeIdMapOf<TypeInfo>>
}

export interface AdapterClass {
  // Must include the "and" and "eq" operators
  supportedOperators: SupportedOperators
  new (...args: any[]): AdapterInstance<new (...args: any[]) => any>
  getStandardizedSchema(model: any, pluralizer: any): any
}

export interface Adapter<T extends AdapterClass> extends AdapterInstance<T> {

}
