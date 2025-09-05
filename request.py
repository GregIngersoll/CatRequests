import boto3
import requests
import sys
import urllib.request

from PIL import Image

def display_image (image_url):
    """
    Display an image from the passed in HTTP url.
    """
    try:
        temp = "temp.jpg"
        urllib.request.urlretrieve(image_url, temp)
        img = Image.open(temp)
        img.show()
    except Exception as ex:
        print (f"Error on image display: {ex}")

def getAllCats(domain):
    """
    Retrieve all Cat Data from the Cats endpoint.
    """
    resp = requests.get(f"http://{domain}/Cats")
    if resp.status_code != 200:
        print (f"Error code: {resp.status_code}")
        return
    
    data = resp.json()
    return data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        domain = sys.argv[1]

        catData = getAllCats(domain)

        s3_client = boto3.client('s3')
        for catInfo in catData:
            path = catInfo["imagePath"]
            realPath = path.split ("/")
            bucket = realPath[2]
            object = realPath[3]
            try:
                presigned_url = s3_client.generate_presigned_url ('get_object', Params={'Bucket':bucket, 'Key':object}, ExpiresIn=3600)
                display_image(presigned_url);
            except Exception as ex:
                print (f"Error {ex}");



