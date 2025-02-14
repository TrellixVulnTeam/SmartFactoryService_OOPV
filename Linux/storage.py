import os
import csv
import datetime


class Storage(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.__filename = ''
        self.create()

    # create new csv, first line data with
    # Test time, QR Code, 'Device name', 'Model Name', 'Result', 'density', 'thresholds'
    def create(self) -> None:
        self.__mkdir()
        self.__filename = self.__get_datetime()
        self.set_cached()
        title = ['Test Time', 'QR Code', 'File Name', 'Device Name', 'Model Name', 'Result', 'KDE_score', 'MSE_score']
        with open(self.full_filename, 'w', newline='') as file:
            csv_write = csv.writer(file)
            csv_write.writerow(title)

    # params: data is dict
    # keywords: time, code, device, model, result
    def write(self, **kwargs) -> None:
        data = {}
        for key, value in kwargs.items():
            data[key] = value
        with open(self.full_filename, 'a', newline='') as file:
            csv_write = csv.writer(file)
            csv_write.writerow([data.get('time'), data.get('code'), data.get('filename'),
                                data.get('device'), data.get('model'), data.get('result'),
                               data.get('KDE_score'), data.get('MSE_score')])

    @property
    def full_filename(self) -> str:
        return './CSV/' + self.__filename + '.csv'

    @property
    def filename(self) -> str:
        """
        讀取快取文件中的檔案名稱
        """
        with open('.SmartFactory.cache', 'r') as cache:
            content = cache.read()
        return content

    @staticmethod
    def __get_datetime() -> str:
        name = datetime.datetime.now().strftime("%Y%m%d%H%M")
        return name

    @staticmethod
    def __mkdir() -> None:
        path = os.path.join('./', 'CSV')
        try:
            os.makedirs(path)
        except:
            pass

    def set_cached(self) -> None:
        """
        將檔案名稱儲存至快取文件中
        """
        with open('.SmartFactory.cache', 'w') as cache:
            cache.write(self.__filename)


storage = Storage()
