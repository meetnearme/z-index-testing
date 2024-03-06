import boto3 
from botocore.config import Config


class BenchmarkBase:
    def setup_method(self, table_name):
        # Initialize the dynamodb resource and table 
        db_config = Config(
            region_name='us-east-1',
            signature_version='v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url="http://localhost:8000",
            config=db_config
        )
        self.table = self.dynamodb.Table(table_name)

    def teardown_method(self):
        # Reset the dynamodb resource and table 
        self.dynamodb = None
        self.table = None

    def query_point(self, lon, lat):
        # place holder method for query_point op
        pass

    def query_range(self, min_lat, max_lat, min_lon, max_lon):
        pass
