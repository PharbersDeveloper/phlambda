import * as d3 from "d3"
import {BandScale} from "../../scale/band"
import {TimeScale} from "../../scale/time"
import {LinearScale} from "../../scale/linear"
import {BarCharts} from "../../charts/barcharts"

export class MaxStackCharts extends BarCharts {
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
                domain: [0, this.source.max() * 1.1], // max 累加的max
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
        const stackSericeLength = this.stackSeries.length
        const keyArr = this.keys


        const groups = svg.selectAll("g")
                .data(this.stackSeries)
                .enter()
                .append("g")
                .style("fill", function(d, i) {
                    return curTheme.colors(i, stackSericeLength)
                })
             
        groups.selectAll(".textAll")
                .data(this.stackSeries[0])
                .enter()
                .append("text")
                .text(function(d) {
                    let all = 0
                    const ks = Object.keys(d.data)
                    for(let i = 0; i < ks.length; i++) {
                        all += isNaN(d.data[ks[i]] ) ? 0 : d.data[ks[i]] 
                    }
                    
                    return Math.round(all/1000000)
                })
                .attr("x", function(d, i) { 
                    return xScale(new Date(d.data.time)) - 6;
                })
                .attr("y", function(d) {
                    let all = 0
                    const ks = Object.keys(d.data)
                    for(let i = 0; i < ks.length; i++) {
                        all += isNaN(d.data[ks[i]] ) ? 0 : d.data[ks[i]] 
                    }

                    return yScale(all)
                })
                .attr("fill", "#2B2F3D")
                .attr("font-size", 11)
    
                    
        groups.selectAll("rect") 
            .data(function(d) { 
                return d; 
            }) 
            .enter()
            .append("rect")
            .attr("x", function(d, i) { 
                return xScale(new Date(d.data.time)) - 6;
            })
            .attr("y", function(d) {
                return yScale(d[1]); 
            })
            .attr("height", function(d) {
                return yScale(d[0]) - yScale(d[1]);
            })
            .attr("width", 12)

        groups.selectAll(".text") 
            .data(function(d) { 
                return d; 
            }) 
            .enter()
            .append("text")
            .attr("x", function(d, i) { 
                if (d[1] - d[0] < 10) {
                    return xScale(new Date(d.data.time)) - 3;
                }
                return xScale(new Date(d.data.time)) - 6;
            })
            .attr("y", function(d) {
                return  (yScale(d[0]) + yScale(d[1]))/2; 
            })
            .text(function(d) {
                let all = 0
                for(let i = 0; i < keyArr.length; i++) {
                    const curK = keyArr[i]
                    all += d.data[curK]
                }
                const value = (d[1] - d[0]) / all
                
                return Math.round(value * 1000) / 10 + "%"
            })
            .attr("fill", "#848996")
            .attr("font-size", 11)
    

        if (this.theme.hasLabel()) {
            const l = this.theme.queryLabel()
            l.render(svg, this.source, xScale, yScale)
        }
    }
}