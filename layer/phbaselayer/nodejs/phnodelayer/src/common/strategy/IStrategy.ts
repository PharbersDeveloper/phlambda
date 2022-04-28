import DBModel from "../models/DBModel"

export default interface IStrategy {
    choose(config: DBModel): any
}
