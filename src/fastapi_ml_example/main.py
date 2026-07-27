from fastapi import FastAPI

app = FastAPI(title="FastAPI ML Example")


def main() -> None:
    "Запуск приложения в Uvicorn (`uv run fastapi-ml-example`)."
    import uvicorn
    uvicorn.run(app, port=8080)


if __name__ == "__main__":
    main()
