import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ec2 = boto3.resource('ec2')

#Change value based on ISO 3166-1 alpha-2 country code
COUNTRY_CODE = 'es'
RUNNING_INSTANCE_CODE = 16

def is_running(instance):
    if instance.state['Code'] == RUNNING_INSTANCE_CODE:
        return True
    return False

def has_country(country, instance):
    tags = instance.tags
    for tag in tags:
        if (tag['Key'] == 'country') & (tag['Value'] == country):
            return True
    return False

def get_running_instances_id(country):
    running_instances_id = []
    instances = list(ec2.instances.all())
    logger.info("Number of instances found: {}".format(len(instances)))
    for instance in instances:
        if has_country(country,instance) & is_running(instance):
            running_instances_id.append(instance.instance_id)
    return running_instances_id


def stop_instances(country):
    running_instances_id = get_running_instances_id(country)
    logger.info("{} number of instances that will be stop".format(str(len(running_instances_id))))
    for id in running_instances_id:
        ec2.Instance(id).stop()
        logger.info('Instance with id {} has been stopped'.format(id))


def lambda_handler(event, context):
    country=COUNTRY_CODE
    logger.info('Stopping instances of: {}'.format(country))
    stop_instances(country)
    