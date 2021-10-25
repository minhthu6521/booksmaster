import logo from './logo.svg';
import './App.css';
import {backend_url, content_api} from './variables.js'

import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    useRouteMatch,
    useParams
} from "react-router-dom";

export default function App() {
    return (
        <Router>
            <div>
                <ul>
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                </ul>

                <Switch>
                    <Route path="/books">
                        <Books/>
                    </Route>
                    <Route path="/">
                        <Home/>
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}

function Home() {
    return <h2>Home</h2>;
}

class Books extends React.Component {
    constructor(props) {
        super(props);
        this.state = {books: []};
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
            items.push(<li>
                <Link to={`books/${value["id"]}`}>
                    {value["title"]}
                </Link>
            </li>)
        }
        return (
            <div>
                <h2>Books</h2>
                <ul>
                    {items}
                </ul>

                <Switch>
                    <Route path={`books/:bookId`}>
                        <Book/>
                    </Route>
                    <Route path="/books">
                        <h3>Please select a topic.</h3>
                    </Route>
                </Switch>
            </div>
        );
    }
}

function Book() {
    let {bookId} = useParams();
    return <h3>Requested topic ID: {bookId}</h3>;
}

