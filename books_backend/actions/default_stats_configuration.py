DEFAULT_MAIN_STATISTICS_PAGE_CONFIGURATION = [
    {
        "id": "default0",
        "query_configuration": {
            "gets": [{
                "name": "books.id",
                "operation": ["count"],
                "label": "number_of_books"
            }]
        },
        "display_configuration": {
            "title": "Total number of books",
            "type": "text"
        }
    },
    {
        "id": "default1",
        "query_configuration": {
            "gets": [
                {
                    "name": "books.content_length",
                    "operation": ["avg"],
                    "label": "Average book length"
                }
            ]
        }
    },
    {
        "id": "default1",
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
                "items": [{
                    "item": {
                        "name": "genre.name",
                        "label": "Genre"
                    },
                    "clause": "not equal",
                    "value": "(empty)"
                }
                ],
                "operation": "and"

            },
            "groups": [
                {
                    "name": "genre.name"
                }
            ]
        }
    }
]

DEFAULT_BOOK_STATISTICS_PAGE_CONFIGURATION = [

]
