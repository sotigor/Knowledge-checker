
def get_subjects() -> list:
    """
    Get list of subject names from text file
    :return: list of subject names
    """
    with open("./txt files/subjects.txt", 'r', encoding="UTF-8") as subj:
        subjects_list = []
        for i in subj.readlines():
            subjects_list.append(i.strip())
    return subjects_list

def get_difficulty() -> list:
    """
    Get list of difficulty levels from text file
    :return: list of difficulty levels
    """
    with open("./txt files/difficulty_levels.txt", 'r', encoding="UTF-8") as diff_lev:
        difficulty_list = []
        for i in diff_lev.readlines():
            difficulty_list.append(i.strip())
        return difficulty_list

def get_number_of_ques() -> list:
    """
    Get number of questions list from text file
    :return: list with number of questions
    """
    with open("./txt files/number_of_questions.txt", 'r', encoding="UTF-8") as num_of_ques:
        num_of_quest_list = []
        for i in num_of_ques.readlines():
            num_of_quest_list.append(i.strip())
        return num_of_quest_list

