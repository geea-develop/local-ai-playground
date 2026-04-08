"""
Text Processing Skill
Provides utilities for text manipulation and analysis
"""

def uppercase_transform(text: str) -> str:
    """Convert text to uppercase"""
    return text.upper()


def reverse_text(text: str) -> str:
    """Reverse the given text"""
    return text[::-1]


def word_count(text: str) -> int:
    """Count the number of words in the text"""
    return len(text.split())


if __name__ == "__main__":
    sample = "Hello Claude Playground"
    print(f"Original: {sample}")
    print(f"Uppercase: {uppercase_transform(sample)}")
    print(f"Reversed: {reverse_text(sample)}")
    print(f"Word count: {word_count(sample)}")
