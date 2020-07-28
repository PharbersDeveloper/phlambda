import * as d3 from "d3"
import {Histogram} from "../histogram"
import {Position} from "../theme/utils/position"

export class BarCharts extends Histogram {

    constructor(
        source,
        theme) {

        super(source, theme)
    }

    render(width, height, dataset) {
        const vp = this.theme.histogramRect(new Position(0, 0, width, height))
        const ivp = this.theme.histogramInnerRect(vp)
        const svg = d3.select("body")
                .append("svg")
                // .attr("width", vp.w)
                .attr("width", width)
                // .attr("height", vp.h)
                .attr("height", height)

        const xScale = d3.scaleBand()
                .domain(d3.range(dataset.length))
                .rangeRound([ivp.x, ivp.w])
                .paddingInner(0.05)

        const xAxisScale =
            d3.scaleLinear()
                .domain([0, d3.max(dataset)])
                .range([ivp.x, ivp.w])

        const yScale =
            d3.scaleLinear()
                .domain([0, d3.max(dataset) + 1])
                .range([ivp.h, ivp.y])

        svg.selectAll("rect")
            .data(dataset)
            .enter()
            .append("rect")
            .attr("x", (d, i) => xScale(i))
            .attr("y", (d) => yScale(d))
            .attr("width", xScale.bandwidth())
            .attr("height", (d) => ivp.h - yScale(d))
            .attr("fill", (d, i) => this.theme.colors(i))

        svg.selectAll("text")
            .data(dataset)
            .enter()
            .append("text")
            .text((d) => d.toString())
            .attr("x", (d, i) => xScale(i) + xScale.bandwidth() / 2)
            .attr("y", (d) => yScale(d) + 14)
            .attr("font-family", "sans-serif")
            .attr("font-size", "11px")
            .attr("fill", "white")
            .attr("text-anchor", "middle")

        // const xAxis = d3.axisBottom().scale(xAxixScale).tickValues([0, 1, 2, 3])//.ticks(dataset.length)
        const xAxis = d3.axisBottom().scale(xAxisScale).ticks(dataset.length)
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0," + ivp.h + ")")
            .call(xAxis)

        const yAxis = d3.axisLeft().scale(yScale).ticks(dataset.length)
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + ivp.x + ", 0)")
            .call(yAxis)
    }

    /**
     * 4. interactivity
     */
    events() {
        console.error("not implemented")
        throw new Error("not Implemented")
    }
}
