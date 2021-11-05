DEFAULT_MAIN_STATISTICS_PAGE_CONFIGURATION = [
    {
        "id": "count_book_num",
        "query_configuration": {
            "gets": [{
                "name": "books.id",
                "operation": ["count"],
                "label": "Number of books"
            }]
        },
        "display_configuration": {
            "title": "Number of books",
            "type": "text"
        }
    },
    {
        "id": "number_of_author_text",
        "query_configuration": {
            "gets": [{
                "name": "author.id",
                "operation": ["count"],
                "label": "Number of authors"
            }]
        },
        "display_configuration": {
            "title": "Number of authors",
            "type": "text"
        }
    },
    {
        "id": "number_of_genre_text",
        "query_configuration": {
            "gets": [{
                "name": "genre.id",
                "operation": ["count"],
                "label": "Number of genres"
            }]
        },
        "display_configuration": {
            "title": "Number of genres",
            "type": "text"
        }
    },
    {
        "id": "most_read_genres",
        "query_configuration": {
            "gets": [
                {
                    "name": "books.id",
                    "operation": ["count"],
                    "label": "Number of Books"
                },
                {
                    "name": "genre.name",
                    "label": "Genre"
                }
            ],
            "orders": [
                {
                    "item": {
                        "name": "books.id",
                        "operation": ["count"]
                    },
                    "direction": "desc"
                }
            ],
            "limit": 10,
            "groups": [
                {
                    "name": "genre.name"
                }
            ],
            "filters": {
                "items": [
                    {
                        "item": {
                            "name": "genre.name",
                            "label": "Genre"
                        },
                        "clause": "not equal",
                        "value": "(empty)"
                    },
                ],
                "operation": "and"

            }
        },
        "display_configuration": {
            "title": "Most read genres",
            "type": "pie_chart",
            "name": "genre",
            "value": "number_of_books"
        }

    },
    {
        "id": "count_book_language",
        "query_configuration": {
            "gets": [
                {
                    "name": "books.id",
                    "operation": ["count"],
                    "label": "Number of books"
                },
                {
                    "name": "books.language",
                    "label": "Language"
                }
            ],
            "groups": [
                {
                    "name": "books.language"
                }
            ],
            "filters": {
                "items": [
                    {
                        "item": {
                            "name": "books.language",
                            "label": "Language"
                        },
                        "clause": "not equal",
                        "value": "(empty)"
                    },
                ],
                "operation": "and"

            }
        },
        "display_configuration": {
            "title": "Number of books by language",
            "type": "pie_chart",
            "name": "language",
            "value": "number_of_books"
        }

    },
    {
        "id": "average_num_words_per_text",
        "query_configuration": {
            "gets": [
                {
                    "name": "books.content_length",
                    "operation": ["avg"],
                    "label": "Average book length"
                }
            ]
        },
        "display_configuration": {
            "title": "Average number of words per book",
            "type": "text"
        }
    },
    {
        "id": "average_num_words_per_genre",
        "query_configuration": {
            "gets": [
                {
                    "name": "books.content_length",
                    "operation": ["avg"],
                    "label": "Average book length"
                },
                {
                    "name": "genre.name",
                    "label": "Genre"
                }
            ],
            "filters": {
                "items": [
                    {
                        "item": {
                            "name": "genre.name",
                            "label": "Genre"
                        },
                        "clause": "not equal",
                        "value": "(empty)"
                    },
                ],
                "operation": "and"

            },
            "groups": [
                {
                    "name": "genre.name"
                }
            ],
            "limit": 10,
            "orders": [
                {
                    "item": {
                        "name": "books.id",
                        "operation": ["count"]
                    },
                    "direction": "desc"
                }
            ]
        },
        "display_configuration": {
            "title": "Average number of words per book per genre",
            "type": "bar_chart",
            "xAxis": "genre",
            "yAxisLabel": "Average book length",
            "yAxis": "average_book_length",
            "width": "1100",
            "height": "500"
        }
    }
]

DEFAULT_BOOK_STATISTICS_PAGE_CONFIGURATION = [

]
