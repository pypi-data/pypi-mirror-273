# uWebServer

TODO: simple slogan

## Features

- Simple interface

## Examples

```python
import asyncio

from uwebserver import Request, Response, WebServer

app = WebServer()


@app.route("/")
async def hello(req: Request, resp: Response):
    resp.set_content_type("text/html")
    return "<h1>Hello World</h1>"


asyncio.run(app.run())
```
