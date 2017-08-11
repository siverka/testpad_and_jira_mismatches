# Main script
# Do not forget update scripts.txt before run

from sources.script_processing import script_processing


# Read names of scripts for status validating
with open('scripts.txt', 'r') as file:
    script_names = [line.strip() for line in file.readlines()]

# Read configuration
with open('configuration.txt', 'r') as file:
    lines = [line.strip().split('=') for line in file.readlines()]
    config = dict(lines)

# Execute validation
for script in script_names:
    print('\n' + script)
    script_processing(script, config)
