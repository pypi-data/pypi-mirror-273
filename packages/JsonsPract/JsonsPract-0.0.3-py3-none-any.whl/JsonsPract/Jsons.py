
class Jsons:


    def __init__(self, key, value):

        self.key = key
        self.value = value

    def to_dict(self):

        return {'key': self.key, 'value': self.value}

    @classmethod
    def from_dict(cls, data):

        return cls(data['key'], data['value'])

    def to_json(self):

        return '{{"key": "{}", "value": "{}"}}'.format(self.key, self.value)

    @classmethod
    def from_json(cls, json_str):

        data_dict = json_str.strip('{}').split(', ')
        key = data_dict[0].split(': ')[1].strip('"')
        value = data_dict[1].split(': ')[1].strip('"')
        return cls(key, value)

    def __repr__(self):

        return f'Jsons({self.key}, {self.value})'

    def concatenate_json(json_str1, json_str2):

        # Удаляем начальные и конечные фигурные скобки и пробелы
        json_str1 = json_str1.strip('{} ')
        json_str2 = json_str2.strip('{} ')

        # Разбиваем строки JSON по запятой и создаем списки
        json_list1 = json_str1.split(',')
        json_list2 = json_str2.split(',')

        # Создаем в новый список объединяя элементы обоих списков
        merged_list = json_list1 + json_list2

        # Удаляем пробелы и создаем строку JSON снова
        concatenated_json = '{' + ', '.join(merged_list) + '}'

        return concatenated_json

    def is_valid_json_structure(json_str):

        stack = []
        within_quotes = False

        for i, char in enumerate(json_str):
            if char == '"':
                if i > 0 and json_str[i - 1] != '\\':
                    within_quotes = not within_quotes
            elif not within_quotes:
                if char == '{':
                    stack.append(char)
                elif char == '}':
                    if not stack or stack.pop() != '{':
                        return False
                elif char == ',':
                    if json_str[i + 1] == '  ':
                        return False

        return len(stack) == 0

    def max_json_depth(json_str):

        depth = 0
        max_depth = 0

        for char in json_str:
            if char == '{':
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == '}':
                depth -= 1

        return max_depth


