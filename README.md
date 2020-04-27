# python
The files found in this repository were created only for learning and practice propose and may not follow the best practices in code development.

## Stackoverflow - webscraping.py

This script creates a file with a sorted list of skills and the  number of times that skill was listed in a job offer from a given country (you can use also city names) extracted from http://stackoverflow.com/jobs.

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
### Linux
Don't forget to give execution permission to this script.

```
chmod +x ./webscraping.py
```

This script you can use like the following example below:
```
$ ./webscraping.py Canada 16
```
Where the first parameter is the country and the second parameter the max number of page to extract the data.
