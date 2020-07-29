import {Position} from "./theme/utils/position"
import * as d3 from "d3"
import {LinearScale} from "./scale/linear"

export class Histogram {
    constructor(
        source,
        theme,
        charts = [],
        scales = { x : new LinearScale(), y: new LinearScale() }) {

        this.theme = theme
        this.source = source
        this.charts = charts
        this.scales = scales
    }

    genXAxisScale(ivp) {
        const x = this.scales["x"]
        if (x) {
            const opt = {
                domain: [0, this.source.max()],
                rangeRound: [ivp.x, ivp.w],
                paddingInner: 0.05
            }
            return x.genScale(opt)
        } else {
            return d3.scaleBand()
                .domain(d3.range(this.source.length()))
                .rangeRound([ivp.x, ivp.w])
                .paddingInner(0.05)
        }
    }

    genYAxisScale(ivp) {
        const y = this.scales["y"]
        if (y) {
            const opt = {
                domain: [0, this.source.max()],
                rangeRound: [ivp.h, ivp.y]
            }
            return y.genScale(opt)
        } else {
            return d3.scaleLinear()
                .domain([0, this.source.max()])
                .range([ivp.h, ivp.y])
        }
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

        this.charts.forEach(x => x.render(svg, ivp))

        this.theme.queryHorAxis().forEach(x => x.render(svg, xAxisScale, ivp))
        this.theme.queryVerAxis().forEach(x => x.render(svg, yAxisScale, ivp))
    }

    registerCharts(c) {
        this.charts.push(c)
    }
}
