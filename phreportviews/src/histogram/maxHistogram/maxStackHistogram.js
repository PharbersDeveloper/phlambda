import {Position} from "../theme/utils/position"
import * as d3 from "d3"
import {LinearScale} from "../scale/linear"
import {BandScale} from "../scale/band"
import {TimeScale} from "../scale/time"
import { Histogram } from "../histogram"
import label from "../label/defaultlabel"

export class MaxStackHistogram extends Histogram {
    constructor(
        hid,
        source,
        theme,
        charts = [],
        scales = { x : new TimeScale(), y: new LinearScale() }) {

        super(hid, source, theme, charts, scales)

        this.hid = hid
        this.theme = theme
        this.source = source
        this.charts = charts
        this.scales = scales
    }

    genXAxisScale(ivp) {
        const x = this.scales["x"]
        if (x) {
            const opt = {
                domain: [new Date("2018-01"), new Date("2019-12")],
                rangeRound: [ivp.x, ivp.w],
                paddingInner: 0.05
            }
            return x.genScale(opt)
        } else return null
    }

    genYAxisScale(ivp) {
        const y = this.scales["y"]
        if (y) {
            const opt = {
                domain: [0, this.source.max() * 1.1], // 叠加后的最大值
                rangeRound: [ivp.h, ivp.y]
            }
            return y.genScale(opt)
        } else return null
    }

    displayHistogram(width, height, xTitle, yTitle) {
        this.render(width, height, xTitle, yTitle)
        // this.events()
    }

  

    /**
     * 3. Render the initial view
     */
    render(width, height, xTitle, yTitle) {
        const vp = this.theme.histogramRect(new Position(0, 0, width, height))
        const ivp = this.theme.histogramInnerRect(vp)
        const getColor = this.theme.colors.bind(this)
        const labelData = this.source.keys()
        const colors = this.theme.getUsedColors(labelData, labelData.length)

        // outer info 的处理 
        // 修改ivp
        const info = d3.select(this.hid)
                        .append("svg")
                        .attr("width", width)
                        .attr("height", height)
        
        // info.append("text")
        //         .attr("font-size", "12px")
        //         .attr("fill", "#848996")
        //         .attr("transform", `translate(${ivp.w/2}, ${ivp.h + 40})`)
        //         .text("")   
                
        info.append("text")
                .attr("font-size", "12px")
                .attr("fill", "#848996")
                .attr("transform", `translate(10, ${ivp.h / 2}) rotate(270, 10 10)`)
                .text("销售额")

        const infogs = info.selectAll("g")
            .data(this.source.keys())
            .enter()
            .append("g")
        
        infogs.selectAll("rect")
            .data(this.source.keys())
            .enter()
            .append("rect")
            .attr("width", 8)
            .attr("height", 8)
            .attr("fill", function(d, i) {
                return colors[i]
            })
            .attr("transform", function(d, i) {
                const x = (i + 1) * 24 + i * (ivp.w - 24*4)/4
                let offset = 0
                if (labelData.length < 4) {
                    offset =  (4 -labelData.length ) * x / 2 
                }
                return `translate(${ivp.x + x + offset}, ${ivp.h + 60 - 8})`
            })
            .attr("rx", "2")
            .attr("ry", "2")

        infogs.selectAll("text")
            .data(this.source.keys())
            .enter()
            .append("text")
            .text(function(d) {
                return d
            })
            .attr("fill", "#7A869A")
            .attr("transform", function(d, i) {
                const x = (i + 1) * 24 + i * (ivp.w - 24*4)/4
                let offset = 0
                if (labelData.length < 4) {
                    offset =  (4 -labelData.length ) * x / 2 
                }
                return `translate(${ivp.x + x + 20 + offset}, ${ivp.h + 60})`
            })
            .attr("font-size", 12)


        // 图表
        const svg = info.append("svg")
            .attr("width", width)
            .attr("height", height)

            
        const xAxisScale = this.genXAxisScale(ivp)
        const yAxisScale = this.genYAxisScale(ivp)
            
        // this.theme.setXAxisTicks(this.source.min()[0] * 0.9, this.source.max()[0]*1.1, 5)
        // this.theme.createColors(svg)
        // this.theme.clipBubbleChart(svg, ivp)
        this.theme.setYAxisTicks(0, this.source.max() * 1.1, 3)
        this.theme.axisAssist(svg, yAxisScale,ivp)
            
        this.charts.forEach(x => x.render(svg, ivp))
        
        this.theme.showExtraAAxis(svg, ivp)
        this.theme.showLabel(svg, ivp, this.source.keys())

        if (xAxisScale) {
            this.theme.queryHorAxis().forEach(x => x.render(svg, xAxisScale, ivp))
        }

        if (yAxisScale) {
            this.theme.queryVerAxis().forEach(x => x.render(svg, yAxisScale, ivp))
        }

        // this.showTitle(ivp,svg, xTitle, yTitle)
    }

    registerCharts(c) {
        this.charts.push(c)
    }

    showTitle(ivp,svg, xTitle, yTitle) {
        if (xTitle) {
            this.theme.queryHorAxis().forEach(x => x.showXTitle(svg, xTitle, ivp))
        }

        if (yTitle) {
            this.theme.queryVerAxis().forEach(x => x.showYTitle(svg, yTitle, ivp))
        }
    }
}
