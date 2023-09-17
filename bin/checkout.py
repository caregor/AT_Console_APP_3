import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='UTF-8')

    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False