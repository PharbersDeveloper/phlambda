import { label } from "../defaultlabel";

export class BarLineLabel extends label {
    constructor() {
        super()
    }

    // 为什么方法名为 render 的时候会先去调用label的方法
    renderBarLineLabel(svg, ivpInfo, labelData, colors) {
        console.log("在这里?", ivpInfo)
        // labels
        const infogs = svg.append("g")
            .attr("transform", `translate(${ivpInfo.bottom.x + ivpInfo.bottom.w/4}, 0)`)
        
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
                const x = (i + 1) * 24 + i * (ivpInfo.bottom.w - 24*4)/8
                let offset = 0
                if (labelData.length > 4) {
                    offset =  (4 - labelData.length ) * x / 2 
                }
                return `translate(${ivpInfo.bottom.x + x }, ${ivpInfo.bottom.y  })`
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
                const x = (i + 1) * 24 + i * (ivpInfo.bottom.w - 24*4)/8
                let offset = 0
                if (labelData.length > 4) {
                    offset =  (4 -labelData.length ) * x / 2 
                }
                return `translate(${ivpInfo.bottom.x + x + 20 }, ${ivpInfo.bottom.y + 8})`
            })
            .attr("font-size", 12)
    }
}

export default new BarLineLabel ()