"""Upload photos to MinIO

Revision ID: 009
Revises: 008
Create Date: 2024-01-09 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import os
import io
import requests
from urllib.parse import urlparse
import boto3
from botocore.client import Config


# revision identifiers, used by Alembic.
revision: str = '009'
down_revision: Union[str, None] = '008'
next_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Initialize MinIO client
    s3_client = boto3.client(
        's3',
        endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT', 'minio:9000')}",
        aws_access_key_id=os.getenv('MINIO_ACCESS_KEY', 'user'),
        aws_secret_access_key=os.getenv('MINIO_SECRET_KEY', 'password'),
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
    
    bucket_name = os.getenv('MINIO_BUCKET', 'media')
    
    # Get all media entries with external URLs
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id, external_resource_url FROM media WHERE external_resource_url LIKE 'https://images.unsplash.com%' OR external_resource_url LIKE 'https://i.pravatar.cc%'"))
    
    # Update each media entry
    for row in result:
        media_id = row[0]
        old_url = row[1]
        
        try:
            # Download the image
            response = requests.get(old_url, timeout=10)
            response.raise_for_status()
            
            # Determine file extension from content type
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            if 'png' in content_type:
                file_extension = 'png'
            elif 'webp' in content_type:
                file_extension = 'webp'
            else:
                file_extension = 'jpg'
            
            # Determine folder based on URL pattern
            if 'unsplash' in old_url:
                folder = 'photos'
            else:
                folder = 'avatars'
            
            # Generate S3 key
            s3_key = f"{folder}/media_{media_id}.{file_extension}"
            
            # Upload to MinIO
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=io.BytesIO(response.content),
                ContentType=content_type
            )
            
            # Update database with new S3 URL
            new_url = f"http://minio:9000/{bucket_name}/{s3_key}"
            conn.execute(
                sa.text("UPDATE media SET external_resource_url = :new_url WHERE id = :id"),
                {"new_url": new_url, "id": media_id}
            )
            
            print(f"Uploaded media {media_id}: {s3_key}")
            
        except Exception as e:
            print(f"Failed to upload media {media_id}: {str(e)}")
            # Continue with other uploads even if one fails
            continue


def downgrade() -> None:
    # Revert to original pravatar URLs
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id FROM media WHERE external_resource_url LIKE 'http://minio:9000%'"))
    
    for row in result:
        media_id = row[0]
        # Extract the img number from the media ID or use a default pattern
        img_num = media_id
        old_url = f"https://i.pravatar.cc/150?img={img_num}"
        
        conn.execute(
            sa.text("UPDATE media SET external_resource_url = :old_url WHERE id = :id"),
            {"old_url": old_url, "id": media_id}
        )
