from json_dict_processing import create_processor

# конфиг для обработки приза
CONFIG_PRIZE = {
    "prize_amount": ["prizeAmount"],
    "prize_amount_adjusted": ["prizeAmountAdjusted"],
    # мейби это лишняя обработка, но я не знаю как записан год
    "award_year": (
        ["awardYear"],
        lambda s: int(s[:4]) if s and s[:4].isdigit() else None,
    ),
    "category_en": ["category", "en"],
    "prize_status": ["prizeStatus"],
}


# процессор для обработки списка призов
def prize_processor():
    return create_processor(CONFIG_PRIZE, list_processor=True)
