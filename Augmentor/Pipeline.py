from Augmentor import ImageOperations
from Augmentor import ImageSource
from Augmentor import GithubFlavoredMarkdownTable
from Augmentor.ProgramFinishedException import ProgramFinishedException


class Pipeline(object):
    ProgramFinishedException = ProgramFinishedException

    def __init__(self, image_path=None):
        self.function_list = []
        self.function_iterator = None
        self.image_iterator = None
        self.image_to_process = None
        self.finished = None
        if image_path is not None:
            self.image_path = image_path
            self.image_source = ImageSource.ImageSource(image_path)

        else:
            raise ProgramFinishedException("No image source")

        self.image_operations = ImageOperations.ImageOperations()

    def addFlipX(self, chance=1):
        print("addFlipX")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.flip_x(self.image_operations,
                                                                                         img_source, storage_location,
                                                                                         chance),
             "FlipX"])
        self.setup_iterators()

    def addFlipY(self, chance=1):
        print("addFlipY")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.flip_y(self.image_operations,
                                                                                         img_source, storage_location,
                                                                                         chance),
             "FlipY"])
        self.setup_iterators()

    def addTranspose(self, chance=1):
        print("addTranspose")
        self.setup_iterators()

    def addRotate90(self, chance=1):
        print("addRotate90")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.rotate_90(self.image_operations,
                                                                                            img_source,
                                                                                            storage_location, chance),
             "Rotate90"])
        self.setup_iterators()

    def addRotate180(self, chance=1):
        print("addRotate180")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.rotate_180(self.image_operations,
                                                                                             img_source,
                                                                                             storage_location, chance),
             "Rotate180"])
        self.setup_iterators()

    def addRotate270(self, chance=1):
        print("addRotate270")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.rotate_270(self.image_operations,
                                                                                             img_source,
                                                                                             storage_location, chance),
             "Rotate270"])
        self.setup_iterators()

    def addResize(self, height, width, chance=1):
        print("addResize")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.resize(self.image_operations,
                                                                                         img_source, height, width,
                                                                                         storage_location,
                                                                                         chance), "Resize"])
        self.setup_iterators()

    def addScale(self, height, width, chance=1):
        print("addScale")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.scale(self.image_operations,
                                                                                        img_source, height, width,
                                                                                        storage_location,
                                                                                        chance), "Scale"])
        self.setup_iterators()

    def addRotate(self, degree, chance=1):
        print("addRotate")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.rotate(self.image_operations,
                                                                                         img_source, degree,
                                                                                         storage_location,
                                                                                         chance),
             "Rotate"])
        self.setup_iterators()

    def addCrop(self, height, width, chance=1):
        print("addCrop")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.crop(self.image_operations,
                                                                                       img_source,
                                                                                       height, width, storage_location,
                                                                                       chance), "Crop"])
        self.setup_iterators()

    def addConvertGrayscale(self, chance=1):
        print("addConvertGrayscale")
        self.function_list.append(
            [lambda img_source, storage_location: ImageOperations.ImageOperations.convert_grayscale(
                self.image_operations, img_source,
                storage_location,
                chance),
             "ConvertGrayscale"])
        self.setup_iterators()

    def execute(self, number_of_images=None, storage_location=None):
        if number_of_images is None:
            finished = self.image_source.populate_images()

            if finished is -1:
                raise ProgramFinishedException("All images have been executed!")

            for image in self.image_source.list_of_images:
                for function, _ in self.function_list:
                    function(image, storage_location)
            raise ProgramFinishedException("All images have been executed!")

        else:

            if self.image_to_process is None:
                self.image_to_process = self.image_source.populate_one_image()
            if self.image_to_process is -1:
                raise ProgramFinishedException("All images have been executed!")

            i = 0
            while i < number_of_images:
                try:
                    if self.image_to_process is -1:
                        raise ProgramFinishedException("All images have been executed!")
                    f = (next(self.function_iterator))
                    f(self.image_to_process, storage_location)
                    i += 1

                except StopIteration:

                    self.image_to_process = self.image_source.populate_one_image()
                    self.setup_function_iterator()
        if storage_location is None:
            print("Saving " + str(i) + " images to " + self.image_source.root_path)
        if isinstance(storage_location, list):
            print("Images saved to memory object.")

    def summary(self):
        list_of_operations = []
        for _, function_name in self.function_list:
            list_of_operations.append(function_name)

        table_data = [
            ['Pipeline Summary:', ''],
            ['Operation count', str(len(self.function_list))],
            ['Operations', ''],
        ]
        for i in range(0, len(list_of_operations)):
            table_data[2][1] += str(list_of_operations[i] + '\n')

        table = GithubFlavoredMarkdownTable(table_data)
        print(table.table)

    def setup_iterators(self):
        self.image_iterator = iter(self.image_source.list_of_images)
        self.setup_function_iterator()

    def setup_function_iterator(self):
        function_list = []
        for function in self.function_list:
            function_list.append(function[0])
        self.function_iterator = iter(function_list)

    def clean_up(self, storage_location):
        for buffer in storage_location:
            buffer.close()
