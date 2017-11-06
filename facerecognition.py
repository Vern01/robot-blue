import boto3
import io
from PIL import Image


class FaceRecognition:
    s3 = boto3.resource('s3')
    rekognition = boto3.client('rekognition', region_name='eu-west-1')
    dynamodb = boto3.client('dynamodb', region_name='eu-west-1')

    def upload_img(self, image_path, name):
        file = open(image_path, 'rb')
        object = self.s3.Object('blue-faces', 'index/' + image_path)
        object.put(Body=file,
                         Metadata={'FullName': name}
                         )

    def compare_img(self, image_path):
        image = Image.open(image_path)
        stream = io.BytesIO()
        image.save(stream, format="JPEG")
        image_binary = stream.getvalue()
        response = self.rekognition.search_faces_by_image(
            CollectionId='face_collection',
            Image={'Bytes': image_binary}
        )
        if response['FaceMatches']:
            face = self.dynamodb.get_item(
                TableName='face_collection',
                Key={'RekognitionId': {'S': response['FaceMatches'][0]['Face']['FaceId']}}
            )

            if 'Item' in face:
                print(face['Item']['FullName']['S'], response['faceMatches'][0]['Face']['Confidence'])
            else:
                print('No match found in person lookup')