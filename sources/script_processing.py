import keyring
import os
from sources.testpad import get_tests

from sources.get_jira_changes import get_jira_changes


def script_processing(script_name: str, config: dict, output_mode: str):
    # Get tests with jira issue from script
    tests = get_tests(script_name,
                      config['testpad_auth'],
                      keyring.get_password('testpad', config['testpad_auth']),
                      config['pattern'])
    # Get changes in statuses for test in tests
    changes = get_jira_changes(tests,
                               server=config['server'],
                               auth=(config['jira_auth'],
                                     keyring.get_password('jira', config['jira_auth'])),
                               mode=output_mode)
    # Print out the changes
    print('\nOutput file:', script_name)
    output_file = 'outputs/' + script_name + '.txt'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as file:
        file.writelines(changes)
