#PYPI
######
#build
python setup.py sdist #standard egg
python setup.py bdist_wheel #new_standard wheel

#upload
python setup.py sdist upload -r pypi
python setup.py bdist_wheel upload -r pypi


#GIT
#####
git add -A #add all new files to the repo.
git commit -m "$1" #commit changes locally - set argument as message
git push origin master # Sends your commits in the "master" branch to GitHub


