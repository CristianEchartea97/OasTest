class MockBotoS3Client:
    """Mock Boto3 S3 Client for testing purposes"""

    def __init__(self, service_name):
        self.service_name = service_name

    def generate_presigned_url(self, operation_name, Params, ExpiresIn):
        return "https://example.com/presigned-url"

    def start_execution(self, stateMachineArn, name, input):
        return {"executionArn": "arn:aws:mocked_ececution_arn"}


class MockBoto3Session:
    """Mock Boto3 Session for testing purposes"""

    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def client(self, service_name):
        return MockBotoS3Client(service_name)


class MockBoto3:
    """Mock Boto3 for testing purposes"""

    class session:
        Session = MockBoto3Session
