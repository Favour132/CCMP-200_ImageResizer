import boto3
from PIL import Image
import io
import os
import json

s3 = boto3.client("s3")

# Optional: use different bucket for resized images, else same as source
resized_bucket = os.environ.get("RESIZED_BUCKET")


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # 🔹 If called via API Gateway (HTTP), the input is in event["body"]
    if "body" in event and isinstance(event["body"], str):
        try:
            data = json.loads(event["body"])
        except Exception as e:
            return {
                "status": "fail",
                "error": f"Invalid JSON body: {e}",
                "received": event
            }
    else:
        # 🔹 If called from Step Functions or directly, use event/Input
        data = event.get("Input", event)

    bucket = data.get("bucket")
    key = data.get("key")

    if not bucket or not key:
        return {
            "status": "fail",
            "error": "Missing bucket or key",
            "received": data
        }

    target_bucket = resized_bucket or bucket

    try:
        # 1) Download original image
        response = s3.get_object(Bucket=bucket, Key=key)
        image = Image.open(response["Body"])

        # 2) Resize to thumbnail
        image.thumbnail((128, 128))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        # 3) Upload resized image
        resized_key = f"resized-{key}"
        s3.put_object(
            Bucket=target_bucket,
            Key=resized_key,
            Body=buffer,
            ContentType="image/jpeg",
        )

        # 4) Always return plain JSON with top-level status
        return {
            "status": "success",
            "source_bucket": bucket,
            "source_key": key,
            "resized_bucket": target_bucket,
            "resized_key": resized_key,
        }

    except Exception as e:
        return {
            "status": "fail",
            "error": str(e),
        }
