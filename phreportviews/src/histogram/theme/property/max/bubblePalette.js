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
                .attr("stop-color", "rgba(245,209,57,0.65)")
        EIRadia.append("stop")
                .attr("offset", "87%")
                .attr("stop-color", "rgba(232,166,6,0.65)")

        // const circleShadow = svg.select("defs")
        //                         .append('svg:filter')
        //                         .attr('id', 'drop-shadow')
        //                         .attr('filterUnits', "userSpaceOnUse")
        //                         .attr('width', '100%')
        //                         .attr('height', '100%');
        // circleShadow.append('svg:feGaussianBlur')
        //     .attr('in', 'SourceGraphic')
        //     .attr('stdDeviation', 1)
        //     .attr('result', 'blur-out');
        // circleShadow.append('svg:feOffset')
        //     .attr('in', 'color-out')
        //     .attr('dx', 3)
        //     .attr('dy', 3)
        //     .attr('result', 'the-shadow');
        // circleShadow.append('svg:feBlend')
        //     .attr('in', 'SourceGraphic')
        //     .attr('in2', 'the-shadow')
        //     .attr('mode', 'normal');
    }
}

export default new BubblePalette()
