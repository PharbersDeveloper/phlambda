
class RandomCode {
    public random(num: number): string {
        return Math.random().toFixed(num).slice(-num)
    }
}
export default new RandomCode()
