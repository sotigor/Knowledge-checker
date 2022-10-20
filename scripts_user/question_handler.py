
def modify_question(question: str) -> str:
    """
    Split long questions in two rows
    :param question: it is a string for work with 
    :return: the same or modified question 
    """
    if len(question) > 30:
        if question.find(':') != -1:
            return question[0:question.find(':')+1] + '\n' + question[question.find(':')+1:]
        ind_gaps = []
        for ind, val in enumerate(question):
            if val == " " and (37 - ind) > 0:
                ind_gaps.append(ind)
        opt_val = max(ind_gaps)
        return question[0:opt_val] + '\n' + question[opt_val:]
    return question