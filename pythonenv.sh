#!/bin/bash

NEWENVIRONMENT='virtualenv'

cd $HOME/environment/
mkdir $NEWENVIRONMENT
cd $NEWENVIRONMENT
virtualenv v-env
source ./v-env/bin/activate

# Install packages
pip install pandas
pip install tldextract
pip install argparse
pip install regex
pip install networkx
pip install bokeh
pip install scipy
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