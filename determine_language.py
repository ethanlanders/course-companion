class CodeLanguageIdentifier:
    """
    Identifies the programming language of a code block.

    Looks for the presence of specific keywords unique to each programming language.

    Attributes:
        languages_patterns (dict): A dictionary mapping programming languages to lists
                                    of unique keywords and syntax patterns associated with each language.
    """
    def __init__(self):
        self.languages_patterns = {
            #'Python': ['def ', 'import ', 'from ', 'class ', ':', 'print(', 'lambda '],
            'Python': ['def ', 'import ', 'from ', 'class ', 'print(', 'lambda '],
            'JavaScript': ['function ', '=>', 'var ', 'let ', 'const ', 'console.log('],
            'Java': ['public class', 'public static void main', 'import java.', 'new '],
            'C++': ['#include ', 'int main()', 'std::', 'cout <<', 'cin >>'],
            'Rust': ['fn ', 'let ', 'mut ', 'match ', 'trait ', 'enum '],
            'Kotlin': ['fun ', 'val ', 'var ', 'println(', 'import '],
        }

    def identify_language(self, code_block):
        """
        Identifies the programming language of a  code block.

        Args:
            code_block (str): The code block string

        Returns:
            str: The language with the highest score or, if there is no match, it returns "Unknown".
        """
        scores = {language: 0 for language in self.languages_patterns}

        for language, patterns in self.languages_patterns.items():
            for pattern in patterns:
                if pattern in code_block:
                    scores[language] += 1

        # find highest score
        identified_language = max(scores, key=scores.get)
        if scores[identified_language] == 0:
            return "Unknown"

        return identified_language


