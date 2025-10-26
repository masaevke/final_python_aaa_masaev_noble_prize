import statistics
from typing import List, Any, Dict, Tuple
from operator import itemgetter
from collections import Counter


def mean(values: List[Any]) -> float:
    return statistics.mean(values) if values else 0


def median(values: List[Any]) -> float:
    return statistics.median(values) if values else 0


def mode(values: List[Any]) -> Any:
    return statistics.mode(values) if values else None


def count(data: List[Any]) -> int:
    return len(data)


def unique_count(data: List[Dict]) -> int:
    """кол-во уникальных элементов"""
    if not data or not isinstance(data[0], dict):
        return len(set(data)) if data else 0

    unique_items = set()
    for item in data:
        item_tuple = tuple(sorted((k, str(v)) for k, v in item.items()))
        unique_items.add(item_tuple)
    return len(unique_items)


def top_n(
    data: List[Dict], field: str, n: int = 5, reverse: bool = True
) -> List[Tuple[Any, int]]:
    """
    функция выводит топ значений по полю

    Args:
        data: список словарей
        field: поле для анализа
        n: количество топовых элементов
        reverse: первые или последние

    Returns:
        список кортежей
    """
    counter = {}
    for item in data:
        value = item.get(field)
        if value is not None:
            counter[value] = counter.get(value, 0) + 1

    sorted_items = sorted(counter.items(), key=itemgetter(1), reverse=reverse)
    return sorted_items[:n]


def describe_numeric(values: List[Any]) -> Dict[str, Any]:
    """
    все вместе+описательные статистики
    """
    if not values:
        return {}

    clean_values = [v for v in values if v is not None]
    if not clean_values:
        return {}

    return {
        "count": len(clean_values),
        "mean": statistics.mean(clean_values),
        "median": statistics.median(clean_values),
        "min": min(clean_values),
        "max": max(clean_values),
        "std": statistics.stdev(clean_values) if len(clean_values) > 1 else 0,
    }


def print_laureates_analysis(laureates_data: List[Dict]) -> None:
    """
    Общая инфа
    """
    print(f"Всего лауреатов: {count(laureates_data)}")

    unique_laureates_count = unique_count(laureates_data)
    print(f"Количество уникальных записей: {unique_laureates_count}")

    all_prizes = []
    for item in laureates_data:
        all_prizes.extend(item.get("prizes_relevant", []))

    top_categories = top_n(all_prizes, "category_en", n=5)
    print("\nТоп-5 категорий призов:")
    for cat, cnt in top_categories:
        print(f"  {cat}: {cnt}")

    all_years = [
        p.get("award_year") for p in all_prizes if p.get("award_year") is not None
    ]
    year_stats = describe_numeric(all_years)
    print(f"\nСтатистики по годам награждения:")
    for k, v in year_stats.items():
        print(f"  {k}: {v}")

    prizes_per_laureate = [
        len(item.get("prizes_relevant", [])) for item in laureates_data
    ]
    avg_prizes = mean(prizes_per_laureate)
    print(f"\nСреднее количество призов на лауреата: {avg_prizes:.2f}")

    med_prizes = median(prizes_per_laureate)
    print(f"Медианное количество призов на лауреата: {med_prizes}")

    try:
        most_common_prize_count = mode(prizes_per_laureate)
        print(
            f"Наиболее частое количество призов на лауреата: {most_common_prize_count}"
        )
    except statistics.StatisticsError:
        print("Наиболее частое количество призов: (множество модусов)")

    types = [item.get("type_") for item in laureates_data]
    type_counts = Counter(t for t in types if t)  # Фильтруем None
    print(f"\nТипы лауреатов: {dict(type_counts)}")
