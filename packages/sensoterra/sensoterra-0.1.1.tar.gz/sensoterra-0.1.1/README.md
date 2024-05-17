# Sensoterra

Package with a module to load Sensoterra probe data by polling the Sensoterra Customer API.

## Example code

```python
import time
from sensoterra.customerapi import CustomerApi

email = "me@example.com"
password = "secret"

api = CustomerApi(email, password)
api.set_language("en")

while True:
    api.poll()

    for probe in api.probes():
        print(probe)
        for sensor in probe.sensors():
            print(sensor)
        print()

    time.sleep(900)
    print('-' * 70)
```

## Changelog

[CHANGELOG](CHANGELOG.md)

