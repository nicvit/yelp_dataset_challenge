__author__ = 'Adisorn'

import os
import json
import base64

OUTPUT_FOLDER_PATH = './output_images'

class ImageExporter(object):

    def __init__(self):
        super(ImageExporter, self).__init__()

    def list_all_images(self):
        for f in os.listdir(OUTPUT_FOLDER_PATH):
            if f.endswith(".jpg") or f.endswith(".png"):
                file_path = OUTPUT_FOLDER_PATH + '/' + f
                yield file_path, f

    def convert_images_to_base64(self):
        res = []
        for file_path, file_name in self.list_all_images():
            with open(file_path, "rb") as imageFile:
                base64_str = base64.b64encode(imageFile.read())
                #print base64_str
                image_base64 = ImageBase64()
                image_base64.set_image_contents(base64_str, file_name)
                #print(image_base64.to_json_string())
                res.append(image_base64)
            #print(file_name)

        return res

class ImageBase64(object):
    def __init__(self):
        super(ImageBase64, self).__init__()

    def set_image_contents(self, content, file_name):
        self.__content = content
        self.__file_name, self.__file_extension = os.path.splitext(file_name)

    def to_dict(self):
        dct = dict()
        dct['file_name'] = self.file_name
        dct['content'] = self.content
        dct['file_extension'] = self.file_extension

        return dct

    def to_json_string(self):
        dct = self.to_dict()
        return json.dumps(dct)

    @property
    def content(self):
        return self.__content

    @property
    def file_name(self):
        return self.__file_name

    @property
    def file_extension(self):
        return self.__file_extension.replace('.', '')

if __name__ == "__main__":
    fileExplorer = ImageExporter()
    fileExplorer.convert_images_to_base64()
