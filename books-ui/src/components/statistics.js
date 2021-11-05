import React, {useEffect, useRef} from "react";
import {backend_url} from "../variables";
import BarChart from "./bar_chart";
import Histogram from "./histogram";
import AreaChart from "./area_chart";
import * as d3 from "d3";
import PieChart from "./pie_chart";

const components = {
    bar_chart: BarChartHandler,
    histogram: Histogram,
    area_chart: AreaChart,
    pie_chart: PieChart,
    text: TextItem
}

export default class Statistics extends React.Component {
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
            <div>{items}</div>
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
            this.state.data ? <Item className="statItem" data={this.state.data} {...this.props}/> : <div></div>
        )
    }
}

function TextItem(props) {
    const key = props.display_configuration.item ? props.display_configuration.item : props.query_configuration.gets[0].label.replace(/\s+/g, '_').toLowerCase();
    return <div>
        <h3>{props.display_configuration.title}</h3>
        <p>{props.data[0][key]}</p>
    </div>
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
            height: 500,
            width: 1000,
            color: "steelblue"
        })
        svg.current.appendChild(chart)
    }, [])
    return (
        <div>
            <div ref={svg}/>
        </div>
    )
}