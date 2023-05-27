from fastapi import FastAPI, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status
# uvicorn books.books:app --reload

app = FastAPI()

# BOOKS = [
#     {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
#     {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
#     {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
#     {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
#     {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
#     {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
# ]

class Book:
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: int
    year: int

    def __init__(self, id:int, title: str, author: str, category: str, description: str, rating: int, year: int):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.description = description
        self.rating = rating
        self.year = year

class BookRequest(BaseModel):

    id: int = Field(title="ID not required")
    title: str = Field(..., min_length=3, max_length=50)
    author: str = Field(..., min_length=3, max_length=50)
    category: str = Field(..., min_length=3, max_length=10)
    description: str = Field(..., min_length=3, max_length=50)
    rating: int = Field(..., ge=1, le=5)
    year: int = Field(..., ge=2000, le=2030)

    class Config:
        schema_extra = {
            "example": {
                "title": "Title 7",
                "author": "Author 7",
                "category": "Category",
                "description": "Book Description",
                "rating": 5,
                "year": 2025
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'Andrew', 'Coding', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'Andrew', 'Coding','A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'Andrew', 'Coding','A awesome book!', 5, 2029),
    Book(4, 'Title 1', 'Author 1', 'Category','Book Description', 2, 2028),
    Book(5, 'Title 2', 'Author 2', 'Category','Book Description', 3, 2027),
    Book(6, 'Title 3', 'Author 3', 'Category','Book Description', 1, 2026)
]


@app.get("/books", status_code=status.HTTP_200_OK)
def get_books():
    return BOOKS

@app.get("/books/{book_title}", status_code=status.HTTP_200_OK)
# def get_book_by_title(book_title: str):
def get_book_by_title(book_title: str = Path(..., min_length=3, max_length=50)):
    # return [book for book in BOOKS if book['title'].lower() == book_title.lower()]
    for book in BOOKS:
        if book['title'].lower() == book_title.lower():
            return book
        
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
# def get_book_by_category(category: str):
def get_book_by_category(category: str = Query(..., min_length=3, max_length=10)):
    return [book for book in BOOKS if book['category'].lower() == category.lower()]

@app.get("/books/{author}/{category}", status_code=status.HTTP_200_OK)
def get_book_by_author_and_category(author: str, category: str):
    return [book for book in BOOKS if (book['author'].lower() == author.lower() and book['category'].lower() == category.lower())]

# @app.get("books/{id}")

@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
# def create_book(book: dict = Body(...)):
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(book) == 0:
        book.id = 1
    else:
        book.id = BOOKS[-1].id + 1
    return book
    

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
# def update_book(updated_book: dict = Body(...)):
def update_book(updated_book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/delete_book/{book_title}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_title: str):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")