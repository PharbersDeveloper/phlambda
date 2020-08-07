import { Palette } from "../palette";

export class BubblePalette extends Palette {
    constructor() {
        super()
    }

    renderRadia(svg) {
         // 定义circle的颜色，使用 radial-gradient 渐变
         const defaultRadia =  svg.append("defs")
                                .append("radialGradient")
                                .attr("id", "defaultEI")

        defaultRadia.append("stop")
                    .attr("offset", "23%")
                    .attr("stop-color", "rgba(225,231,234,0.65)")

        defaultRadia.append("stop")
                    .attr("offset", "87%")
                    .attr("stop-color", "rgba(181,196,202,0.65)")


        const EIRadia = svg.select("defs")
                        .append("radialGradient")
                        .attr("id", "EIRadia")

        EIRadia.append("stop")
                .attr("offset", "23%")
                .attr("stop-color", "rgba(171,228,27,0.65)")
        EIRadia.append("stop")
                .attr("offset", "87%")
                .attr("stop-color", "rgba(120,160,19,0.65)")
    }
}

export default new BubblePalette()
