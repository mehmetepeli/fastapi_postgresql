from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book, User, Movie, BoardGame, Comic
from database import get_db
from sqlalchemy.future import select
from datetime import datetime
from passlib.context import CryptContext
from schemas import UserCreate, UserUpdate, BookCreate, BookUpdate, MovieCreate, MovieUpdate, BoardGameCreate, BoardGameUpdate, ComicCreate, ComicUpdate

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@app.get("/users")
async def users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # Get single book by ID
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    # Check if user exists
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
async def add_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if username already exists
    existing_user = await db.execute(select(User).where(User.username == user_data.username))
    if existing_user.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Check if email already exists
    existing_email = await db.execute(
        select(User).where(User.email == user_data.email))
    if existing_email.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user
    new_user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role,
        created_at=datetime.now()
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    # Get the user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if new username is taken by another user
    if user_data.username and user_data.username != user.username:
        existing_user = await db.execute(
            select(User).where(
                (User.username == user_data.username) &
                (User.id != user_id)  # Exclude current user
            )
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken by another user"
            )

    # Check if new email is taken by another user
    if user_data.email and user_data.email != user.email:
        existing_email = await db.execute(
            select(User).where(
                (User.email == user_data.email) &
                (User.id != user_id)  # Exclude current user
            )
        )
        if existing_email.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user"
            )

    # Update only provided fields
    update_data = user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # Delete a user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    # Check if user exists
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}


@app.get("/books")
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books


@app.get("/books/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    # Get single book by ID
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    # Check if book exists
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books")
async def add_book(book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    # Check if book title already exists
    existing_book = await db.execute(select(Book).where(Book.title == book_data.title))
    if existing_book.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this title already exists"
        )

    # Verify user exists if user_id is provided
    if book_data.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == book_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Create new book in database
    new_book = Book(
        title=book_data.title,
        author=book_data.author,
        genre=book_data.genre,
        published_date=book_data.published_date,
        rating=book_data.rating,
        user_id=book_data.user_id,
        created_at=datetime.now()
    )

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


@app.put("/books/{book_id}")
async def update_book(book_id: int, book_data: BookUpdate, db: AsyncSession = Depends(get_db)):
    # Get the book
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Check if title is being changed and would conflict
    if book_data.title and book_data.title != book.title:
        existing_book = await db.execute(
            select(Book).where(
                (Book.title == book_data.title) &
                (Book.id != book_id)  # Exclude current book
            )
        )
        if existing_book.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this title already exists"
            )

    # Check if new user_id exists
    if book_data.user_id is not None and book_data.user_id != book.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == book_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Update only provided fields
    update_data = book_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)
    return book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    # Delete a book
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted successfully"}

@app.get("/movies")
async def get_movies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie))
    movies = result.scalars().all()
    return movies

@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    # Get single book by ID
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    # Check if movie exists
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/movies")
async def add_movie(movie_data: MovieCreate, db: AsyncSession = Depends(get_db)):
    # Check if movie title already exists
    existing_movie = await db.execute(select(Movie).where(Movie.title == movie_data.title))
    if existing_movie.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie with this title already exists"
        )

    # Verify user exists if user_id is provided
    if movie_data.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == movie_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Create new movie in database
    new_movie = Movie(
        title=movie_data.title,
        director=movie_data.director,
        genre=movie_data.genre,
        release_date=movie_data.release_date,
        rating=movie_data.rating,
        user_id=movie_data.user_id,
        created_at=datetime.now()
    )

    db.add(new_movie)
    await db.commit()
    await db.refresh(new_movie)
    return new_movie

@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, movie_data: MovieUpdate, db: AsyncSession = Depends(get_db)):
    # Get the book
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    # Check if title is being changed and would conflict
    if movie_data.title and movie_data.title != movie.title:
        existing_movie = await db.execute(
            select(Movie).where(
                (Movie.title == movie_data.title) &
                (Movie.id != movie_id)  # Exclude current book
            )
        )
        if existing_movie.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Movie with this title already exists"
            )

    # Check if new user_id exists
    if movie_data.user_id is not None and movie_data.user_id != movie.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == movie_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Update only provided fields
    update_data = movie_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)
    return movie

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    # Delete a movie
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    # Check if movie exists
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    await db.delete(movie)
    await db.commit()
    return {"message": "Movie deleted successfully"}

@app.get("/board_games")
async def board_games(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BoardGame))
    games = result.scalars().all()
    return games

