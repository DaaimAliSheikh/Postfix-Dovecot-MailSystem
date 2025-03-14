import subprocess


def delete_user(email):
    # Define the Docker exec command
  username = email.split('@')[0]
  
  command = ['docker', 'exec', 'postfix-smtp', "userdel", "-r",  username] # -r to also delete the home folder of user which contains all the emails

    # Execute the command
  docker_result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
  if docker_result.returncode == 0:
      print(docker_result.stdout)
  else:
      print(f'Error: {docker_result.stderr}')



