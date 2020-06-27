import json
import os

S3_BUCKET = os.environ["BUCKET_NAME"]


async def write_to_s3(new_file: dict, file_name: str, client) -> None:
    key = f"{file_name}.json"

    await client.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(new_file),
        ContentType="application/json",
        ContentDisposition="inline"
    )

    print(f"{file_name} written.")
