import * as d3 from "d3"
import {BandScale} from "../../scale/band"
import {TimeScale} from "../../scale/time"
import {LinearScale} from "../../scale/linear"
import {LineCharts} from "../linecharts"

export class MaxLineCharts extends LineCharts {
    constructor(
        source,
        theme,
        scales = { x: new TimeScale(), y: new LinearScale() }) {

        super(source, theme, scales)

        const stack = d3.stack()
                            .keys(this.source.keys())
        this.stackSeries = stack(source.ds.dataset)
        this.source = source
        this.keys = this.source.keys()
    }

    genXScale(ivp) {
        const x = this.scales["x"]
        if (x) {
            const opt = {
                domain: [new Date("2018-01"), new Date("2019-12")],
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

    genYScale(ivp) {
        const y = this.scales["y"]
        if (y) {
            const opt = {
                domain: [-1, 1], 
                rangeRound: [ivp.h, ivp.y]
            }
            return y.genScale(opt)
        } else {
            return d3.scaleLinear()
                .domain([0, this.source.max()])
                .range([ivp.h, ivp.y])
        }
    }


    render(svg, ivp) {
        const xScale = this.genXScale(ivp)
        const yScale = this.genYScale(ivp)
        const curTheme = this.theme
        const lineDate = this.source.ds.dataset
        const lineA = d3.line()
                        .x(function(d) { return xScale(new Date(d["time"])) })
                        .y(function(d) { return yScale(d["市场增长率"]) })

        const lineB = d3.line()
                        .x(function(d) { return xScale(new Date(d["time"])) + 12 })
                        .y(function(d) { return yScale(d["产品增长率"]) })
        console.log("data,", data)
            
        svg.append("path")
            .datum(lineDate)
            .attr("d", lineA)
            .attr('fill', 'none')
            .attr('stroke-width', 1)
            .attr('stroke', '#3492E5');

        svg.append("path")
            .datum(lineDate)
            .attr("d", lineB)
            .attr('fill', 'none')
            .attr('stroke-width', 1)
            .attr('stroke', '#283034');
    

        if (this.theme.hasLabel()) {
            const l = this.theme.queryLabel()
            l.render(svg, this.source, xScale, yScale)
        }
    }
}