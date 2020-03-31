## Getting Started directions for DSC291

The directions are based on the assumption that you are familiar with Unix and using a computer that is either an apple PC, or an Ubuntu Linux.

### Conda
It is highly recommended that you install Conda on your laptop. That will allow you to run jupyter notebooks locally, without the help of AWS. To install conda follow [these directions](https://docs.anaconda.com/anaconda/). Once you have conda installed, try it out by following [these Directions](https://docs.anaconda.com/anaconda/user-guide/)

### Github
The code for this course will be distributed through github. 
Directions for cloning or forking the github repository are given [here](https://sites.google.com/eng.ucsd.edu/dsc291-sp20/class-github)

### AWS credentials
AWS credentials provide the main main user verification method for connecting to AWS resources. 

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

See more about the last two lines in the section **Key Pairs** below.

#### Credentials Security
In this class, credentials will be shared among the members of each team for the duration of the spring quarter. This raises a significant volunerability. How can we share the credentials among 8-9 people without unwittingly leaking those credential to the world?

Such leaks can be very costly. There are vigilanties that scour the internet for credentials and then sell the stolen credentials to other unsavory types. Thousands of dollars in AWS debt can be accrued in a single hour. Amazon will often waive these costs, but not always.

The main principle for keeping credentials safe is **keep them separate from your git directories**. Having credentials appear on github/bitbucket/etc. is very common. It might appear in a credential file, or it might be in a notebook that contains commands to that prints the value of the credential variables. Such breaches are so common that AWS constantly scans public repositories for leaked credentials, and blocks the account.

A good practice for this is to create a directory under the home directory (on your laptop), call it something like **Vault** and put all passwords and credentials there. For easy access, you can symbolic links to *Vault* or to specific files in *Vault* from your work directory. Even if you back your work directory on github, the files that are linked will not be backed up.

#### The Treasurer
Due to the sensitivity of the credentials, one member of each team is designated "treasurer". The TAs will share the team credentials with the treasurer and s/he will share it with other members of the team, and verify that the member understands the issue of github and credentials and is storing the credentials safely.

Each set of credentials is associated with a separate AWS account. The status of this account (delayed 12-16 hours) can be monitored [here](https://ets-apps.ucsd.edu/dsc291-custom-aws/). It is the responsibility of the treasurer to closely mnitor these expenses and insure that there are no over-runs.
One of the most common ways to accrue large expenses is to for get that you started instances and never turn them off. You can alway check on the current set of ec2 instances that are running by using the AWS console.

### Using AWS CLI
[AWS-CLI](https://aws.amazon.com/cli/) is a command line interface for AWS. In other words, it allows you to interact with AWS from the command line, or from inside a notebook. AWS-CLI has a huge number of commands, for interacting with just about any part of the AWS universe (see [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/index.html]). 

To use CLI you need to do two things:
1. Download and install [AWS-CLI](https://aws.amazon.com/cli/)
2. Perform  
> source ~/Vault/credentials.sh

The alternative to AWS-CLI is using the [AWS console](https://aws.amazon.com/console/), which is a browser based controller. The alternative is handy when you are trying to do something with AWS for the first time. Once you know how to do that thing, it is better to use AWS-CLI which lets you capture actions in a script.

#### Getting started with AWS-CLI

* **installing aws-cli** follow directions in [AWS-CLI](https://aws.amazon.com/cli/)

* **Setting credentials**   To set credentials run the following command
> source ~/Vault/credentials.sh

* **Creating a new bucket**
> aws s3api create-bucket --bucket yoavfreundtest --region us-west-2

* **Listing buckets**
> aws s3 ls

#### Notes on naming buckets 
* s3 bucket names are globally unique, and the namespace is shared by all AWS accounts. 
* Bucket names must not contain uppercase characters or underscores.
* See [Bucket Restriction and Documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html) for more information.

## The console
The Console is an alternative to usng the command line interface. It is a convenient way to perform one-time tasks, but becomes cumbersome if you want to perform the same task over and over again. For reapeated tasks we use AWS_CLI or custom scripts that run on top of the [boto](https://boto3.amazonaws.com/v1/documentation/api/latest/index.htmlR) SDK.

You can reach the AWS console by clicking on **click here to access AWS** from <a href="https://ets-apps.ucsd.edu/dsc291-custom-aws/">https://ets-apps.ucsd.edu/dsc291-custom-aws/</a></li>. Once you are here you have access to an overwhelming array of services. For our needs, we will mostly use *S3* and *EC2*. 

### Key Pairs
In addition to the AWS_ACCESS credentials, we will need SSH credentials so that we can make SSH connections to EC2 instances. An easy way to generate ssh key pairs is through the console.  From the main page, choose **ec2**, then **key pairs** and **create key pair**. Choose a name for your keypair and whether it is .pem or .ppk (I use .pem). You will then get a .pem file that you download and place in your .ssh directory. (for more on ssh see this [Youtube video](https://www.youtube.com/watch?v=4WQe_-DAn1E) )

## Using aws-jupyter

AWS-Jupyter is a set of scripts written by my student Julaiti Arapat: [GitHub Repository for AWS-jupyter](https://github.com/arapat/aws-jupyter)

One of it's main features is that it makes it easy to create instances on **ec2** and have jupyter notebooks run on them. It has many additional features we will get to later on.

### Getting started with aws-Jupyter

* The package is installed using *pip install* It is not necessary to clone the github repository on your laptop.
* In order to allow aws-jupyter to connect with the ec2 instance you will need both the AWS credetials and the ssh key pair.
* To get started read [Readme.md](https://github.com/arapat/aws-jupyter/blob/master/README.md), for full details read [the manual](https://github.com/arapat/aws-jupyter/blob/master/manual.md)
* To start a single ec2 instance instance use:

> aws-jupyter create -c 1 --name test 

Then issue the command

> aws-jupyter check --name test

until the instance is up and ready. At that point the check command will print out a URL that you can use to connect to the instance.

### First steps using a notebook in the cloud

Once your instance is running, you should be able to connect to the jupyter notebook server by pasting the given URL into you browser.

To clone the public class repository into the instance, click on **New v** and select **Terminal**, this will open a terminal inside your browser. The prompt should be something like:  
> ubuntu@ip-172-31-54-3:~/workspace$ 

Paste into the terminal the command:  
> git clone https://github.com/yoavfreund/Public-DSC291.git

Now you can go back to the main jupyter tab and navigate to  
> Public-DSC291/notebooks/Section0-Intro/notebooks

Click on  
> 1\_pregnancy\_length\_analysis.ipynb


**Congratulations:** You are running a notebook in the cloud!
