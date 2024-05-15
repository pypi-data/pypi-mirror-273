class Dictoat:
    def __init__(self,dictt: dict = {}) -> object:
        """
        Converts a dictionary to an object.

        :param dictt: The Dictonary to be converted to an object.
        :return: Object that can be called as any other.
        """
        for item in dictt:
            if type(dictt[item]) is dict:
                setattr(self, str(item)+'_', Dictoat(dictt[item])) # the undersquare avoids coinciding with reserved keywords
            else:
                setattr(self, str(item)+'_', dictt[item])
