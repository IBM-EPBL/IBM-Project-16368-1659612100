from flask import Flask,render_template
import ibm_boto3
from ibm_botocore.client import Config, ClientError

# Constants for IBM COS values
# Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
# eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_API_KEY_ID = "woQWUbe5L17TQigzRjXOOZyOhnI6-XWGoe8XKB84CyA6"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/baf735ca71e04c5bb0bbcf550d3e9ba8::serviceid:ServiceId-5d2a616c-87e9-4b4b-a442-52308410a6c5"
# eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"
#COS_ENDPOINT ="https://config.cloud-object-storage.cloud.ibm.com"
#COS_API_KEY_ID ="woQWUbe5L17TQigzRjXOOZyOhnI6-XWGoe8XKB84CyA6"
#COS_INSTANCE_CRN ="crn:v1:bluemix:public:iam-identity::a/baf735ca71e04c5bb0bbcf550d3e9ba8::serviceid:ServiceId-5d2a616c-87e9-4b4b-a442-52308410a6c5"
# Create resource
cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )

app = Flask(__name__)


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

@app.route('/')
def index():
    files = get_bucket_contents('customer-care-quadswag')
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run(debug=True)
Footer