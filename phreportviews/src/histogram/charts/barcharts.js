import * as d3 from "d3"
import {Histogram} from "../histogram"
import {Position} from "../theme/utils/position"

export class BarCharts extends Histogram {

    constructor(
        source,
        theme,
        scales) {

        super(source, theme, scales)
    }

    genXScale(ivp) {
        return d3.scaleBand()
            .domain(d3.range(this.source.length()))
            .rangeRound([ivp.x, ivp.w])
            .paddingInner(0.05)
    }

    genYScale(ivp) {
        return d3.scaleLinear()
            .domain([0, this.source.max()])
            .range([ivp.h, ivp.y])
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

    render(width, height) {
        const vp = this.theme.histogramRect(new Position(0, 0, width, height))
        const ivp = this.theme.histogramInnerRect(vp)
        const svg = d3.select("body")
                .append("svg")
                .attr("width", width)
                .attr("height", height)

        const xScale = this.genXScale(ivp)
        const yScale = this.genYScale(ivp)

        const xAxisScale = this.genXAxisScale(ivp)
        const yAxisScale = this.genYAxisScale(ivp)

        svg.selectAll("rect")
            .data(this.source.apply())
            .enter()
            .append("rect")
            .attr("x", (d, i) => xScale(i))
            .attr("y", (d) => yScale(d))
            .attr("width", xScale.bandwidth())
            .attr("height", (d) => ivp.h - yScale(d))
            .attr("fill", (d, i) => this.theme.colors(i))

        if (this.theme.hasLabel()) {
            const l = this.theme.queryLabel()
            l.render(svg, this.source, xScale, yScale)
        }

        this.theme.queryHorAxis().forEach(x => x.render(svg, xAxisScale, ivp))
        this.theme.queryVerAxis().forEach(x => x.render(svg, yAxisScale, ivp))
    }

    /**
     * 4. interactivity
     */
    events() {
        console.error("not implemented")
        throw new Error("not Implemented")
    }
}
