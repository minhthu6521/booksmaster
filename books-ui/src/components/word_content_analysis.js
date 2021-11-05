import React from "react";
import {content_api} from "../variables";
import ReactWordcloud from "react-wordcloud";
import {HistogramHandler} from "./statistics";

export default class ContentAnalysis extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            words: [],
            options: {
                rotations: 1,
                rotationAngles: [0, 0],
                enableOptimizations: true,
                spiral: "archimedean",
                fontSizes: [12, 45]
            },
            showWordsForSelection: false
        };
    }

    componentDidMount() {
        if (this.props.bookId && this.state.words.length === 0) {
            const getWordCount = fetch(`${content_api}/books/${this.props.bookId}/contents/wordcloud?min=1`,
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

    changeWordToShow = (event) => {
        let result = this.state.words.map(obj => {
            return {
                text: obj.text,
                value: obj.value,
                occurrence: obj.occurrence,
                unchecked: event.target.name == obj.text ? !obj.unchecked : obj.unchecked
            }
        })
        this.setState({words: result})
    }

    render() {
        if (this.state.words.length) {
            let words_to_select = [],
                words_to_show = [];
            for (const value of this.state.words) {
                words_to_select.push(<div key={value.text}>
                    <input type="checkbox"
                           id={value.text}
                           name={value.text}
                           defaultChecked={!value.unchecked}
                           onChange={this.changeWordToShow}/>
                    <label htmlFor={value.text}>{value.text} - Occurrence: {value["occurrence"]}</label>
                </div>)
                if (!value.unchecked) {
                    words_to_show.push(value)
                }
            }
            return (<div>
                <h3>Word cloud</h3>
                <button onClick={this.showWordSelection}>Select words to remove from Analysis</button>
                {this.state.showWordsForSelection ? (
                    <div>{words_to_select}</div>
                ) : (<div></div>)}
                <div style={{display: "inline-flex", flex: "wrap"}}>
                    <ReactWordcloud
                        style={{height: 600, width: 600}}
                        words={words_to_show}
                        options={this.state.options}/>
                    <HistogramHandler data={words_to_show} display_configuration={{width: 600, height:600}}/>
                </div>
            </div>)
        }
        return (<div></div>)
    }
}