from django.apps import AppConfig
import json


class MyAppConfig(AppConfig):
    name = "analysis"

    def ready(self):
        singleton = Singleton()
        with open('static/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
            singleton._shared_data = json.load(f)
        with open('static/SentiWord_intensity.json', encoding='utf-8-sig', mode='r') as f2:
            singleton._shared_data2 = json.load(f2)
        print("사전 로드 완료")
        pass


class Singleton():
    _shared_data = dict()
    _shared_data2 = dict()
    def __init__(self):
        self.__dict__ = self._shared_data
        self.__dict__ = self._shared_data2
        pass

    def data_list(self, wordname):
        data = Singleton()._shared_data
        data2 = Singleton()._shared_data2
        result =['None','None','None']
        for i in range(1, len(data)):
            if data[i]['ngram'] == wordname:
                result.pop()
                result.pop()
                result.pop()
                result.append(data[i]['max.value'])
                result.append(data[i]['max.prop'])
                result.append('None')
                break
        for i in range(1, len(data2)):
            if data2[i]['ngram'] == wordname:
                result.pop()
                result.append(data2[i]['max.value'])
                break
        value = result[0]
        prop = result[1]
        intensity = result[2]
        #print('어근 : ' + r_word)
        #print('극성 : ' + s_word)

        return value, prop, intensity
