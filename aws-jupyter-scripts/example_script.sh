python Start_ec2_instance.py    # python script to start and check on ec2 instance.
                                # importing the aws-jupyter source as a python module will be much cleaner

aws-jupyter run -s startup.sh

aws-jupyter send-dir --local ~/VaultDSC291/ --remote /home/ubuntu/Vault
export MEM_DIR='../notebooks/Section1-Basics/0.MemoryLatency'
aws-jupyter run --script $MEM_DIR/test_multiprocess.py
sleep 120   # sleep 2 minutes
mkdir from_remote
aws-jupyter retrieve --remote /home/ubuntu/workspace/multi_processing_stats.pkl --local from_remote/

aws-jupyter run --script $MEM_DIR/random_poke.py
sleep 120   # sleep 2 minutes
aws-jupyter retrieve --remote /home/ubuntu/workspace/stats.pkl --local from_remote/

