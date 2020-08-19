import * as d3 from "d3"
import {BandScale} from "../../scale/band"
import {TimeScale} from "../../scale/time"
import {LinearScale} from "../../scale/linear"
import {BarCharts} from "../../charts/barcharts"

export class MaxBarCharts extends BarCharts {
    constructor(
        source,
        theme,
        scales = { x: new TimeScale(), y: new LinearScale() }) {

        super(source, theme, scales)
    }

    genXScale(ivp) {
        const x = this.scales["x"]
        console.log(1)
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
        console.log(2, d3.max(this.source.max()), this.source.max())
        const y = this.scales["y"]
        const yMax = d3.max(this.source.max()) * 1.1
        if (y) {
            const opt = {
                domain: [ 0, yMax], 
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
        const data = this.source.ds.dataset
        console.log("data,", data)
             
        svg.selectAll(".rect1") 
            .data(data) 
            .enter()
            .append("rect")
            .attr("x", function(d, i) { 
                console.log("d", d)
                  return xScale(new Date(d.time)) - 6;
            })
            .attr("y", function(d) {
                return ivp.h - yScale(d["市场规模"]); 
            })
            .attr("height", function(d) {
                return yScale(d["市场规模"]);
            })
            .attr("width", 14)
            .attr("fill", curTheme.colors(0))
        
        svg.selectAll(".rect2") 
            .data(data) 
            .enter()
            .append("rect")
            .attr("x", function(d, i) { 
                console.log("d", d)
                  return xScale(new Date(d.time)) - 6 + 14;
            })
            .attr("y", function(d) {
                return ivp.h - yScale(d["产品销售量"]); 
            })
            .attr("height", function(d) {
                return yScale(d["产品销售量"]);
            })
            .attr("width", 14)
            .attr("fill", curTheme.colors(2))

        // const lineDate = this.source.ds.dataset
        // const line = d3.line()
        //     .x(d => {
        //         console.log("1",xScale(d["市场增长率"]))
        //         return xScale(d["市场增长率"])
        //     })
        //     .y(d => yScale(d["产品增长率"]))
    
        // svg.select(".lineChart")
        //     .append("path")
        //     .datum(lineDate)
        //     .attr("d", line)
    

        // if (this.theme.hasLabel()) {
        //     const l = this.theme.queryLabel()
        //     l.render(svg, this.source, xScale, yScale)
        // }
    }
}