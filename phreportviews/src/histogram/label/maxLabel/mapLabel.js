import { label } from "../defaultlabel";

export class MapLabel extends label {
    constructor() {
        super()
    }

    renderMapLabel(svg, ivpInfo, data) {
    
        // EI > 100 提示
        svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivpInfo.left.x + 20}, ${ivpInfo.left.y + ivpInfo.left.h - 20})`)
            .text("EI > 100")

        // EI triangle
        svg.append("polyline")
            .attr("points", function() {
                const x = ivpInfo.left.x 
                const y = ivpInfo.left.y  + ivpInfo.left.h - 20

                console.log("!!!", `${x},${y} ${x+10},${y} ${x+5},${y-10}`)
                return `${x},${y} ${x+10},${y} ${x+5},${y-10}`
                
            })
            .attr("stroke", "black")
            .attr("fill", "black")
            .attr("x", function() {
                return ivpInfo.left.x 
            })
             .attr("y", function() {
                 return  ivpInfo.left.y - 20

            });

        // 颜色渐变矩形
        const rectColor = svg.append("defs")
            .append("linearGradient")
            .attr("id", "mapLinerColorGradient")
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '0%')
            .attr('y2', '100%')
        rectColor.append("stop")
            .attr("offset", "0")
            .attr("stop-color", "rgba(139,113,5,1)")
        rectColor.append("stop")
            .attr("offset", "50%")
            .attr("stop-color", "rgba(248,203,18,1)")
        rectColor.append("stop")
                .attr("offset", "100%")
                .attr("stop-color", "rgba(252,233,157,1)")
        

        svg.append("rect")
            .attr("height", "64")
            .attr("width", 16)
            .attr("x", function() {
                const x = ivpInfo.left.x 
                return x 
            })
            .attr("y", function() {
                const y = ivpInfo.left.y  + ivpInfo.left.h - 20
                return y - 100
            })
            .attr("fill", "url(#mapLinerColorGradient)")

        // 矩形右侧显示的最小值
        svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivpInfo.left.x + 20}, ${ivpInfo.left.y + ivpInfo.left.h - 48})`)
            .text(Math.ceil(data.min/1000000) + "(Mn)")

        // 矩形右侧显示的最大值
        svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivpInfo.left.x + 20}, ${ivpInfo.left.y + ivpInfo.left.h - 110})`)
            .text(Math.ceil(data.max/1000000) + "(Mn)")

        // 矩形上方显示的文字说明
        svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivpInfo.left.x }, ${ivpInfo.left.y + ivpInfo.left.h - 130})`)
            .text("市场规模")
    }
}

export default new MapLabel ()