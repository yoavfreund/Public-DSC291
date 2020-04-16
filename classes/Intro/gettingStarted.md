## Getting Started directions for DSC291

The directions are based on the assumption that you are familiar with Unix and using a computer that is either an apple PC, or an Ubuntu Linux.

### Conda
It is highly recommended that you install Conda on your laptop. That will allow you to run jupyter notebooks locally, without the help of AWS. To install conda follow [these directions](https://docs.anaconda.com/anaconda/). Once you have conda installed, try it out by following [these Directions](https://docs.anaconda.com/anaconda/user-guide/)

### Github
The code for this course will be distributed through github. 
Directions for cloning or forking the github repository are given [here](https://sites.google.com/eng.ucsd.edu/dsc291-sp20/class-github)

### AWS credentials
AWS credentials provide user verification method for connecting to AWS resources. 
We store credentials in two files:

##### For AWS-CLI
**~/Vault/credentials.sh:**  
> export AWS\_ACCESS\_KEY_ID=ASIA...XJ6   
> export AWS\_SECRET\_ACCESS\_KEY=yD8a...96nQg

##### For aws-jupyter and spark-notebook.
**~/Vault/creds.yaml:**  
> Yoav_DSC291:   
>>  access\_key\_id: AKI ..... X2  
>>  secret\_access\_key: GG .... ZZ  
>>  email\_address: yfreund@eng.ucsd.edu 
>>  key\_name: YoavDSC291KeyPair  
>>  ssh\_key: /Users/yoavfreund/.ssh/YoavDSC291KeyPair.pem  

NOTE
1. mkdir ~/Vault (To create Valut directory)
2. Under this folder create credentials.sh and creds.yaml files. Use above template to fill the files.
3. Get access\_key\_id and secret\_access\_key from treasurer. **Don't make these public**
4. See section **Key Pairs** below to create key .pem file.
5. Make sure to set email address, key name and ssh key fields to appropriate values.

#### Credentials Security
In this class, credentials will be shared among the members of each team for the duration of the spring quarter. This raises a significant vulnerability. How can we share the credentials among 8-9 people without unwittingly leaking those credential to the world?

Such leaks can be very costly. There are vigilanties that scour the internet for credentials and then sell the stolen credentials to other unsavory types. Thousands of dollars in AWS debt can be accrued in a single hour. Amazon will often waive these costs, but not always.

The main principle for keeping credentials safe is **keep them separate from your git directories**. Having credentials appear on github/bitbucket/etc. is very common. It might appear in a credential file, or it might be in a notebook that contains commands to that prints the value of the credential variables. Such breaches are so common that AWS constantly scans public repositories for leaked credentials, and blocks the account.

A good practice for this is to create a directory under the home directory (on your laptop), call it something like **Vault** and put all passwords and credentials there. For easy access, you can symbolic links to **Vault** or to specific files in **Vault** from your work directory. Even if you back your work directory on github, the files that are linked will not be backed up.

#### The Treasurer
Due to the sensitivity of the credentials, one member of each team is designated "treasurer". The TAs will share the team credentials with the treasurer and s/he will share it with other members of the team, and verify that the member understands the issue of github and credentials and is storing the credentials safely.

Each set of credentials is associated with a separate AWS account. The status of this account (delayed 12-16 hours) can be monitored [here](https://ets-apps.ucsd.edu/dsc291-custom-aws/). It is the responsibility of the treasurer to closely mnitor these expenses and insure that there are no over-runs. **Only treasurer has access to it**

One of the most common ways to accrue large expenses is to for get that you started instances and never turn them off. You can always check on the current set of ec2 instances that are running by using the below AWS cli command.

> aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[].Instances[*].{Instance:InstanceId}" --output table

### Using AWS CLI
[AWS-CLI](https://aws.amazon.com/cli/) is a command line interface for AWS. In other words, it allows you to interact with AWS from the command line, or from inside a notebook. AWS-CLI has a huge number of commands, for interacting with just about any part of the AWS universe (see [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/index.html]). 

To use CLI you need to do two things:
1. Download and install [AWS-CLI](https://aws.amazon.com/cli/)
2. Perform  
> source ~/Vault/credentials.sh

AWS-CLI lets you capture actions in a script.

#### Getting started with AWS-CLI

* **installing aws-cli** follow directions in [AWS-CLI](https://aws.amazon.com/cli/)

* **Setting credentials**   To set credentials run the following command
> source ~/Vault/credentials.sh

* **Creating a new bucket**
> aws s3api create-bucket --bucket **<BUCKET_NAME>** --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2

* **Listing buckets**
> aws s3 ls

#### Notes on naming buckets 
* s3 bucket names are globally unique, and the namespace is shared by all AWS accounts. 
* Bucket names must not contain uppercase characters or underscores.
* See [Bucket Restriction and Documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html) for more information.

### Key Pairs
We will need SSH credentials so that we can make SSH connections to EC2 instances. Use below command 
> aws ec2 create-key-pair --key-name YoavDSC291KeyPair --query 'KeyMaterial' --output text > /Users/yoavfreund/.ssh/YoavDSC291KeyPair.pem

https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-keypairs.html#creating-a-key-pair

## Using aws-jupyter

AWS-Jupyter is a set of scripts written by my student Julaiti Arapat: [GitHub Repository for AWS-jupyter](https://github.com/arapat/aws-jupyter)

One of it's main features is that it makes it easy to create instances on **ec2** and have jupyter notebooks run on them. It has many additional features we will get to later on.

### Getting started with aws-Jupyter

* The package is installed using *pip install* It is not necessary to clone the github repository on your laptop.
* In order to allow aws-jupyter to connect with the ec2 instance you will need both the AWS credetials and the ssh key pair.
* To get started read [Readme.md](https://github.com/arapat/aws-jupyter/blob/master/README.md), for full details read [the manual](https://github.com/arapat/aws-jupyter/blob/master/manual.md)

* Set the basic configuration
> aws-jupyter config
>> Please set following configuration parameters.Type Enter if the default value is correct.

>> Region [None]: us-west-2

>> Instance type [m3.xlarge]: 

>> AMI [ami-0fc359be23c460554]: 

>> Credential [None]: /Users/yoavfreund/Vault/creds.yaml

* Check AWS credentials work
> aws-jupyter access

* To start a single ec2 instance instance use:
> aws-jupyter create -c 1 --name test_dsc291 --region us-west-2

Then issue the command
> aws-jupyter check --name test_dsc291

Wait until the instance is up and ready. At that point above command will print out output that will look like below. 

> The Jupyter Notebook is running on the cluster at the address below.
> 
> Open the following address using the browser on your computer
>
>  http://IP:8888/?token=ba17a86916f60743f89ba3c7e571304b55d933b38fbfaf63
>
> (If the URL didn't show up, please wait a few seconds and try again.)

Use the URL to connect to your ec2 instance.

### First steps using a notebook in the cloud

Once your instance is running, you should be able to connect to the jupyter notebook server by pasting the given URL into you browser.

To clone the public class repository into the instance, click on **New** and select **Terminal**, this will open a terminal inside your browser. The prompt should be something like:  
> ubuntu@ip-172-31-54-3:~/workspace$ 

Paste into the terminal the command:  
> git clone https://github.com/yoavfreund/Public-DSC291.git

Now you can go back to the main jupyter tab and navigate to  
> Public-DSC291/notebooks/Section0-Intro/notebooks

Click on  
> 1\_pregnancy\_length\_analysis.ipynb


**Congratulations:** You are running a notebook in the cloud!
