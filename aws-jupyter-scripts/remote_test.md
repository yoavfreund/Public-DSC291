## Using aws-jupyter

* aws-jupyter -h
* aws-jupyter config

> Please set following configuration parameters.Type Enter if the default value is correct.
> Region [us-west-2]:
> Instance type [m3.xlarge]:
> AMI [ami-0fc359be23c460554]:
> Credential [/Users/yoavfreund/VaultBrain/creds.yaml] 
> ### keep credentials out of github

*  aws-jupyter create -c 1 --name testing --type m5ad.2xlarge
*  aws-jupyter check --name testing
* aws-jupyter run --script ./test_multiprocess.py

aws-jupyter retrieve -h
aws-jupyter retrieve --remote /home/ubuntu/workspace/multi_processing_stats.pkl --local from_remote/

aws-jupyter terminate --name testing

### Storage performance

S3: https://github.com/dvassallo/s3-benchmark
EBS: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html

===

instances types and prices

On Demand
https://aws.amazon.com/ec2/pricing/on-demand/

Spot
https://aws.amazon.com/ec2/spot/pricing/
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances-history.html

Questions for Julaiti

* How to read/write from S3 from the aws-jupyter instances, directly to memory?
boto
Julaiti will make a little demo script.

* How to check whether a script has ended?
Read file repeatedly until all of the file (including a line saying "end" has been read).

* when an instance is "ebs only" what does it mean? Holds only the OS image, with about 5GB free.

* Is there a fixed (across instance types) path/paths to the usable storage?
With SSD you need to mount the disk before using it.
Julaiti: Do you need to also format the disk or is there a standard command?

=====
### Examples of low latency / high throughput

* ARCGIS basemap - ocean map: https://www.arcgis.com/home/webmap/viewer.html?webmap=5ae9e138a17842688b0b79283a4353f6


