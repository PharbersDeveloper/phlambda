import BaseModel from '../models/BaseModel'

export default abstract class Config extends BaseModel {
    abstract getConf(): BaseModel
}