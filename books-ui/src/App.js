import './App.css';
import Books from './components/books.js'

import React from "react";
import {BrowserRouter as Router, Link, Route, Switch} from "react-router-dom";
import Genres from "./components/genre";

export default class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <ul>
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        <li>
                            <Link to='/books'>Books</Link>
                        </li>
                        <li>
                            <Link to='/genres'>Genres</Link>
                        </li>
                    </ul>

                    <Switch>
                        <Route path="/books">
                            <Books/>
                        </Route>
                        <Route path="/genres">
                            <Genres/>
                        </Route>
                        <Route path="/">
                            <Home/>
                        </Route>
                    </Switch>
                </div>
            </Router>
        );
    }
}

function Home() {
    return <h2>Home</h2>;
}


