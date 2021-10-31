import React from "react";
import {backend_url} from "../variables";
import {Link, Route, Switch} from "react-router-dom";

export default class Genres extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            genres: []
        };
    }

    componentDidMount() {
        const getGenres = fetch(`${backend_url}/api/genres`);
        getGenres.then(res => res.json()).then(data => {
            this.setState({genres: data})
        })
    }


    render() {
        let items = [];
        for (const value of this.state.genres) {
            items.push(<li key={value["id"]}>
                <Link to={`/genres/${value["id"]}`}>
                    {value["name"]}
                </Link>
            </li>)
        }
        return (
            <div>
                <h2><Link to={`/genres`}>Genres</Link></h2>
                <Switch>
                    <Route path={`/genres/:genreId`} component={Genre}/>
                    <Route path={`/genres`}>
                        <ul>
                            {items}
                        </ul>
                    </Route>
                </Switch>
            </div>
        );
    }
}


class Genre extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            books: []
        };
    }

    componentDidMount() {
        const getGenre = fetch(`${backend_url}/api/genres/${this.props.match.params.genreId}`);
        getGenre.then(res => res.json()).then(data => {
            console.log(data);
            this.setState(data)
        })
    }

    render() {
        let books = []
        for (const book of this.state.books) {
            books.push(<Link to={`/books/${book.id}`}>
                {book.title}
            </Link>)
        }
        return <div key={this.state.id}>
            <h3>{this.state.name}</h3>
            <div>{books}</div>
        </div>;
    }
}