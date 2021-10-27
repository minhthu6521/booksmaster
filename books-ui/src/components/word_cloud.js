import React from "react";
import {backend_url, content_api} from "../variables";
import {Link, Route, Switch} from "react-router-dom";
import ReactWordcloud from "react-wordcloud";

export default class WordCloud extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            words: []
        };
    }

    componentDidMount() {
        if(this.props.bookId && this.state.words.length === 0) {
            const getWordCount = fetch(`${content_api}/books/${this.props.bookId}/contents/wordcloud`,
                {
                    keepalive:true
                });
            getWordCount.then(res => res.json()).then(data => {
                this.setState(data)
            })
        }
    }

    render() {
        return (<div>
            <h3>Word cloud</h3>
            <ReactWordcloud words={this.state.words}/>
        </div>)
    }
}