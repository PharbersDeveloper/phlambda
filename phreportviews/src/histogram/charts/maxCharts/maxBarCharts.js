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
        const yMax = d3.max(this.source.max()) 
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
             
        svg.selectAll(".rect1") 
            .data(data) 
            .enter()
            .append("rect")
            .attr("x", function(d, i) { 
                  return xScale(new Date(d.time)) - 12;
            })
            .attr("y", function(d) {
                return  yScale(d["产品销售量"]) ; 
            })
            .attr("height", function(d) {
                return ivp.h - yScale(d["产品销售量"]);
            })
            .attr("width", 14)
            .attr("fill", curTheme.colors(2))
        
        svg.selectAll(".rect2") 
            .data(data) 
            .enter()
            .append("rect")
            .attr("x", function(d, i) { 
                  return xScale(new Date(d.time)) - 12 + 14;
            })
            .attr("y", function(d) {
                
                return yScale(d["市场规模"]); 
            })
            .attr("height", function(d) {
                return ivp.h - yScale(d["市场规模"]) ;
            })
            .attr("width", 14)
            .attr("fill", curTheme.colors(0))

        // if (this.theme.hasLabel()) {
        //     const l = this.theme.queryLabel()
        //     l.render(svg, this.source, xScale, yScale)
        // }
    }
}