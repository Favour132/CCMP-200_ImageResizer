# CCMP-200_ImageResizer

 ## Serverless Image Processing Pipeline

### Overview

This project implements a fully serverless, event-driven image processing pipeline using multiple AWS services.
When an image is uploaded to the Original Images S3 bucket, the system automatically triggers a workflow that resizes the image and stores the thumbnail in a separate Resized Images S3 bucket.

The solution demonstrates cloud automation using:

* Amazon S3 – image storage

* AWS Lambda – image resizing logic

* AWS Step Functions – workflow orchestration and error handling

* Amazon API Gateway – optional HTTP trigger for the workflow

* Amazon CloudWatch – operational monitoring and logging

This pipeline is scalable, cost-efficient, and requires zero server management.

### Architecture Diagram

__Screenshot from my Lambda page__

<img width="1240" height="511" alt="image" src="https://github.com/user-attachments/assets/9d1e20c7-89ed-4fdd-8778-9ab22ea13dc4" />


__Screenshot of the Workflow Architecture Diagram__

<img width="1536" height="1024" alt="Workflow Diagram" src="https://github.com/user-attachments/assets/af7d72c6-28a5-489c-a180-30c5aff33029" />


### Setup Instructions

Follow these steps to deploy and run the pipeline.

#### 1. Create the S3 Buckets

Create two buckets in the same AWS Region:

* Original Images Bucket: __favour-capstone-originals__ -> Receives the uploaded images

* Resized Images Bucket: __favour-capstone-resized__ -> Stores the resized images

No special configuration is required for testing.

#### 2. Deploy the Lambda Function

1. Go to AWS Lambda -> Create a Function

2. Runtime: Python 3.12

3. Upload the Lambda code from *(lambda_function.py)*

4. Add environment variable:
     *__RESIZED_BUCKET = favour-capstone-resized__*

5. Add required IAM permissions:

* __s3:GetObject__ on original bucket.

* __s3:PutObject__ on resized bucket.

6. Add S3 Trigger:

* Bucket: original-images-bucket

* Event type: *PUT*

* Add *.jpg* or *.png* suffix filter (Optional)

Make sure the Lambda has the Pillow library included via layer or zip package.   

#### 3. Create the Step Functions State Machine

1. Go to AWS Step Functions

2. Create Standard Workflow

3. Paste the definition from *state_machine/image_processing.json*

4. Replace the Lambda ARN

5. Save the workflow

The state machine includes:

* Task -> Resize image via Lambda

* Choice -> Check success or failure

* Success -> End workflow

* Fail -> Stop execution with error

#### 4. Create the API Gateway Endpoint (Optional)

To manually trigger processing:

1. Create HTTP API

2. Add a POST route

3. Integrate with Step Functions -> StartExecution

4. Provide execution role permissions

Send JSON like:

*__{
  "bucket": "favour-capstone-originals",
  "key": "image.jpg"
}__*

### Testing Instructions

Use these steps to verify that the pipeline works correctly.

#### Test #1 — Automatic Workflow via AWS Console

1. Upload an image (JPG/PNG) to original-images-bucket.

2. Open Step Functions -> Executions and confirm a new execution started.

3. Check resized-images-bucket:

* A resized version of the image should appear.

4. For troubleshooting:

* View Lambda logs: CloudWatch -> Logs -> /aws/lambda/your-function

* Review Step Functions execution diagram

#### Test #2 — Testing using VSCode PowerShell

You can test the pipeline using AWS CLI and by invoking the API Gateway endpoint:

1. Upload an image to the original bucket:

   *aws s3 cp "C:\path\to\your\image.jpg" s3://favour-capstone-originals/*

2. Lambda should automatically trigger the resizing function.

3. Check the resized bucket:

   *aws s3 ls s3://favour-capstone-resized/*

4. Download the resized image to verify:

   *aws s3 cp s3://favour-capstone-resized/image.jpg C:\path\to\downloaded\resized_image.jpg*

5. Invoke the Step Functions workflow via API Gateway:

   *Invoke-WebRequest `
      -Uri "https://654ne481rb.execute-api.us-east-1.amazonaws.com/prod/start" `
      -Method POST `
      -ContentType "application/json" `
      -Body '{"bucket":"favour-capstone-originals","key":"Pretty-2.jpg"}'*

6. Check the resized images bucket to confirm the image was processed.

7. Optional: View Lambda logs in CloudWatch for debugging:

    *aws logs tail /aws/lambda/CapstoneImageResizer --follow*

### Key Features

* Event-driven, serverless architecture

* Automated image resizing

* Workflow state management

* Optional HTTP front-end trigger

* Scalable and low-cost processing

* Fully monitored using CloudWatch

