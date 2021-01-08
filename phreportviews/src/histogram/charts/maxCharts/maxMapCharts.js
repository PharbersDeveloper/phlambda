import * as d3 from "d3"
import { json, xml } from 'd3-fetch';
import {BandScale} from "../../scale/band"
import {TimeScale} from "../../scale/time"
import {LinearScale} from "../../scale/linear"
import {LineCharts} from "../linecharts"
import chinawithoutsouthsea from "../../../../assets/max/chinawithoutsouthsea.json"

export class MaxMapCharts extends LineCharts {
    constructor(
        source,
        theme,
        scales = { x: new LinearScale(), y: new LinearScale() }) {

        super(source, theme, scales)

        this.source = source
        this.sourceMin = this.source.min()
        this.sourceMax = this.source.max()
        this.sourceMiddle = Math.floor((this.sourceMax - this.sourceMin)/2)
    }

    genXScale(ivp) {
        const x = this.scales["x"]
        
        if (x) {
            const opt = {
                domain: [this.sourceMin, this.sourceMiddle],
                rangeRound: [0, 1],
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
                domain: [this.sourceMax - this.sourceMiddle, this.sourceMax], 
                rangeRound: [0, 1]
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
        const middleData = this.sourceMiddle
        
        const sourceData = this.source
        const projection = d3.geoMercator().fitSize([ivp.w + 50, ivp.h+10], chinawithoutsouthsea);
        const path = d3.geoPath().projection(projection)

        // 渐变色
        const minColor = d3.rgb(252,233,157);
        const middleColor = d3.rgb(248,203,18);
        const maxColor = d3.rgb(139,113,5);
        const computeMinMiddle = d3.interpolateRgb(minColor,middleColor);
        const computeMiddleMax = d3.interpolateRgb(middleColor,maxColor);

        // 省份绘制
        const gs = svg.selectAll("path")
           .data(chinawithoutsouthsea.features)
           .enter()
           .append("g")

        gs.append("path")
           .attr("d", path)
           .attr("stroke", "white")
           .attr("stroke-width", 2)
           .attr("fill", d => {
               const provinceData = sourceData.getCurProvinceData(d.properties.name, "market")
               const color = provinceData < middleData ?  computeMinMiddle(xScale(provinceData)) : computeMiddleMax(yScale(provinceData))
               return color
           })
           .on("mouseover", function(d) {
               d3.select(this).attr("fill", "#FAA700")
           })
           .on("mouseout", function(d) {
                const provinceData = sourceData.getCurProvinceData(d.properties.name, "market")
                const color = provinceData < middleData ?  computeMinMiddle(xScale(provinceData)) : computeMiddleMax(yScale(provinceData))
                d3.select(this).attr("fill", color)
           })
           .on("click", function(d) {
            console.log("this province", d.properties.name)
            // 调用父页面的方法
            if (parent.window.changeProvince ){

                parent.window.changeProvince(d.properties.name)
            }
        });
        
        // EI > 100 的省份绘制黑色三角形
        gs.append("polyline")
           .attr("points", d => {
            const provinceEI = sourceData.getCurProvinceData(d.properties.name, "EI")
            const p = projection(d["properties"]["cp"])
            const x = p[0]
            const y = p[1]
               if (provinceEI > 100) {
                   return `${x},${y} ${x+10},${y} ${x+5},${y-10}`
               } else {
                   return "0,0"
               }
           })
           .attr("stroke", "black")
           .attr("fill", "black")
           .attr("x", function(d) {
                const p = projection(d["properties"]["cp"])
                return p[0]
            })
            .attr("y", function(d) {
                const p = projection(d["properties"]["cp"])
                return p[1]
            });
            
        // 左下角南海地图
        const southseaSVG = svg.append("svg")
                                .attr("height", "150")
                                .attr("width", "120")
                                .attr("x", ivp.x + ivp.w - 100 )
                                .attr("y", ivp.y + ivp.h - 70)
                                
                                
        const southsea = southseaSVG.append("g")
                                    .attr("transform", "scale(0.4)")
                                
        
        // x1, y1, x2, y2
        const southseaData = [
            { y2:"7", x2:"145", y1:"7", x1: "20", type: "line" },
            { y2:"24", x2:"6", y1:"7", x1:"20", type: "line" },
            { y2:"195", x2: "145", y1: "7", x1:"145", type: "line" },
            { y2:"195", x2:"6", y1: "24", x1: "6", type: "line"},
            { y2:"195", x2:"145", y1: "195", x1: "6", type: "line"},
            { d: "m6,31.5l9,7.5l15,9l15,4l18,0l17,-14l21,-31L20,7L6,24z", type: "path"},
            { d: "m113,7l10,25l11,-25z", type: "path"},
            { d: "m46.5,66.5l14.5,-6.5l-1,13l-7,7l-15,4l8.5,-17.5z", type: "path"},
            { y2:"46.5", x2:"132.5", y1: "31.5", x1: "141.5", type: "line" },
            { y2:"76.5", x2:"115.5", y1:"61.5", x1:"121.5", type: "line" },
            { y2:"111.5", x2:"110.5", y1:"92.5", x1:"110.5", type: "line" },
            { y2:"147.5", x2:"101.5", y1:"127.5", x1:"108.5", type: "line"},
            { y2:"177.5", x2:"78.5", y1:"163.5", x1:"91.5", type: "line"},

            { y2:"188.5", x2:"39.5", y1:"184.5", x1:"54.5", type: "line"},
            { y2:"158.5", x2:"11.5", y1:"172.5", x1:"17.5", type: "line"},
            { y2:"132.5", x2:"39.5", y1:"142.5", x1:"24.5", type: "line"},
            { y2:"98.5", x2:"37.5", y1:"113.5", x1:"40.5", type: "line"},

        ]

        const lines = southseaData.filter(it => { return it.type === "line" })
        const paths = southseaData.filter(it => { return it.type === "path" })
        southsea.selectAll("line.southSeaLine")
                .data(lines)
                .enter()
                .append("line")
                .attr("x1", d => d.x1)
                .attr("y1", d => d.y1)
                .attr("x2", d => d.x2)
                .attr("y2", d => d.y2)
                .attr("stroke", "#EBECF0")
                

        southsea.selectAll("path.southSeaPath")
                .data(paths)
                .enter()
                .append("path")
                .attr("d", d => d.d)
                .attr("fill", "#B3BAC5")


        if (this.theme.hasLabel()) {
            const l = this.theme.queryLabel()
            l.render(svg, this.source, xScale, yScale)
        }
    }
}