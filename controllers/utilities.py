import hashlib

class Utilities:

    def hash_row(sql_row):
        row_string = ','.join(map(str, sql_row))

        hash_object = hashlib.md5()

        hash_object.update(row_string.encode())

        hash_result = hash_object.hexdigest()

        return hash_result

    #sql_row = [1, 'John', 'Doe', 'john.doe@example.com']
