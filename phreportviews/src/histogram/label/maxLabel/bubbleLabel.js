import { label } from "../defaultlabel";

export class BubbleLabel extends label {
    constructor() {
        super()
    }

    render(svg, ivp) {
        svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivp.w/2 + 20}, ${ivp.h + 60})`)
            .text("EI > 100")

        svg.append("rect")
            .attr("fill", "#f5d139")
            .attr("width", "8")
            .attr("height", "8")
            .attr("transform", `translate(${ivp.w/2 - 8 - 8 + 20}, ${ivp.h + 60 - 8})`)
            .attr("rx", "2")
            .attr("ry", "2")
            // 第一个 8 减去rect自身的宽度
            // 第二个 8 是和text的间距
            // 20 是为了位置居中进行的偏移
    }
}

export default new BubbleLabel ()