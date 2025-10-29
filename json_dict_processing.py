from typing import Any, Callable, Dict, List, Tuple, Union


def extract_nested_value(obj: Any, keys: List[str], none: Any = None) -> Any:
    """
    функция измлекает значение из вложенного словаря/списка по цепочке ключей,
    если путь не существует — возвращает none.

    Args:
        obj: исходный объект
        keys: список ключей или индексов для последовательного доступа
        none: значение, возвращаемое при отсутствии пути

    Returns:
        значение по указанному пути или none
    """
    current = obj
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and key.isdigit():
            idx = int(key)
            if 0 <= idx < len(current):
                current = current[idx]
            else:
                return none
        else:
            return none
    return current


def process_dictionary_with_config(
    dictionary: Dict, config: Dict[str, Union[List[str], Tuple[List[str], Callable]]]
) -> Dict[str, Any]:
    """
    функция обрабатывает словарь 

    Args:
        dictionary: входной словарь с вложенными данными
        config: конфигурация вида:
                - {атрибут: [путь, к, данным]} — без трансформации,
                - {атрибут: ([путь, к, данным], обработка)} — с трансформацией

    Returns:
        плоский словарь с извлечёнными и преобразованными значениями
    """
    result = {}
    for attr_name, spec in config.items():
        if isinstance(spec, tuple):
            path_list, transform = spec
            raw_value = extract_nested_value(dictionary, path_list)
            if raw_value is not None:
                try:
                    result[attr_name] = transform(raw_value)
                except (ValueError, TypeError):
                    result[attr_name] = None
            else:
                result[attr_name] = None
        else:
            result[attr_name] = extract_nested_value(dictionary, spec)
    return result


def process_list_of_dicts_with_config(
    list_of_dicts: List[Dict],
    config: Dict[str, Union[List[str], Tuple[List[str], Callable]]],
) -> List[Dict[str, Any]]:
    """
    обработка списка словарей
    
    Args:
        list_of_dicts: список словарей для обработки
        config: конфигурация извлечения и преобразования полей

    Returns:
        список плоских обработанныхз словарей
    """
    return [process_dictionary_with_config(item, config) for item in list_of_dicts]


def create_processor(
    config: Dict[str, Union[List[str], Tuple[List[str], Callable]]],
    list_processor: bool = False,
) -> Callable:
    """
    создает готовый процессор с предзагруженной конфигурацией.

    Args:
        config: конфигурация обработки полей
        list_processor: если True - процессор принимает список словарей
                        если False — один словарь

    Returns:
        функция-процессор, принимающая данные и возвращающая результат
    """
    if list_processor:
        return lambda data_list: process_list_of_dicts_with_config(data_list, config)
    else:
        return lambda data_dict: process_dictionary_with_config(data_dict, config)
