cd cdk/notebook_instances
mkdir notebook
cd notebook
cdk init --language python --app notebook
cp ../app.py ../cdk.json  ../requirements.txt .
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt

cdk context
cdk list

cdk synth SagemakerStackEU
cdk deploy SagemakerStackEU

<uncomment bucket in app.py>

cdk synth SagemakerStackEU
cdk diff SagemakerStackEU
cdk deploy SagemakerStackEU

cdk destroy SagemakerStackEU

