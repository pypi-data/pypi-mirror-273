import argparse
import json
class Jsons:
    """класс Jsons добавляет новые функции, которых нет в стандартном модуле Json"""

    def __init__(self, json_file):
        """
        Инициализирует экземпляр класса Jsons и загружает данные из JSON-файла.

        :param json_file: Путь к JSON-файлу.
        """
        self.json_data = self.load_json(json_file)

    def load_json(self, json_file):
        """
        Загружает JSON данные из указанного файла.

        :param json_file: Путь к JSON-файлу.
        :return: Содержимое JSON-файла в виде Python объектов (dict, list и т.д.).
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return None

    def max_depth(self, data=None):
        """
        Вычисляет максимальную глубину вложенности JSON данных.

        :param data: JSON данные для вычисления глубины. Если не указано, используется загруженный JSON.
        :return: Максимальная глубина вложенности JSON данных.
        """
        if data is None:
            data = self.json_data

        if isinstance(data, dict):
            if not data:
                return 1
            return 1 + max(self.max_depth(value) for value in data.values())
        elif isinstance(data, list):
            if not data:
                return 1
            return 1 + max(self.max_depth(item) for item in data)
        else:
            return 0

    def find_by_value(self, value, data=None):
        """
        Ищет все вхождения заданного значения в JSON данных.

        :param value: Значение для поиска.
        :param data: JSON данные для поиска. Если не указано, используется загруженный JSON.
        :return: Список ключей, связанных с заданным значением.
        """
        if data is None:
            data = self.json_data

        results = []

        if isinstance(data, dict):
            for k, v in data.items():
                if v == value:
                    results.append(k)
                results.extend(self.find_by_value(value, v))
        elif isinstance(data, list):
            for item in data:
                results.extend(self.find_by_value(value, item))

        return results

    def find_by_key(self, key, data=None):
        """
        Ищет все вхождения заданного ключа в JSON данных.

        :param key: Ключ для поиска.
        :param data: JSON данные для поиска. Если не указано, используется загруженный JSON.
        :return: Список значений, связанных с заданным ключом.
        """
        if data is None:
            data = self.json_data

        results = []

        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    results.append(v)
                results.extend(self.find_by_key(key, v))
        elif isinstance(data, list):
            for item in data:
                results.extend(self.find_by_key(key, item))

        return results




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jsons")
    parser.add_argument("--method", choices=["__init__", "load_json", "max_depth", "find_by_value", "find_by_key"], help="Method name to display documentation")

    args = parser.parse_args()

    if args.method:
        print(getattr(Jsons, args.method).__doc__)