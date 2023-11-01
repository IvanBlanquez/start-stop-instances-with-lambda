import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ec2 = boto3.resource('ec2')

#Change value based on ISO 3166-1 alpha-2 country code
COUNTRY_CODE = 'es'
STOPPED_INSTANCE_CODE = 80

def is_stopped(instance):
    if instance.state['Code'] == STOPPED_INSTANCE_CODE:
        return True
    return False

def has_country(country, instance):
    tags = instance.tags
    for tag in tags:
        if (tag['Key'] == 'country') & (tag['Value'] == country):
            return True
    return False

def get_stopped_instances_id(country):
    stop_instances_id = []
    instances = list(ec2.instances.all())
    logger.info("Number of instances found: {}".format(len(instances)))
    for instance in instances:
        if has_country(country,instance) & is_stopped(instance):
            stop_instances_id.append(instance.instance_id)
    return stop_instances_id


def start_instances(country):
    stopped__instances_id = get_stopped_instances_id(country)
    logger.info("{} number of instances that will be start".format(str(len(stopped__instances_id))))
    for id in stopped__instances_id:
        ec2.Instance(id).start()
        logger.info('Instance with id {} has been started'.format(id)  )


def lambda_handler(event, context):
    country=COUNTRY_CODE
    logger.info('Starting instances of: {}'.format(country))
    start_instances(country)
    