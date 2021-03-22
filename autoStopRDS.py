import boto3

rds = boto3.client('rds')

def lambda_handler(event, context):
    db_list = list_db_clusters_autostop()
    for cluster in db_list:
        if cluster['Status'] == 'available':
            rds.stop_db_cluster(DBClusterIdentifier=cluster['DBClusterIdentifier'])
            print('stopping: ' + cluster['DBClusterIdentifier'])
        else:
            print('no operation for autoStop: ' + cluster['DBClusterIdentifier'] + ' ' + cluster['Status'])

def list_db_clusters_autostop():
    list = []
    
    response = rds.describe_db_clusters(MaxRecords=20)
    if len(response['DBClusters']) > 0:
        for cluster in response['DBClusters']:
            tags = rds.list_tags_for_resource(ResourceName=cluster['DBClusterArn'])

            if len(tags['TagList']) > 0:
                for tag in tags['TagList']:
                    if tag['Key'] == 'autoStop' and tag['Value'] == 'true':
                        list.append(cluster)
                        break
                
    return list
