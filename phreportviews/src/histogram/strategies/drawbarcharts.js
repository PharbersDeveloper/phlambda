import IDrawable from "./drawable"

export class DrawBarCharts extends IDrawable {
    draw(opt) {
        console.info("bar charts draw")
    }
}

export default new DrawBarCharts()
