# get_gradesData_from_nuweb

## Support
Windows, MacOS(Intel, M1).

This app needs GoogleChrome. Supports for Safari, Firefox and Microsoft Edge is not provided.

## Installation
1. Install GoogleChrome (This version needs GoogleChrome)

2. Check your Chrome's version, and get suitable chromedriver from [Chromedriver(chromium)](https://chromedriver.chromium.org/downloads)

3. execute following:
```
git clone https://github.com/sky21peanuts/get_gradesData_from_nuweb.git
```

4. Put chromedriver under ./driver

5. On terminal, execute following to get Selenium:
 ```
 pip3 install selenium
 ```
 or
 ```
 python -m pip install selenium
 ```

## Usage
Go to getGrade/app/ and execute app.py, and  commandline starts. Then only you put your ID and password, your grade date is downloaded ~/Desktop .

## Caution
- This app depends on your internet connection speed. If some error(such as NoSuchElementException..) occurd, edit app/app.py and let `WAIT_TIME` be bigger.

- By using `--headless` option, chrome window will be hidden.
