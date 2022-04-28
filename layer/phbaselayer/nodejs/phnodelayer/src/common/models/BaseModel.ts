
export default abstract class BaseModel {
    name: string
    abstract toString(): string
    abstract toStructure(): any
}
