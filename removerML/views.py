from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
# from django.http import JsonResponse
import json
from django.http import HttpResponse
import json
import jsonpickle
from json import JSONEncoder
import os
import datetime
import base64
from . import remover

import models

extensions = ['.jpg', '.jpeg', '.png']
# response_data = {}
# response_data['result'] = 'error'
# response_data['message'] = 'Some error message'
# data = [{'name': 'Peter', 'email': 'peter@example.org'},
#             {'name': 'Julia', 'email': 'julia@example.org'}]
def index(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        ext = os.path.splitext(image.name)[1]
        if ext.lower() in extensions:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            file_name = uploaded_file_url.split("/")[2]

            input_path = os.getcwd() + uploaded_file_url
            output_path = os.getcwd() + "/uploads/" + \
                                    file_name.split(".")[0] + "_processed.png"

            remover.process(input_path, output_path)
            image_path = uploaded_file_url.split(".")[0] + "_processed.png"
            employee = ResponseData(200,"abc")
            employeeJSON = json.dumps(employee)

#             return render(request, 'removerML/index.html', {"image_path": image_path})
            return HttpResponse(json.loads(employeeJSON), content_type="application/json")
        else:
            return HttpResponse("Only Allowed extensions are {}".format(extensions))
    return HttpResponse({'foo':'bar'}, content_type="application/json")

def data(request):
    if request.method == 'POST' and request.POST['image']:
        image = request.POST['image']
        data = base64.b64decode(image)
        image_name = datetime.datetime.now().strftime("%Y%b%d%H%M%S%f") + ".jpg"
        image_path = os.getcwd() + "/uploads/" + image_name

        with open(image_path, "wb") as f:
            f.write(data)

        input_path = os.getcwd() + "/uploads/" + image_name
        output_path = os.getcwd() + "/uploads/" + image_name.split(".")[0] + "_processed.png"

        remover.process(input_path, output_path)
        image_path = "/uploads/" + image_name.split(".")[0] + "_processed.png"
        return HttpResponse(request.get_host() + image_path)
