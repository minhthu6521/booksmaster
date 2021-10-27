import React from "react";
import {backend_url, content_api} from "../variables";
import {Link, Route, Switch} from "react-router-dom";
import ReactWordcloud from "react-wordcloud";

export default class WordCloud extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            words: [],
            options: {
                rotations: 1,
                rotationAngles: [0, 0],
                enableOptimizations: true,
                spiral: "archimedean",
            },
            showWordsForSelection: false
        };
    }

    componentDidMount() {
        if (this.props.bookId && this.state.words.length === 0) {
            const getWordCount = fetch(`${content_api}/books/${this.props.bookId}/contents/wordcloud`,
                {
                    keepalive: true
                });
            getWordCount.then(res => res.json()).then(data => {
                this.setState(data)
            })
        }
    }

    showWordSelection = () => {
        const current = this.state.showWordsForSelection
        this.setState({showWordsForSelection: !current})
    }

    render() {
        let items = [];
        for (const value of this.state.words) {
            items.push(<div>
                <input type="checkbox"
                       id={value.text}
                       name={value.text}
                       defaultChecked={!value.unchecked}/>
                <label htmlFor={value.text}>{value.text}</label>
            </div>)
        }
        return (<div>
            <h3>Word cloud</h3>
            <button onClick={this.showWordSelection}>Select words to remove from Word Cloud</button>
            {this.state.showWordsForSelection ? (
                <div>{items}</div>
            ) : (<div></div>)}
            <div style={{height: 600, width: 600}}><ReactWordcloud words={this.state.words}
                                                                   options={this.state.options}/></div>
        </div>)
    }
}