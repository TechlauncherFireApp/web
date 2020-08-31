from dotenv import load_dotenv
import os

# Get the address of the mysql host
# (development environment only)
def mysql_host_address():
    file_path = "/etc/hosts"
    with open(file_path, 'r') as f:
        # Read lines of hosts file
        line = f.readline()
        lines = []
        while line:
            lines.append(line)
            line = f.readline()
    try:
        # Get the last line of the file (mysql_net interface)
        workspace_host_split = lines[-1].split()[0].split('.')
        # Switch the last number between 2 and 3
        last_num = workspace_host_split[3]
        switcher = {
            "3":"2",
            "2":"3"
        }
        last_num = switcher[last_num]
        # Compile the MySQL host ip
        mysql_host_split = workspace_host_split
        mysql_host_split[3] = last_num
        mysql_host = '.'.join(mysql_host_split)
        return mysql_host
    except:
        print("Failed to get address of mysql host")
        return False

# Load and set relevant environment variables
def load_env():
    load_dotenv()
    # if this is a development environment, get MYSQL_HOST programatically
    # otherwise set it through .env or manually
    if os.environ.get('DEVELOPMENT'):
        mysql_host = mysql_host_address()
        os.environ["MYSQL_HOST"] = mysql_host
