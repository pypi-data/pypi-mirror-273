import boto3
import s3fs
from dotenv import load_dotenv
import os

class DocumentStorageConnection:
    """Manages S3 connections, providing both boto3 resource and s3fs file system."""
    _resource_instance = None
    _filesystem_instance = None

    @classmethod
    def initialize(cls):
        """Initialize the S3 client connections."""
        load_dotenv()  # Load environment variables from .env file

        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        if cls._resource_instance is None:
            cls._resource_instance = boto3.resource(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
        
        if cls._filesystem_instance is None:
            cls._filesystem_instance = s3fs.S3FileSystem(
                key=aws_access_key_id,
                secret=aws_secret_access_key
            )

    @classmethod
    def get_resource(cls):
        """Return the boto3 resource instance, initializing if not already done."""
        if cls._resource_instance is None:
            cls.initialize()  # Ensure it is initialized
        return cls._resource_instance

    @classmethod
    def get_filesystem(cls):
        """Return the s3fs filesystem instance, initializing if not already done."""
        if cls._filesystem_instance is None:
            cls.initialize()  # Ensure it is initialized
        return cls._filesystem_instance
