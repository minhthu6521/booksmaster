import './App.css';
import Books from './components/books.js'

import React from "react";
import {BrowserRouter as Router, Link, Route, Switch} from "react-router-dom";

export default class App extends React.Component {
    render() {
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
}

function Home() {
    return <h2>Home</h2>;
}


