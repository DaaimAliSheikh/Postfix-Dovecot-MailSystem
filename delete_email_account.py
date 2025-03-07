import subprocess
import sys


def delete_user(username):
    # Define the Docker exec command
  command = ['docker', 'exec', 'postfix-smtp', "userdel", "-r",  username] # -r to also delete the home folder of user

    # Execute the command
  docker_result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
  if docker_result.returncode == 0:
      print(docker_result.stdout)
  else:
      print(f'Error: {docker_result.stderr}')



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 delete_user.py <username>")
        sys.exit(1)
    username = sys.argv[1]
    delete_user(username)