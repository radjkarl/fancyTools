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


#API on GitHub pages
####################

sphinx-apidoc -A "Karl Bedrich" -F -f -o doc fancytools

cd doc/_build

git clone https://github.com/radjkarl/fancyTools.git gh-pages

rm -r html
mv gh-pages html
cd html

git rm -rf -f .
git clean -fxd
cd ../../



make html
cd _build/html
git add .
git commit -a -m 'API updated'
git push -f origin HEAD:gh-pages 

cd ../../..
