#/bin/bash

echo "Uploading code to 209.97.142.1\n"
rsync -avzh --exclude={'__pycache__/','tests/','driver/','logs/','.mypy_cache/','.pytest_cache/','.ropeproject/','.vagrant/','.idea','.git','.pytest_cache/*'} --delete ~/code/python/dbasik-dev/dbasik_dftgovernance/ dbasik@209.97.142.1:/dbasik/code/dbasik_dftgovernance/
# you have to start and stop the server manually. Not doing it causes issues with terminal hooking, etc
#ssh dbasik@dbasik "pkill gunicorn & bash /dbasik/code/dbasik_dftgovernance/gunicorn_start.bash"
