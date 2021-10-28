import io
import boto3


def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    kwargs = {'Bucket': bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix,)
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                return

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj["Key"]


def check_s3_file(floc):
    '''
    Return True if exists and False if it does not
    '''
    bucket = floc.split('/')[2]
    prefix = '/'.join(floc.split('/')[3:])

    found = False
    for key in get_matching_s3_keys(bucket, prefix):
        if prefix in key:
            found = True
    return found


def store_s3_file(bucket, location, binary_string):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket, location)
    object.put(Body=binary_string)


def load_coverage_report(s3_bucket, s3_key, sep='\t', names=None):
    '''
    https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
    '''
    # Load the data from s3
    client = boto3.client("s3")
    obj = client.get_object(Bucket=s3_bucket, Key=s3_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()), sep=sep, names=names)

    return df


def load_coverage_report2(s3_loc, sep='\t', names=None):
    '''
    https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
    '''
    s3_bucket = s3_loc.split('/')[2]
    s3_key = '/'.join(s3_loc.split('/')[3:])

    # Load the data from s3
    client = boto3.client("s3")
    obj = client.get_object(Bucket=s3_bucket, Key=s3_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()), sep=sep, names=names)

    return df


def read_s3_file(s3_bucket, s3_key):
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket, s3_key)
    return obj.get()['Body'].read().decode("utf-8")


def object_size(s3_bucket, s3_key):
    return boto3.resource('s3').Bucket(s3_bucket).Object(s3_key).content_length


def object_size2(s3_loc):
    s3_bucket = s3_loc.split('/')[2]
    s3_key = '/'.join(s3_loc.split('/')[3:])

    return boto3.resource('s3').Bucket(s3_bucket).Object(s3_key).content_length


def read_s3_file2(s3_loc):
    s3 = boto3.resource('s3')
    bucket = s3_loc.split('/')[2]
    key = '/'.join(s3_loc.split('/')[3:])
    return read_s3_file(bucket, key)


def store_s3_file2(s3_loc, binary_string):
    s3 = boto3.resource('s3')
    bucket = s3_loc.split('/')[2]
    key = '/'.join(s3_loc.split('/')[3:])
    return store_s3_file(bucket, key, binary_string)
