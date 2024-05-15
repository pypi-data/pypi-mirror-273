import argparse
class Jsons:
    """Jsons type representing key-value pairs."""

    def __init__(self, key, value):
        """
        Initialize Jsons object.

        Args:
            key (str): The key of the data.
            value (str): The value associated with the key.
        """
        self.key = key
        self.value = value

    def to_dict(self):
        """
        Convert Jsons object to a dictionary.

        Returns:
            dict: A dictionary representation of the Jsons object.
        """
        return {'key': self.key, 'value': self.value}

    @classmethod
    def from_dict(cls, data):
        """
        Create a Jsons object from a dictionary.

        Args:
            data (dict): The dictionary containing 'key' and 'value' keys.

        Returns:
            Jsons: A Jsons object created from the dictionary.
        """
        return cls(data['key'], data['value'])

    def to_json(self):
        """
        Convert Jsons object to a JSON string.

        Returns:
            str: A JSON string representation of the Jsons object.
        """
        return '{{"key": "{}", "value": "{}"}}'.format(self.key, self.value)

    @classmethod
    def from_json(cls, json_str):
        """
        Create a Jsons object from a JSON string.

        Args:
            json_str (str): A JSON string representing the Jsons object.

        Returns:
            Jsons: A Jsons object created from the JSON string.
        """

        data_dict = json_str.strip('{}').split(', ')
        key = data_dict[0].split(': ')[1].strip('"')
        value = data_dict[1].split(': ')[1].strip('"')
        return cls(key, value)

    def __repr__(self):
        """
        Return a string representation of the Jsons object.

        Returns:
            str: A string representation of the Jsons object.
        """
        return f'Jsons({self.key}, {self.value})'

    def concatenate_json(json_str1, json_str2):
        """
        Concatenate two JSON structures.

        Args:
            json_str1 (str): The first JSON structure as a string.
            json_str2 (str): The second JSON structure as a string.

        Returns:
            str: A JSON string representing the concatenated JSON structures.
        """
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
        """
        Check if the JSON structure has balanced curly brackets and proper comma separators.

        Args:
            json_str (str): The JSON structure as a string.

        Returns:
            bool: True if the JSON structure is valid, False otherwise.
        """
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
        """
        Calculate the maximum depth of a JSON structure.

        Args:
            json_str (str): The JSON structure as a string.

        Returns:
            int: The maximum depth of the JSON structure.
        """
        depth = 0
        max_depth = 0

        for char in json_str:
            if char == '{':
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == '}':
                depth -= 1

        return max_depth

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jsons")
    parser.add_argument("--method", choices=["to_dict", "from_dict", "to_json", "from_json", "__repr__", "concatenate_json", "is_valid_json_structure", "max_json_depth"], help="Method name to display documentation")

    args = parser.parse_args()

    if args.method:
        print(getattr(Jsons, args.method).__doc__)
