# AWS Excel Sheet SQS Service

A serverless AWS service that processes data through SQS and generates Excel sheets stored in S3. This service can be triggered from third-party backend services.

## Architecture

- **SQS Queue**: Receives messages from third-party services
- **Lambda Functions**: Two Lambda functions process messages:
  1. **Data Processor**: Processes and validates incoming data
  2. **Excel Generator**: Generates Excel files and uploads to S3
- **S3 Bucket**: Stores generated Excel files

## Prerequisites

- Python 3.11 or higher
- AWS CLI configured with appropriate credentials
- AWS CDK CLI installed (`npm install -g aws-cdk`)
- AWS account with permissions to create:
  - SQS queues
  - Lambda functions
  - S3 buckets
  - IAM roles and policies

## Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Lambda dependencies
pip install -r lambdas/data_processor/requirements.txt -t lambdas/data_processor/
pip install -r lambdas/excel_generator/requirements.txt -t lambdas/excel_generator/
```

### 2. Bootstrap CDK (First time only)

```bash
cdk bootstrap
```

### 3. Deploy Infrastructure

```bash
cd infrastructure
cdk deploy
```

After deployment, note the stack outputs:
- `QueueUrl`: SQS queue URL (use this to send messages)
- `BucketName`: S3 bucket name where Excel files are stored
- `DataProcessorFunctionName`: Name of the data processor Lambda
- `ExcelGeneratorFunctionName`: Name of the Excel generator Lambda

## Usage

### Sending Messages from Third-Party Service

Use the provided script or integrate directly with your backend:

```python
from scripts.send_to_sqs import send_excel_request
import boto3

# Your SQS queue URL (from CDK stack outputs)
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/excel-processing-queue"

# Your data
data = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]

# Send message
response = send_excel_request(
    queue_url=QUEUE_URL,
    data=data,
    filename="users_report.xlsx",
    metadata={"report_type": "users", "version": "1.0"}
)
```

### Message Format

The SQS message body should be a JSON object with the following structure:

```json
{
  "data": [
    {"field1": "value1", "field2": "value2"},
    {"field1": "value3", "field2": "value4"}
  ],
  "filename": "report.xlsx",
  "metadata": {
    "key": "value"
  }
}
```

### Example Script

```bash
# Make script executable
chmod +x scripts/send_to_sqs.py

# Run with queue URL
python scripts/send_to_sqs.py <QUEUE_URL>
```

## Lambda Functions

### Data Processor Lambda

- **Purpose**: Processes and validates incoming data
- **Input**: SQS message with data, filename, and metadata
- **Output**: Saves processed data as JSON to S3 (intermediate step)
- **Location**: `lambdas/data_processor/`

### Excel Generator Lambda

- **Purpose**: Generates Excel files from processed data
- **Input**: SQS message with data, filename, and metadata
- **Output**: Excel file saved to S3 bucket
- **Location**: `lambdas/excel_generator/`
- **Dependencies**: Uses `openpyxl` library for Excel generation

## S3 Bucket Structure

```
excel-sheets-{account}-{region}/
├── processed/
│   └── {filename}.json          # Intermediate processed data
└── excel/
    └── {filename}.xlsx          # Final Excel files
```

## Monitoring

- Check CloudWatch Logs for Lambda execution logs
- Monitor SQS queue metrics in CloudWatch
- Check S3 bucket for generated files

## Cleanup

To remove all resources:

```bash
cd infrastructure
cdk destroy
```

**Warning**: This will delete the S3 bucket and all its contents. Make sure to backup any important files first.

## Customization

### Modify Lambda Functions

1. Edit the Lambda function code in `lambdas/data_processor/` or `lambdas/excel_generator/`
2. Redeploy: `cdk deploy`

### Change Infrastructure

1. Edit `infrastructure/sqs_lambda_stack.py`
2. Redeploy: `cdk deploy`

### Adjust Lambda Settings

Modify in `infrastructure/sqs_lambda_stack.py`:
- `timeout`: Lambda execution timeout
- `memory_size`: Lambda memory allocation
- `batch_size`: Number of messages processed per invocation

## Troubleshooting

### Lambda Timeout

- Increase timeout in `sqs_lambda_stack.py`
- Ensure SQS visibility timeout is greater than Lambda timeout

### Permission Errors

- Verify IAM roles have correct permissions
- Check S3 bucket policies

### Excel Generation Issues

- Verify `openpyxl` is installed in Lambda layer
- Check CloudWatch logs for detailed error messages

## Security Notes

- SQS queue is not publicly accessible by default
- Ensure proper IAM policies for third-party services
- Consider using VPC endpoints for private access
- Enable S3 bucket encryption for production use

## License

MIT

