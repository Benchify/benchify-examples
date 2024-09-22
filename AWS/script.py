import boto3
import json
import pulp
from datetime import datetime, timezone

# Initialize AWS clients
cloudwatch = boto3.client('cloudwatch')
kinesis = boto3.client('kinesis')

def put_metric_data(metric_name, value, unit):
    """Put custom metric data to CloudWatch"""

    cloudwatch.put_metric_data(
        Namespace='CustomMetrics',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.now(timezone.utc)  # Fixed here
            }
        ]
    )

def put_record_to_kinesis(stream_name, data):
    """Put a record to Kinesis Data Stream"""

    response = kinesis.put_record(
        StreamName=stream_name,
        Data=json.dumps(data),
        PartitionKey=str(datetime.now(timezone.utc).timestamp())  # Fixed here
    )
    return response

def log_to_cloudwatch(log_group, log_stream, message):
    """Log a message to CloudWatch"""

    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)  # Fixed here
    cloudwatch.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[
            {
                'timestamp': timestamp,
                'message': message
            }
        ]
    )

def optimize_production():
    """Optimize production using linear programming and log the results to CloudWatch"""
    
    log_group = 'ProductionOptimizationLogs'
    log_stream = 'OptimizationResults'

    # Create the LP problem
    prob = pulp.LpProblem("Production Optimization", pulp.LpMaximize)

    # Define variables
    x1 = pulp.LpVariable("Product_1", lowBound=0)
    x2 = pulp.LpVariable("Product_2", lowBound=0)

    # Define the objective function
    prob += 20 * x1 + 30 * x2, "Profit"

    # Define constraints
    prob += 2 * x1 + 3 * x2 <= 100, "Labor_hours"
    prob += 4 * x1 + 3 * x2 <= 120, "Material_units"

    # Solve the problem
    prob.solve()

    # Prepare the results
    status = pulp.LpStatus[prob.status]
    product1 = x1.varValue
    product2 = x2.varValue
    total_profit = pulp.value(prob.objective)

    # Log the results to CloudWatch
    log_to_cloudwatch(log_group, log_stream, f"Status: {status}")
    log_to_cloudwatch(log_group, log_stream, "Optimal Production Plan:")
    log_to_cloudwatch(log_group, log_stream, f"Product 1: {product1} units")
    log_to_cloudwatch(log_group, log_stream, f"Product 2: {product2} units")
    log_to_cloudwatch(log_group, log_stream, f"Total Profit: ${total_profit}")

    # Send the results to Kinesis
    stream_name = 'ProductionOptimizationResults'
    data = {
        'timestamp': str(datetime.now(timezone.utc)),  # Fixed here
        'status': status,
        'product1': product1,
        'product2': product2,
        'total_profit': total_profit
    }
    response = put_record_to_kinesis(stream_name, data)
    log_to_cloudwatch(log_group, log_stream, f"Optimization results sent to Kinesis. Shard ID: {response['ShardId']}")

    # Return the results
    return {
        'status': status,
        'product1': product1,
        'product2': product2,
        'total_profit': total_profit
    }

if __name__ == "__main__":
    # Put a custom metric to CloudWatch
    put_metric_data('MyCustomMetric', 42, 'Count')

    # Put a record to Kinesis Data Stream
    stream_name = 'MyKinesisStream'
    data = {
        'timestamp': str(datetime.now(timezone.utc)),  # Fixed here
        'message': 'Hello, Kinesis!'
    }
    response = put_record_to_kinesis(stream_name, data)
    print(f"Record sent to Kinesis. Shard ID: {response['ShardId']}")
