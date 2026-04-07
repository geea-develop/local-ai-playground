"""
Data Skill
Provides data manipulation and analysis utilities
"""

from typing import List, Dict, Any


def flatten_list(nested_list: List[Any]) -> List[Any]:
    """Flatten a nested list"""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def group_by_key(data: List[Dict], key: str) -> Dict[Any, List[Dict]]:
    """Group list of dictionaries by a specific key"""
    grouped = {}
    for item in data:
        if key in item:
            group_key = item[key]
            if group_key not in grouped:
                grouped[group_key] = []
            grouped[group_key].append(item)
    return grouped


def filter_by_condition(data: List[Dict], key: str, value: Any) -> List[Dict]:
    """Filter list of dictionaries by key-value condition"""
    return [item for item in data if item.get(key) == value]


if __name__ == "__main__":
    nested = [[1, 2], [3, [4, 5]], 6]
    print(f"Flattened: {flatten_list(nested)}")
    
    people = [
        {"name": "Alice", "city": "NYC"},
        {"name": "Bob", "city": "LA"},
        {"name": "Charlie", "city": "NYC"},
    ]
    print(f"Grouped by city: {group_by_key(people, 'city')}")
    print(f"People in NYC: {filter_by_condition(people, 'city', 'NYC')}")
