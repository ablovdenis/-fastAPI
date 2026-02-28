from fastapi import FastAPI

from api import categories, comments, locations, posts, users

app = FastAPI()


# Добавил роутеры, чтоб не импортировать последовательно один API в другой.
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(posts.router)
app.include_router(comments.router)