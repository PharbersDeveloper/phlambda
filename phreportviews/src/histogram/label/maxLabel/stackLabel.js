import { label } from "../defaultlabel";

export class StackLabel extends label {
    constructor() {
        super()
    }

    // 为什么方法名为 render 的时候就执行两遍
    renderStackLabel(svg, ivpInfo, labelData, colors) {
        const infogs = svg.append("g")
                        .attr("transform", `translate(${ivpInfo.bottom.x}, 0)`)

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
                const n = labelData.length
                const width = (ivpInfo.bottom.w)/4
                const pos = i % 4
                const x = pos * width
                let offset = 0
                if (n >= 4) {
                    const curLines = Math.floor(i/4)
                    offset =  (curLines - 1) * 24                    
                    return `translate(${ivpInfo.left.w + x }, ${ivpInfo.bottom.y + offset })`
                } else {
                    offset = (4 - n) * width / 2
                    return `translate(${ivpInfo.left.w + x + offset }, ${ivpInfo.bottom.y })`
                }
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
                const n = labelData.length
                const width = (ivpInfo.bottom.w)/4
                const pos = i % 4
                const x = pos * width
                let offset = 0
                if (n >= 4) {
                    const curLines = Math.floor(i/4)
                    offset =  (curLines - 1) * 24                 
                    return `translate(${ivpInfo.left.w + x + 20 }, ${ivpInfo.bottom.y + 8 + offset })`
                } else {
                    offset = (4 - n) * width / 2
                    return `translate(${ivpInfo.left.w + x + 20 + offset }, ${ivpInfo.bottom.y + 8 })`
                }
            })
            .attr("font-size", 12)


    }
}

export default new StackLabel ()