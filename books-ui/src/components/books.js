import React from "react";
import {backend_url} from "../variables";
import {Link, Route, Switch} from "react-router-dom";

export default class Books extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            books: []
        };
    }

    componentDidMount() {
        const getBooks = fetch(`${backend_url}/api/books`);
        getBooks.then(res => res.json()).then(data => {
            this.setState({books: data})
        })
    }

    render() {
        let items = [];
        for (const value of this.state.books) {
            items.push(<li  key={value["id"]}>
                <Link to={`/books/${value["id"]}`}>
                    {value["title"]}
                </Link>
            </li>)
        }
        return (
            <div>
                <h2><Link to={`/books`}>Books</Link></h2>
                <Switch>
                    <Route path={`/books/:bookId`} component={Book}/>
                    <Route path={`/books`}>
                        <ul>
                            {items}
                        </ul>
                    </Route>
                </Switch>
            </div>
        );
    }
}

class Book extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            authors: [],
            genres: []
        };
    }

    componentDidMount() {
        const getBooks = fetch(`${backend_url}/api/books/${this.props.match.params.bookId}`);
        getBooks.then(res => res.json()).then(data => {
            this.setState(data)
        })
    }

    render() {
        const authors = [], genres = [];
        for (const {first_name, last_name} of this.state.authors) {
            authors.push(<p key={`author_${first_name}`}>
                {first_name} {last_name}
            </p>)
        }
        for (const {name} of this.state.genres) {
            genres.push(<p>
                {name}
            </p>)
        }
        return <div key={this.state.id}>
            <h3>{this.state.title}</h3>
            <div><label>Author: </label>{authors}</div>
            { genres && <div><label>Genres: </label>{genres}</div>}
        </div>;
    }
}
