#!/bin/bash

NEWENVIRONMENT='virtualenv'

cd $HOME/environment/
mkdir $NEWENVIRONMENT
cd $NEWENVIRONMENT
virtualenv v-env
source ./v-env/bin/activate

# Install packages
pip install pandas
mkdir goodfaith
cp -r $HOME/environment/goodfaith/* ./goodfaith

deactivate

chmod 777 -R $HOME/environment/virtualenv/
# source $HOME/environment/$NEWENVIRONMENT/v-env/bin/activate
# chmod -R 777 $HOME/environment/


#  ./__main__.py -s $HOME/environment/virtualenv/samples/scope.json -i $HOME/environment/virtualenv/samples/brevityinmotion-urls-max.txt -o $HOME/environment/virtualenv/output