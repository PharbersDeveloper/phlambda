import * as d3 from "d3"
import {Charts} from "./chats"

export class BarCharts extends Charts {

    constructor(
        source,
        theme) {

        super(source, theme)
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

    getBarHeight(d, i, ys, ivp) {
        return ivp.h - ys(this.source.measure(d))
    }

    getBarBand(d, i, xs, ivp) {
        return xs.bandwidth()
    }

    getBarPosX(d, i, xs, ivp) {
        return xs(i)
    }

    getBarPosY(d, i, ys, ivp) {
        return ys(this.source.measure(d))
    }

    render(svg, ivp) {
        const xScale = this.genXScale(ivp)
        const yScale = this.genYScale(ivp)

        svg.selectAll("rect")
            .data(this.source.apply())
            .enter()
            .append("rect")
            .attr("x", (d, i) => this.getBarPosX(d, i, xScale, ivp))
            .attr("y", (d, i) => this.getBarPosY(d, i, yScale, ivp))
            .attr("width", (d, i) => this.getBarBand(d,i, xScale, ivp))
            .attr("height", (d, i) => this.getBarHeight(d, i, yScale, ivp))
            .attr("fill", (d, i) => this.theme.colors(i))

        if (this.theme.hasLabel()) {
            const l = this.theme.queryLabel()
            l.render(svg, this.source, xScale, yScale)
        }
    }

    /**
     * 4. interactivity
     */
    events() {
        console.error("not implemented")
    }
}
