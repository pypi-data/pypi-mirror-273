# Botasaurus Requests

botasaurus-requests is a fork of the requests library with the playwright dependencies removed.

## Installation

```bash
pip install botasaurus-requests
```

## Usage

```python
from botasaurus_requests import request

driver = Driver()
response = request.get(
    "https://www.g2.com/products/omkar-cloud/reviews",
    headers={
        "Referer": "https://www.google.com/",
    },
)
print(response.status_code)
```

## Credits

Special thanks to [daijro](https://github.com/daijro) for creating [hrequests](https://github.com/daijro/hrequests).