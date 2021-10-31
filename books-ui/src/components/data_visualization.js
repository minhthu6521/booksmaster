import {useEffect, useRef, useState} from 'react';
import Histogram from "./histogram";
import * as d3 from "d3";

export default function DataVisualization(props) {
    const svg = useRef(null);
    useEffect(() => {
        let data = props.dataSet
        let chart = Histogram(data, {
            value: d => d.value,
            width: 600,
            height: 500,
            color: "steelblue",
            label: "Number of times repeated →"
        })
        svg.current.appendChild(chart)
    }, [])
    return (
        <div>
            <div id="occurrence-of-words">
                <div ref={svg}/>
            </div>
        </div>
    )
}


/*
        var svg = d3.select("#svg svg"),
            margin = 200,
            width = svg.attr("width") - margin,
            height = svg.attr("height") - margin;


        var xScale = d3.scaleBand().range([0, width]).padding(0.4),
            yScale = d3.scaleLinear().range([height, 0]);

        var g = svg.append("g")
            .attr("transform", "translate(" + 100 + "," + 100 + ")");
        xScale.domain(data.map(function (d) {
            return d.text;
        }));
        yScale.domain([0, d3.max(data, function (d) {
            return d.value;
        })]);

        g.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(xScale));

        g.append("g")
            .call(d3.axisLeft(yScale).tickFormat(function (d) {
                return d;
            }).ticks(10))
            .append("text")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("value");

        g.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                return xScale(d.text);
            })
            .attr("y", function (d) {
                return yScale(d.value);
            })
            .attr("width", xScale.bandwidth())
            .attr("height", function (d) {
                return height - yScale(d.value);
            });
*/
