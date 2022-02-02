
<!--BEGIN STABILITY BANNER-->
---

![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

> **This is a stable example. It should successfully build out of the box**
>
> This example is built on Construct Libraries marked "Stable" and does not have any infrastructure prerequisites to build.
---
<!--END STABILITY BANNER-->

This project is forked from AWS GitHub with a slight modification. In the Medium article, I showed how to deploy PPE rekognition stack.
The full article is available on [Medium](https://medium.com/@rafalb)  

This project was inspired by [aws-sample repository](https://github.com/aws-samples/aws-cdk-examples/tree/master/python/rekognition-lambda-s3-trigger)  
I highly recommend you go through that as well. Many thanks for AWS developer whose created this example.     

Not for use in production.

This project will create the following in your AWS cloud environment:
* IAM group
* IAM user (added to the IAM group)
* S3 bucket
* DynamoDB table
* Lambda function that performs image PPE via AWS Rekognition when new images are uploaded to the S3 bucket
* Roles and policies allowing appropriate access to these resources

Rekognition output will be written to CloudWatch logs, a results folder in the S3 bucket, as well as the DynamoDB table.  

---

Requirements:
* git
* npm (node.js)
* python 3.x
* AWS access key & secret for AWS user with permissions to create resources listed above
  
---

First, you will need to install the AWS CDK:

```
$ sudo npm install -g aws-cdk
```

You can check the toolkit version with this command:

```
$ cdk --version
```

Now you are ready to create a virtualenv:

```
$ python3 -m venv .venv
```

Activate your virtualenv:

```
$ source .venv/bin/activate
```

Install the required dependencies:

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

If everything looks good, go ahead and deploy!  This step will actually make
changes to your AWS cloud environment.  

```
$ cdk bootstrap
$ cdk deploy
```

## Testing the app
Upload an image fie to the S3 bucket that was created by CloudFormation.
The image will be automatically classified.
Results can be found in DynamoDB, S3 bucket "results" folder, and CloudWatch logs for the Lambda function
  
To clean up, issue this command (this will NOT remove the DynamoDB
table, CloudWatch logs, or S3 bucket -- you will need to do those manually) :

```
$ cdk destroy
```

To exit the virtualenv python environment:

```
$ deactivate
```

# Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

---
This code has been tested and verified to run with AWS CDK 1.100.0 (build d996c6d)