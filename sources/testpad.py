import re
from csv import reader
import requests
from sources.check_item import CheckItem


def get_session(login: str, password: str):
    url_login = 'https://ontestpad.com/login'
    with requests.Session() as session:
        r = session.get(url_login)
        csrftoken = r.cookies['csrftoken']
        values = {
            'csrfmiddlewaretoken': csrftoken,
            'js': 'y',
            'next': '',
            'email': login,
            'password': password
        }
        session.post(url_login,
                     data=values,
                     headers={'Referer': url_login})
        # TODO: add login validation
        return session


# Convert script name to URL
def get_script_url(script_name: str):
    # TODO add script_name validation
    scripts = {
        'AL IDE issues': '10',
        'Cloud components': '14',
        'Cloud regression': '15',
        'Cloud issues': '17'
    }
    url = 'https://anylogic.ontestpad.com/script/' + scripts[script_name]
    return url + '/exportcsv//testpad-' + script_name.lower().replace(' ', '-')


# Convert "csv" content to list of rows
def get_script_data(script_name: str, login: str, password: str):
    session = get_session(login, password)
    url_script = get_script_url(script_name)
    script = session.get(url_script)
    script_data = script.text.split('\n')
    return [row for row in script_data if row]


# Gather all issues with JIRA link
def get_tests_with_issues(pattern: str, script_data: list):
    header = 'number,indent,text,tags,notes,result,issue,comment'

    # Skip additional info in csv
    i = 0
    while header not in script_data[i]:
        i += 1

    # Get header and main data of test runs from "csv"
    header = reader(script_data[i:i+1]).__next__()
    data = list(reader(script_data[i+1:]))

    # Find columns where issues are written
    indexes = list(filter(lambda k: header[k] == 'issue', range(len(header))))

    # Create list of CheckItem for every issue which matches the pattern
    tests = set()
    for row in data:
        for i in indexes:
            issues = re.findall(pattern, row[i])
            for issue in issues:
                tests.add(CheckItem(id=row[0], status=row[i-1], issue=issue))
    return sorted(list(tests), key=lambda check: check.issue)


# Run all routines in one function
def get_tests(script_name: str, login: str, password: str, pattern: str):
    script_data = get_script_data(script_name, login, password)
    return get_tests_with_issues(pattern, script_data)
