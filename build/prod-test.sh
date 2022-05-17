#!/bin/bash

NEWENVIRONMENT='virtualenv'

cd $HOME/environment/
mkdir $NEWENVIRONMENT
cd $NEWENVIRONMENT
virtualenv v-env
source ./v-env/bin/activate

# Install packages
#pip install pandas
#pip install tldextract
#pip install argparse
#pip install regex
#pip install networkx
#pip install bokeh
#pip install scipy
#python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps goodfaith-brevityinmotion-0.0.1

#python3 -m pip install -i https://test.pypi.org/simple/ goodfaith

#python3 -m pip install $HOME/environment/goodfaith/dist/goodfaith-1.0.3.tar.gz
python3 -m pip install goodfaith

mkdir goodfaith
cd goodfaith
cp -r $HOME/environment/goodfaith/* .

deactivate

chmod 777 -R $HOME/environment/virtualenv/
# source $HOME/environment/$NEWENVIRONMENT/v-env/bin/activate
# chmod -R 777 $HOME/environment/


#  ./__main__.py -s $HOME/environment/virtualenv/samples/scope.json -i $HOME/environment/virtualenv/samples/brevityinmotion-urls-max.txt -o $HOME/environment/virtualenv/output

# python3 -m pip install --upgrade build


# python3 -m pip install --upgrade twine

# python3 -m twine upload --repository testpypi dist/*

# To build project:
# Run the following from root of project:
# python3 -m build
# Then cd into the build folder and run:
# sh testinstall.sh
# Run the following to enable the virtual environment
# source $HOME/environment/virtualenv/v-env/bin/activate
# Can begin to run the test cases
# goodfaith -s $HOME/environment/virtualenv/goodfaith/samples/scope.json -i $HOME/environment/virtualenv/goodfaith/samples/brevityinmotion-urls-max.txt -o $HOME/environment/virtualenv/output -v
# python3 __main__.py -s $HOME/environment/virtualenv/goodfaith/samples/scope.json -i $HOME/environment/virtualenv/goodfaith/samples/brevityinmotion-urls-max.txt -o $HOME/environment/virtualenv/output -v  

# python3 -m twine upload dist/* --verbose