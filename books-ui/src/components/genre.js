import React from "react";
import {backend_url} from "../variables";
import {Link, Route, Switch} from "react-router-dom";
import {FaTrash} from "react-icons/fa";

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

    deleteGenre = (event) => {
        event.preventDefault()
        console.log(event.target.dataset.genre_id)
        const deleteHandler = fetch(`${backend_url}/api/genres/${event.target.dataset.genre_id}`,
            {
                method: 'DELETE'
            })
        window.location.reload();
    }


    render() {
        let items = [];
        for (const value of this.state.genres) {
            items.push(<li key={value["id"]}>
                <Link to={`/genres/${value["id"]}`}>
                    {value["name"]}
                </Link>
                <span>           </span>
                <span><button onClick={this.deleteGenre} data-genre_id={value["id"]}> <FaTrash/></button></span>
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

    toggleEditView = () => {
        const current = this.state.isEdited
        this.setState({isEdited: !current})
    }


    handleSubmit = (value) => {
        const editHandler = fetch(`${backend_url}/api/genre/${this.state.id}`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ...value
                })
            })
        editHandler.then(res => res.json()).then(data => {
            this.setState(data)
        })
    }

    componentDidMount() {
        const getGenre = fetch(`${backend_url}/api/genres/${this.props.match.params.genreId}`);
        getGenre.then(res => res.json()).then(data => {
            this.setState(data)
        })
    }

    render() {
        let books = []
        for (const book of this.state.books) {
            books.push(<p><Link to={`/books/${book.id}`}>
                {book.title}
            </Link></p>)
        }
        return <div key={this.state.id}>
            <button onClick={this.toggleEditView}>Edit metadata</button>
            {this.state.isEdited ? (
                <GenreEditForm genreId={this.state.id} item={this.state} handleSubmit={this.handleSubmit}/>
            ) : (
                <h3>{this.state.name}</h3>)}
            <div>{books}</div>
        </div>;
    }
}

class GenreEditForm extends React.Component {
    constructor(props) {
        super(props);
    }

    onSubmit = (event) => {
        event.preventDefault()
        const data = {
            name: event.target.name.value
        }
        this.props.handleSubmit(data)
    }


    render() {
        if (this.props.item) {
            return (
                <form onSubmit={this.onSubmit}>
                    <div><label>
                        Name:
                        <input
                            type="text"
                            name="name"
                            defaultValue={this.props.item.name || ""}
                            ref={node => (this.inputNode = node)}
                        />
                    </label></div>
                    <button type="submit">Submit</button>
                </form>
            )
        }
        return (<div></div>)
    }
}