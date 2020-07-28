import {Position} from "./theme/utils/position"
import * as d3 from "d3"

export class Histogram {
    constructor(
        source,
        theme,
        charts) {

        this.theme = theme
        this.source = source
        this.charts = charts
    }

    genXAxisScale(ivp) {
        return d3.scaleLinear()
            .domain([0, this.source.max()])
            .range([ivp.x, ivp.w])
    }

    genYAxisScale(ivp) {
        return d3.scaleLinear()
            .domain([0, this.source.max()])
            .range([ivp.h, ivp.y])
    }

    displayHistogram(width, height) {
        this.render(width, height)
        // this.events()
    }

    /**
     * 3. Render the initial view
     */
    render(width, height) {
        const vp = this.theme.histogramRect(new Position(0, 0, width, height))
        const ivp = this.theme.histogramInnerRect(vp)
        const svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)

        const xAxisScale = this.genXAxisScale(ivp)
        const yAxisScale = this.genYAxisScale(ivp)

        this.theme.queryHorAxis().forEach(x => x.render(svg, xAxisScale, ivp))
        this.theme.queryVerAxis().forEach(x => x.render(svg, yAxisScale, ivp))

        this.charts.forEach(x => x.render(svg, ivp))
    }

    /**
     * 4. interactivity
     */
    events() {
        console.error("not implemented")
        throw new Error("not Implemented")
    }
}
