from Augmentor import ImageOperations
from Augmentor import ImageSource
from Augmentor import AsciiTable


class Pipeline(object):

    def __init__(self, image_path ='.'):
        self.function_list = []
        self.image_path = image_path
        self.image_source = ImageSource.ImageSource(image_path)
        self.image_operations = ImageOperations.ImageOperations()

    def addFlipX(self, chance = 1):
        print("addFlipX")
        self.function_list.append([lambda:ImageOperations.ImageOperations.flip_x(self.image_operations, self.image_source, chance), "FlipX"])

    def addFlipY(self, chance = 1):
        print("addFlipY")
        self.function_list.append([lambda:ImageOperations.ImageOperations.flip_y(self.image_operations, self.image_source, chance), "FlipY"])

    def addTranspose(self, chance = 1):
        print("addTranspose")

    def addRotate90(self, chance = 1):
        print("addRotate90")
        self.function_list.append([lambda:ImageOperations.ImageOperations.rotate_90(self.image_operations, self.image_source, chance), "Rotate90"])

    def addRotate180(self, chance = 1):
        print("addRotate180")
        self.function_list.append([lambda:ImageOperations.ImageOperations.rotate_180(self.image_operations, self.image_source, chance), "Rotate180"])

    def addRotate270(self, chance=1):
        print("addRotate270")
        self.function_list.append([lambda:ImageOperations.ImageOperations.rotate_270(self.image_operations, self.image_source, chance), "Rotate270"])

    def addResize(self, height, width):
        print("addResize")
        self.function_list.append([lambda:ImageOperations.ImageOperations.resize(self.image_operations, self.image_source, height, width), "Resize"])

    def addScale(self, height, width):
        print("addScale")
        self.function_list.append([lambda:ImageOperations.ImageOperations.scale(self.image_operations, self.image_source, height, width), "Scale"])

    def addRotate(self, degree):
        print("addRotate")
        self.function_list.append(lambda:ImageOperations.ImageOperations.rotate(self.image_operations, self.image_source, degree))

    def addCrop(self, height, width):
        print("addCrop")
        self.function_list.append(lambda:ImageOperations.ImageOperations.scale(self.image_operations, self.image_source, height, width))

    def AddConvertGrayscale(self):
        print("AddConvertGrayscale")
        self.function_list.append(lambda:ImageOperations.ImageOperations.convert_grayscale(self, self.image_source))

    def execute(self):
        print("Saving " + str(len(self.image_source.list_of_images) + len(self.image_source.list_of_images)) + " images to " + self.image_source.root_path)

        for f,_ in self.function_list:
            f()

    def summary(self):
        list_of_operations = []
        for _,function_name in self.function_list:
            list_of_operations.append(function_name)

        table_data = [
        ['Pipline Summary:'],
        [str(len(self.function_list)) + ' operation(s)'],
        ['New size: ' + str(len(self.image_source.list_of_images) + len(self.image_source.list_of_images))],
        ['TODO: Print additional information'],
        ]
        table = AsciiTable(table_data)
        print(table.table)
