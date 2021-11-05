import React, {useEffect, useRef} from "react";
import {backend_url} from "../variables";
import BarChart from "./lib/bar_chart";
import Histogram from "./lib/histogram";
import AreaChart from "./lib/area_chart";
import * as d3 from "d3";
import PieChart from "./lib/pie_chart";

const components = {
    bar_chart: BarChartHandler,
    histogram: Histogram,
    area_chart: AreaChart,
    pie_chart: PieChartHandler,
    text: TextItem
}

class Statistics extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items_conf: []
        }
    }

    componentDidMount() {
        const getConfiguration = fetch(`${backend_url}/${this.props.getUrl}`);
        getConfiguration.then(res => res.json()).then(data => {
            this.setState({items_conf: data})

        })
    }

    render() {
        const items = [];
        for (const item of this.state.items_conf) {
            items.push(<StatItem key={item.id} {...item}/>)
        }
        return (
            <div className="statBoard">{items}</div>
        )
    }

}


class StatItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null
        }
    }

    componentDidMount() {
        const getData = fetch(`${backend_url}/api/statistics/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.props.query_configuration)
        });
        getData.then(res => res.json()).then(data => {
            this.setState({"data": data})

        })
    }

    render() {
        const Item = components[this.props.display_configuration.type];
        return (
            <div className="statItem">
                <h3>{this.props.display_configuration.title}</h3>
                {this.state.data ? <Item data={this.state.data} {...this.props}/> : <div></div>}
            </div>
        )
    }
}

function TextItem(props) {
    const key = props.display_configuration.item ? props.display_configuration.item : props.query_configuration.gets[0].label.replace(/\s+/g, '_').toLowerCase();
    return (
        <p>{props.data[0][key]}</p>
    )
}

function BarChartHandler(props) {
    const svg = useRef(null);
    useEffect(() => {
        let data = props.data;
        let xAxis = props.display_configuration.xAxis,
            yAxis = props.display_configuration.yAxis;
        let chart = BarChart(data, {
            x: d => d[xAxis],
            y: d => d[yAxis],
            xDomain: d3.groupSort(data, ([d]) => -d[yAxis], d => d[xAxis]),
            yLabel: props.display_configuration.yAxisLabel,
            color: "steelblue",
            width: props.display_configuration.width
        })
        svg.current.appendChild(chart)
    }, [])
    return (
        <div ref={svg}/>
    )
}


function PieChartHandler(props) {
    const svg = useRef(null);
    useEffect(() => {
        let data = props.data;
        let name = props.display_configuration.name,
            value = props.display_configuration.value;
        let chart = PieChart(data, {
            name: d => d[name],
            value: d => d[value]
        })
        svg.current.appendChild(chart)
    }, [])
    return (
        <div ref={svg}/>
    )
}

function HistogramHandler(props) {
    const svg = useRef(null);
    useEffect(() => {
        let data = props.data;
        let chart = Histogram(data, {
            value: d => d.value,
            color: "steelblue",
            label: "Number of times repeated →"
        })
        svg.current.appendChild(chart)
    }, [])
    return (
        <div ref={svg}/>
    )
}

export {
    Statistics,
    PieChartHandler,
    TextItem,
    StatItem,
    BarChartHandler,
    HistogramHandler
}