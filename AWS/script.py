import boto3
import json
import pulp
import logging
from datetime import datetime

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
                'Timestamp': datetime.utcnow()
            }
        ]
    )

def put_record_to_kinesis(stream_name, data):
    """Put a record to Kinesis Data Stream"""
    response = kinesis.put_record(
        StreamName=stream_name,
        Data=json.dumps(data),
        PartitionKey=str(datetime.utcnow().timestamp())
    )
    return response


def optimize_production():
    """Optimize production using linear programming and log the results"""
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

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

    # Log the results
    logger.info("Status: %s" % pulp.LpStatus[prob.status])
    logger.info("Optimal Production Plan:")
    logger.info("Product 1: %s units" % x1.varValue)
    logger.info("Product 2: %s units" % x2.varValue)
    logger.info("Total Profit: $%s" % pulp.value(prob.objective))

    # Send the results to Kinesis
    stream_name = 'ProductionOptimizationResults'
    data = {
        'timestamp': str(datetime.utcnow()),
        'status': pulp.LpStatus[prob.status],
        'product1': x1.varValue,
        'product2': x2.varValue,
        'total_profit': pulp.value(prob.objective)
    }
    response = put_record_to_kinesis(stream_name, data)
    logger.info(f"Optimization results sent to Kinesis. Shard ID: {response['ShardId']}")



if __name__ == "__main__":
    # Put a custom metric to CloudWatch
    put_metric_data('MyCustomMetric', 42, 'Count')

    # Put a record to Kinesis Data Stream
    stream_name = 'MyKinesisStream'
    data = {
        'timestamp': str(datetime.utcnow()),
        'message': 'Hello, Kinesis!'
    }
    response = put_record_to_kinesis(stream_name, data)
    print(f"Record sent to Kinesis. Shard ID: {response['ShardId']}")
