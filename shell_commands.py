import subprocess

def run_migrations():
    subprocess.run('flask db init', shell=True)
    subprocess.run('flask db migrate -m "Initial migrate"', shell=True)
    subprocess.run('flask db upgrade', shell=True)


def first_push_to_git(commit_message, git_url):
    print('Initializing git ...')
    subprocess.run('git init', shell=True)
    print()
    print('Adding files to git ...')
    subprocess.run('git add .' ,shell=True)
    print()
    print('Committing to git ...')
    subprocess.run(f'git commit -m {commit_message}' ,shell=True)
    print()
    print('Adding origin')
    subprocess.run(f'git remote add origin {git_url}')
    print()
    print('Final Push to git ...')
    subprocess.run('git push origin master', shell=True)
    print()


def other_pushes_to_git(commit_message):
    print('Initializing git ...')
    subprocess.run('git init', shell=True)
    print()
    print('Adding files to git ...')
    subprocess.run('git add .' ,shell=True)
    print()
    print('Committing to git ...')
    subprocess.run(f'git commit -m {commit_message}' ,shell=True)
    print()
    
    print('Final Push to git ...')
    subprocess.run('git push origin master', shell=True)
    print()

other_pushes_to_git('"Threading2"')

#run_migrations()