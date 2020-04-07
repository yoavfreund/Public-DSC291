## Using aws-jupyter

* pip install jupyter aws
* Documentation: https://github.com/arapat/aws-jupyter
* aws-jupyter -h
* aws-jupyter config

> Please set following configuration parameters.Type Enter if the default value is correct.
> Region [us-west-2]:
> Instance type [m3.xlarge]:
> AMI [ami-0fc359be23c460554]:
> Credential [/Users/yoavfreund/VaultBrain/creds.yaml] 
> ### keep credentials out of github

* aws-jupyter create -c 1 --name testing --type m5ad.2xlarge
* aws-jupyter check --name testing
* aws-jupyter run --script ./test_multiprocess.py
* aws-jupyter retrieve --remote /home/ubuntu/workspace/multi_processing_stats.pkl --local from_remote/
* aws-jupyter terminate --name testing

