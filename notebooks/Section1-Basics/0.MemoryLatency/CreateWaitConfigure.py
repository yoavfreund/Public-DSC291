aws-jupyter config
aws-jupyter create -c 1 --name testing --type m5ad.2xlarge
aws-jupyter check --name testing
aws-jupyter run --script ./test_multiprocess.py

aws-jupyter retrieve -h
aws-jupyter retrieve --remote /home/ubuntu/workspace/multi_processing_stats.pkl --local from_remote/

aws-jupyter terminate --name testing

