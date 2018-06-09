#/bin/bash

echo "Uploading code to 209.97.142.1\n"
rsync -avzh --exclude={'driver/','.mypy_cache/','.pytest_cache/','.ropeproject/','.vagrant/','.idea','.git','.pytest_cache/*'} --delete ~/code/python/dbasik-dev/dbasik_dftgovernance/ dbasik@209.97.142.1:/dbasik/code/dbasik_dftgovernance/