@app.get("/board_games/{game_id}")
async def get_game(game_id: int, db: AsyncSession = Depends(get_db)):
    # Get single game by ID
    result = await db.execute(select(BoardGame).where(BoardGame.id == game_id))
    game = result.scalar_one_or_none()

    # Check if game exists
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.post("/board_games")
async def add_game(game_data: BoardGameCreate, db: AsyncSession = Depends(get_db)):
    # Check if game title already exists
    existing_game = await db.execute(select(BoardGame).where(BoardGame.title == game_data.title))
    if existing_game.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game with this title already exists"
        )

    # Verify user exists if user_id is provided
    if game_data.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == game_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Create new game in database
    new_game = BoardGame(
        title=game_data.title,
        designer=game_data.designer,
        genre=game_data.genre,
        release_date=game_data.release_date,
        user_id=game_data.user_id,
        created_at=datetime.now()
    )

    db.add(new_game)
    await db.commit()
    await db.refresh(new_game)
    return new_game

@app.put("/board_games/{game_id}")
async def update_game(game_id: int, game_data: BoardGameUpdate, db: AsyncSession = Depends(get_db)):
    # Get the game
    result = await db.execute(select(BoardGame).where(BoardGame.id == game_id))
    game = result.scalar_one_or_none()

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    # Check if title is being changed and would conflict
    if game_data.title and game_data.title != game.title:
        existing_game = await db.execute(
            select(BoardGame).where(
                (BoardGame.title == game_data.title) &
                (BoardGame.id != game_id)  # Exclude current book
            )
        )
        if existing_game.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game with this title already exists"
            )

    # Check if new user_id exists
    if game_data.user_id is not None and game_data.user_id != game.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == game_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Update only provided fields
    update_data = game_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(game, field, value)

    await db.commit()
    await db.refresh(game)
    return game

@app.delete("/board_games/{game_id}")
async def delete_game(game_id: int, db: AsyncSession = Depends(get_db)):
    # Delete a game
    result = await db.execute(select(BoardGame).where(BoardGame.id == game_id))
    game = result.scalar_one_or_none()

    # Check if game exists
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    await db.delete(game)
    await db.commit()
    return {"message": "Game deleted successfully"}

@app.get("/comics")
async def get_comics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comic))
    comics = result.scalars().all()
    return comics

@app.get("/comics/{game_id}")
async def get_comic(comic_id: int, db: AsyncSession = Depends(get_db)):
    # Get single comic by ID
    result = await db.execute(select(Comic).where(Comic.id == comic_id))
    comic = result.scalar_one_or_none()

    # Check if comic exists
    if comic is None:
        raise HTTPException(status_code=404, detail="Comic not found")
    return comic

@app.post("/comics")
async def add_comic(comic_data: ComicCreate, db: AsyncSession = Depends(get_db)):
    # Check if comic title already exists
    existing_comic = await db.execute(select(Comic).where(Comic.title == comic_data.title))
    if existing_comic.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comic with this title already exists"
        )

    # Verify user exists if user_id is provided
    if comic_data.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == comic_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Create new comic in database
    new_comic = Comic(
        title=comic_data.title,
        author=comic_data.author,
        genre=comic_data.genre,
        published_date=comic_data.published_date,
        user_id=comic_data.user_id,
        created_at=datetime.now()
    )

    db.add(new_comic)
    await db.commit()
    await db.refresh(new_comic)
    return new_comic

@app.put("/comics/{comic_id}")
async def update_comic(comic_id: int, comic_data: ComicUpdate, db: AsyncSession = Depends(get_db)):
    # Get the comic
    result = await db.execute(select(Comic).where(Comic.id == comic_id))
    comic = result.scalar_one_or_none()

    if not comic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comic not found"
        )

    # Check if title is being changed and would conflict
    if comic_data.title and comic_data.title != comic.title:
        existing_comic = await db.execute(
            select(Comic).where(
                (Comic.title == comic_data.title) &
                (Comic.id != comic_id)  # Exclude current book
            )
        )
        if existing_comic.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comic with this title already exists"
            )

    # Check if new user_id exists
    if comic_data.user_id is not None and comic_data.user_id != comic.user_id:
        user_exists = await db.execute(
            select(User).where(User.id == comic_data.user_id))
        if not user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Specified user does not exist"
            )

    # Update only provided fields
    update_data = comic_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(comic, field, value)

    await db.commit()
    await db.refresh(comic)
    return comic

@app.delete("/comics/{comic_id}")
async def delete_comic(comic_id: int, db: AsyncSession = Depends(get_db)):
    # Delete a comic
    result = await db.execute(select(Comic).where(Comic.id == comic_id))
    comic = result.scalar_one_or_none()

    # Check if comic exists
    if comic is None:
        raise HTTPException(status_code=404, detail="Comic not found")

    await db.delete(comic)
    await db.commit()
    return {"message": "Comic deleted successfully"}