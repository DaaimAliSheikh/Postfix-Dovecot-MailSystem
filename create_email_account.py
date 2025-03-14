import subprocess
import sys


def create_user(email, password):
    # Define the Docker exec command
  username = email.split('@')[0]
  
  command = [
    'docker', 'exec', 'postfix-smtp', 'sh', '-c',  #sh -c tells docker to run command in a shell inside the container
    f'useradd -m {username} && echo "{username}:{password}" | chpasswd'
]
#   useradd -m user: Creates the user and creates the home directory (-m).
# echo "user:password" | chpasswd: Sets the password for user to password. chpasswd hashes the password automatically.

    # Execute the command
  result = subprocess.run(command, capture_output=True, text=True)
  return result




