import sys

class DbHelper:
    __DEFAULT_SORT_VALUE = {
        int: sys.maxsize * -1,
        str: '',
        bool: False,
        'none': None
    }

    @classmethod
    # Used by the sort method.
    # Some model fields can be Null (None) and python
    # does not like to compare NoneType to int or str, etc.
    # This method attempts to find the field type by finding the first
    # non-None value and inspecting it.
    # Then we can look-up a valid default value to use in sorting.
    def __model_attr_type(cls, names, objs):
        types = []
        for attr in names:
            attr_type = 'none'
            for obj in objs:
                if obj[attr] is not None:
                    attr_type = type(obj[attr])
                    break

            types.append(attr_type)

        return types

    @classmethod
    def sort(cls, items, sort_desc):
        reverse = False
        sort_flds = sort_desc
        if ':' in sort_desc:
            (sort_flds, sort_dir) = sort_desc.split(':', 2)
            reverse = True if sort_dir == 'desc' else False

        sort_attrs = sort_flds.split(',')

        types = cls.__model_attr_type(sort_attrs, items)
        def key_smith(o):
            key_ring = [cls.__DEFAULT_SORT_VALUE[types[i]] if o[f] == None else o[f] for i,f in enumerate(sort_attrs)]
            return key_ring

        # In Place
        # items.sort(key=key_smith)
        # return None

        # As New List
        return sorted(items, key=key_smith, reverse=reverse)

    # Used to do integer comparisons via the Tinydb.Query.test() method.
    # This is used b/c is solves the problem of being able to compare values
    # when a db field's value can be None (null).
    # If the db_val is None assume no match/False.
    # Without this (using straight TinyDb) you will get this error if the db
    # field contains null/None:
    #   => 'TypeError: '>' not supported between instances of 'NoneType' and 'int'
    @staticmethod
    def cmp_integer(doc_val, op, test_val):
        result = False
        if doc_val is not None:
            values = test_val.split(':')
            values = [int(val) for val in values]
            if op == 'ne':
                result = doc_val != values[0]
            elif op == 'gt':
                result = doc_val > values[0]
            elif op == 'gte':
                result = doc_val >= values[0]
            elif op == 'lt':
                result = doc_val < values[0]
            elif op == 'lte':
                result = doc_val <= values[0]
            elif op == 'btw':
                result = values[0] <= doc_val <= values[1]
            else:
                result = doc_val == values[0]

        return result
