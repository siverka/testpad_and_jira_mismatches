import keyring
from sources.testpad import get_tests

from sources.get_jira_changes import get_jira_changes


def script_processing(script_name: str, config: dict):
    # Get tests with jira issue from script
    tests = get_tests(script_name,
                      config['testpad_auth'],
                      keyring.get_password('testpad', config['testpad_auth']),
                      config['pattern'])
    # Get changes in statuses for test in tests
    changes = get_jira_changes(tests,
                               server=config['server'],
                               auth=(config['jira_auth'],
                                     keyring.get_password('jira', config['jira_auth'])))
    # Print out the changes
    output_file = script_name + '.txt'
    print('\nOutput file:', output_file)
    with open('outputs/' + output_file, 'w') as file:
        file.writelines(changes)
