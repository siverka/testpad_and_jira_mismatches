from jira import JIRA
from sources.progress import progress

statuses = {'pass': ['Closed'],
            'skip': ['Closed'],
            'fail': ['Open', 'In Progress', 'Reopened'],
            'blocked': ['Open', 'In Progress', 'Reopened'],
            '': ['Open', 'In Progress', 'Reopened'],
            'query': ['Open', 'In Progress', 'Reopened']}


def get_jira_changes(tests: list, server: str, auth: tuple, mode = ['info', 'issues']):
    jira = JIRA(server, basic_auth=auth)
    global statuses
    changes = []
    i, n = 0, len(tests)
    for check in tests:
        issue = jira.issue(check.issue)
        status = issue.fields.status.name
        resolution = issue.fields.resolution
        if status not in statuses[check.status]:
            if mode == 'info':
                changes.append(repr(check) + ", jira: " + status + ', resolution: ' + str(resolution) + '\n')
            else:
                changes.append(check.issue + ' ')
        i += 1
        progress(i, n)
    return changes
