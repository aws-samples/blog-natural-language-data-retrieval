# create a class called UserInputs.This class holds a set of example user requests,
# and returns string based on an index.
class TestCases:

    # a static method to return a string based on an index
    @staticmethod
    def get_test_case(index: int):
        # a list of example user requests (aka queries)
        strings = [
            "Where were the olympics held in 2016?",
            "When were the olympics held in London?",
            "In what games did Usain Bolt compete?",
            "How many vacation days does John Doe have remaining?",
            "In what games did Isabelle Werth, Nedo Nadi and Allyson Felix compete?",
            "Where does Isabelle Werth train for the games?",
            "Did Isabelle Werth train for the games in Paris?"
        ]

        # Check if the index is in bounds,  if not, return an empty string
        if index < 0 or index >= len(strings):
            print(f"Test input index: {index} is out of bounds")
            return ""
        # return a string based on an index
        return strings[index]
