from jira import JIRA

from sources.progress import progress


def get_jira_changes(tests: list, server: str, auth: tuple):
    jira = JIRA(server, basic_auth=auth)
    statuses = {'blocked': ['Open', 'In Progress', 'Reopened'],
                'fail': ['Open', 'In Progress', 'Reopened'],
                '': ['Open', 'In Progress', 'Reopened'],
                'pass': ['Resolved', 'Closed'],
                'skip': ['Open', 'In Progress', 'Reopened']}
    changes = []
    i, n = 0, len(tests)
    for check in tests:
        status = jira.issue(check.issue, fields='status').fields.status.name
        if status not in statuses[check.status]:
            changes.append(repr(check) + ", jira: " + status + '\n')
        i += 1
        progress(i, n)
    return changes
