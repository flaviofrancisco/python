# python
The files found in this repository were created only for learning and practice propose and may not follow the best practices in code development.

## Stackoverflow - webscraping.py

This script creates a file with a sorted list by quantity of job skills from a given country extracted from http://stackoverflow.com/jobs.

### Dependecies

Install Python:

https://www.python.org/

Install lxml

https://lxml.de/

```
import sys
import requests
import operator
from lxml.html import fromstring
```

This script you can use like the following example below:
```
$ ./webscraping.py Canada 16
```
Where the first parameter is the country and the second parameter the max number of page to extract the data.
