from CSVManipulator import *

def check_expect(result, expected):
    if result == expected:
        print('Test passed!')
        return True
    print('expected ' + str(expected) + ' but got ' + str(result))
    return False

def format_data_t(dataManip):
    entry = [['What', 'is', '1754', '-', '3936?|-2182|3176,', '6529,', '6903']]
    expected = [{'question'    : '1754 - 3936?',
                 'answer'      : '-2182',
                 'distractors' : '3176, 6529, 6903'}]
    check_expect(dataManip.format_data(entry), expected)

def add_to_csv(dataManip):
    dataManip.add_to("What is 781 + 820?|1601|0540, 6172, 999, -835")

def delete_from_test(dataManip):
    dataManip.delete_from("781 + 820?")

def edit_question_test(dataManip):
    dataManip.edit_question("781 + 820?", "What is 781 + 820?|1601|0540, 6172, 999")

def filter_for_test(dataManip):
    req    = {"operation" : "FIND",
              "attribute" : "question",
              "value"     : "6352 + 976?"}

    result = dataManip.filter_for(req)
    print("FIND test: 6352 + 976?")
    for row in result:
        print(row)

    reqF    = {"operation" : "FIND",
               "attribute" : "answer",
               "value"     : "4112"}

    resultF = dataManip.filter_for(reqF)
    print("FIND test: 4112")
    for row in resultF:
        print(row)

    req    = {"operation" : "FIND",
              "attribute" : "distractors",
              "value"     : "368, 9268, 3949, 1417"}

    result = dataManip.filter_for(req)
    print("FIND test: 368, 9268, 3949, 1417")
    for row in result:
        print(row)

    reqG    = {"operation" : "GT",
               "attribute" : "answer",
               "value"     : "4112"}

    resultG = dataManip.filter_for(reqG)
    print("GT test: 4573")
    for row in resultG:
        print(row)

    reqL    = {"operation" : "LT",
               "attribute" : "answer",
               "value"     : "4112"}

    resultL = dataManip.filter_for(reqL)
    print("LT test: 4573")
    for row in resultL:
        print(row)

    check_expect(len(resultF) + len(resultG) + len(resultL), len(dataManip.dataEntries))

def sort_by_test(dataManip, op, att):
    req = {"operation" : op,
           "attribute" : att
          }
    dataManip.sort_by(op, att)

if __name__ == "__main__":
    dataManip = CSVManipulator('data/code_challenge_question_dump.csv')
    add_to_csv(dataManip)
    delete_from_test(dataManip)
    add_to_csv(dataManip)
    edit_question_test(dataManip)
    filter_for_test(dataManip)
    sort_by_test(dataManip, 'LT', 'answer')
    sort_by_test(dataManip, 'LT', 'question')
