class BaseObject(object):
    def __init__(self, obj):
        self.__base_dic = obj

    def safe_get(self, keys):
        dct = self.val
        for key in keys:
            try:
                dct = dct[key]
            except KeyError:
                return None
        return dct

    def safe_set(self, value, keys):
        dct = self.val
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                break

            res = dct.get(key, None)
            if res is None:
                dct[key] = {}
                dct = dct[key]

        dct[keys[-1]] = value

    @property
    def val(self):
        return self.__base_dic

"""

"""

class User(BaseObject):
    def __init__(self, info):
        self.__user_id = info['user_id']
        self.__reviews = []

class Review(BaseObject):
    def __init__(self, info):
        super(self.__class__, self).__init__(info)

    @property
    def review_id(self):
        return super(self.__class__, self).safe_get(['review_id'])

    @property
    def text(self):
        return super(self.__class__, self).safe_get(['text'])

    @property
    def reviewed_by(self):
        return super(self.__class__, self).safe_get(['reviewed_by'])

