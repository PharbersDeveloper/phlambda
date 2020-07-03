import { Model } from "mongoose"
import { StrictDictMap } from "../../../types"
import { isRootModel } from "./schema"

export function getTypePath(
  model: Model<any>,
  modelNamesToTypeNames: StrictDictMap<string>
) {
  const modelNames = isRootModel(model)
    ? [model.modelName]
    : [model.modelName, model.baseModelName as string]

  return modelNames.map((it) => modelNamesToTypeNames[it]) as string[]
}
