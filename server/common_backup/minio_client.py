"""MinIO S3 storage utilities"""
import os
import io
import boto3
from botocore.client import Config
from typing import Optional


class MinIOClient:
    """MinIO S3-compatible storage client"""
    
    def __init__(self):
        self.endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
        self.access_key = os.getenv('MINIO_ACCESS_KEY', 'user')
        self.secret_key = os.getenv('MINIO_SECRET_KEY', 'password')
        self.bucket = os.getenv('MINIO_BUCKET', 'media')
        self.secure = os.getenv('MINIO_SECURE', 'false').lower() == 'true'
        
        protocol = 'https' if self.secure else 'http'
        
        self.client = boto3.client(
            's3',
            endpoint_url=f"{protocol}://{self.endpoint}",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'
        )
    
    def upload_file(
        self, 
        file_data: bytes, 
        key: str, 
        content_type: str = 'application/octet-stream'
    ) -> str:
        """
        Upload file to MinIO
        
        Args:
            file_data: File bytes
            key: S3 object key (path)
            content_type: MIME type
            
        Returns:
            URL to access the file
        """
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=io.BytesIO(file_data),
            ContentType=content_type
        )
        
        protocol = 'https' if self.secure else 'http'
        return f"{protocol}://{self.endpoint}/{self.bucket}/{key}"
    
    def get_file_url(self, key: str) -> str:
        """
        Get public URL for a file
        
        Args:
            key: S3 object key
            
        Returns:
            Public URL
        """
        protocol = 'https' if self.secure else 'http'
        return f"{protocol}://{self.endpoint}/{self.bucket}/{key}"
    
    def delete_file(self, key: str) -> None:
        """
        Delete file from MinIO
        
        Args:
            key: S3 object key
        """
        self.client.delete_object(Bucket=self.bucket, Key=key)
    
    def file_exists(self, key: str) -> bool:
        """
        Check if file exists
        
        Args:
            key: S3 object key
            
        Returns:
            True if file exists
        """
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except:
            return False


# Singleton instance
minio_client = MinIOClient()
