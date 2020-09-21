class Client():
    def put_object(self, Body, Bucket, Key, ContentType):
        return True

    def get_object(self, Bucket, Key):
        return {
            'Body': Key
        }