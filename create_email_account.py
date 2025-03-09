import subprocess
import sys


def create_user(username, password):
    # Define the Docker exec command
  command = [
    'docker', 'exec', 'postfix-smtp', 'sh', '-c',  #sh -c tells docker to run commadn in a shell inside the container
    f'useradd -m {username} && echo "{username}:{password}" | chpasswd'
]
#   useradd -m user: Creates the user and creates the home directory (-m).
# echo "user:password" | chpasswd: Sets the password for user to password. chpasswd hashes the password automatically.

    # Execute the command
  docker_result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
  if docker_result.returncode == 0:
      print(docker_result.stdout)
  else:
      print(f'Error: {docker_result.stderr}')



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 create_email_account.py <username> <password>")
        sys.exit(1)
    username = sys.argv[1]
    password = sys.argv[2]
   
    create_user(username, password)