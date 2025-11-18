Set Up 

What is venv?

`venv` is a module in Python that allows you to create isolated environments for your projects. This is useful for managing dependencies and ensuring that your project has access to the correct versions of libraries without interfering with other projects on your system. When you create a virtual environment using `venv`, it creates a directory that contains a copy of the Python interpreter and a local `site-packages` directory where you can install packages specific to that environment.

Creating a Virtual Environment

To create a virtual environment using `venv`, you can use the following command:

```
python -m venv myenv
```

This will create a new directory called `myenv` (you can choose any name you like) that contains the virtual environment.


what type hints on python are? 

Type hints in Python are a way to indicate the expected data types of variables, function parameters, and return values. They were introduced in Python 3.5 through PEP 484 and are part of the typing module. Type hints help improve code readability, provide better documentation, and enable static type checking using tools like mypy.

what async and await in python are?


`async` and `await` are keywords in Python used to define and work with asynchronous coroutines. Asynchronous programming allows you to write code that can perform non-blocking operations, making it easier to handle tasks like I/O-bound operations (e.g., network requests, file I/O) without blocking the main thread.

- `async`: This keyword is used to define a coroutine function. A coroutine is a special type of function that can be paused and resumed, allowing other tasks to run in the meantime. You define a coroutine by using the `async def` syntax.

- `await`: This keyword is used to pause the execution of a coroutine until the awaited task is complete. It can only be used inside an `async` function. When you `await` a task, the event loop can switch to other tasks while waiting for the result.

Here's a simple example:

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(main())
```

In this example, the `main` function is defined as a coroutine using `async def`. Inside the coroutine, we use `await` to pause the execution for 1 second without blocking the event loop. When we run the `main` coroutine using `asyncio.run()`, it prints "Hello", waits for 1 second, and then prints "World".

how fastapi handles asynchronous requests

FastAPI is built on top of Starlette, which is an asynchronous framework. It fully supports asynchronous request handling using `async` and `await`. When you define an endpoint in FastAPI using an `async def` function, it allows the server to handle other requests while waiting for I/O-bound operations to complete.

Here's a simple example of an asynchronous FastAPI endpoint:

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    await asyncio.sleep(1)
    return {"Hello": "World"}
```

In this example, the `read_root` function is defined as an asynchronous endpoint. When a request is made to this endpoint, it will wait for 1 second without blocking the server, allowing it to handle other requests in the meantime.

what pydantic is?
Pydantic is a data validation and settings management library for Python, built on top of Python's type annotations. It allows you to define data models using standard Python classes and type hints, and it automatically validates and parses input data to ensure it conforms to the specified types. Pydantic is commonly used in FastAPI for request and response data validation.

code errors and status in fastapi 
In FastAPI we can use the Response and status module to managment status and responses easily 

http exception 
In FastAPI, you can raise HTTP exceptions to indicate errors in your API endpoints. FastAPI provides a convenient way to raise exceptions with specific status codes and messages using the `HTTPException` class from the `fastapi` module.