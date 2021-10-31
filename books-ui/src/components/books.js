import React from "react";
import {backend_url} from "../variables";
import {Link, Route, Switch} from "react-router-dom";
import ContentAnalysis from "./word_content_analysis";
import ReactStars from "react-rating-stars-component"

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
            items.push(<li key={value["id"]}>
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

    toggleEditView = () => {
        const current = this.state.isEdited
        this.setState({isEdited: !current})
    }

    handleSubmit = (value) => {
        const editHandler = fetch(`${backend_url}/api/books/${this.state.id}`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: this.state.id,
                    ...value
                })
            })
        editHandler.then(res => res.json()).then(data => {
            this.setState(data)
        })
    }
    ratingChanged = (newRating) => {
        const editHandler = fetch(`${backend_url}/api/books/${this.state.id}/ratings/${newRating}`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
        editHandler.then(res => res.json()).then(data => {
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
            <button onClick={this.toggleEditView}>Edit metadata</button>
            {this.state.isEdited ? (
                <BookEditForm bookId={this.state.id} item={this.state} handleSubmit={this.handleSubmit}/>
            ) : (
                <div>
                    <h3>{this.state.title}</h3>
                    <div dangerouslySetInnerHTML={{__html: this.state.description}} ></div>
                    <div>Rating: {this.state.current_user_rating}<ReactStars
                        count={5}
                        onChange={this.ratingChanged}
                        size={24}
                        isHalf={true}
                        value={this.state.current_user_rating}
                        activeColor="#ffd700"
                    /></div>
                </div>
            )}
            <div><label>Author: </label>{authors}</div>
            {genres && <div><label>Genres: </label>{genres}</div>}
            <ContentAnalysis bookId={this.state.id}/>
        </div>;
    }
}

class BookEditForm extends React.Component {
    constructor(props) {
        super(props);
    }

    onSubmit = (event) => {
        event.preventDefault()
        const data = {
            title: event.target.title.value,
            description: event.target.description.value
        }
        this.props.handleSubmit(data)
    }


    render() {
        if (this.props.item) {
            return (
                <form onSubmit={this.onSubmit}>
                    <div><label>
                        Title:
                        <input
                            type="text"
                            name="title"
                            defaultValue={this.props.item.title || ""}
                            ref={node => (this.inputNode = node)}
                        />
                    </label></div>
                    <div><label>
                        Description:
                        <textarea
                            name="description"
                            defaultValue={this.props.item.description || ""}
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