import { label } from "../defaultlabel";

export class BarLineLabel extends label {
    constructor() {
        super()
    }

    // 为什么方法名为 render 的时候会先去调用label的方法
    renderBarLineLabel(svg, ivpInfo, labelData, colors) {
        const infogs = svg.append("g")
                .attr("transform", `translate(${ivpInfo.bottom.x + ivpInfo.bottom.w/2 - 196}, ${ivpInfo.bottom.y + ivpInfo.bottom.h/2})`)
        
        infogs.selectAll("rect")
            .data(labelData)
            .enter()
            .append("rect")
            .attr("width", 8)
            .attr("height", 8)
            .attr("fill", function(d, i) {
                return colors[i]
            })
            .attr("transform", function(d, i) {
                const pos = i * (80 + 24)              
                return `translate(${ivpInfo.left.x + pos }, 0)`
            })
            .attr("rx", "2")
            .attr("ry", "2")

        infogs.selectAll("text")
            .data(labelData)
            .enter()
            .append("text")
            .text(function(d) {
                return d
            })
            .attr("fill", "#7A869A")
            .attr("transform", function(d, i) {
                const pos = i * (80 + 24)              
                return `translate(${ivpInfo.left.x + pos + 20 }, 8)`
            })
            .attr("font-size", 12)
    }
}

export default new BarLineLabel ()