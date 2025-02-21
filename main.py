from fastapi import FastAPI

app = FastAPI()

@app.post("/program")
def create_program():
    return {
        "title": "New Program",
        "description": "This is a new program."\
    }

@app.get("/")
def root():
    return {
        "message": "Hello World"
    }
