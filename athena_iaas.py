# __Author__ = "Pranav Chandran"
# __Date__ = 24-06-2024
# __Time__ = 19:13
# __FileName__ = athena_iaas.py
import boto3
import time
import os

# take the cred from env
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# split the cred from env
# aws_access_key_id = aws_access_key_id.split(':')[1]
# aws_secret_access_key = aws_secret_access_key.split(':')[1]

# Set the AWS credentials and region
# os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
# os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # Replace 'us-east-1' with your region


def run_query():
    client = boto3.client('athena')

    query = "SELECT * FROM my_athena_db.salary_data;"
    output_location = 's3://athenajenkinstestbucket/'

    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': 'my_athena_db'
        },
        ResultConfiguration={
            'OutputLocation': output_location,
        }
    )

    print('Execution ID: ' + response['QueryExecutionId'])

    # Wait for the query to finish execution
    while True:
        response = client.get_query_execution(
            QueryExecutionId=response['QueryExecutionId']
        )
        state = response['QueryExecution']['Status']['State']
        print(f"Query state: {state}")



if __name__ == '__main__':
    run_query()