from django.db import models

# Create your models here.


class ResponseData(object):
    def __init__(self, code, imagepath):
        self.code = code
        self.imagepath = imagepath
