import csv

"""
CSVManipulator is a class with methods that interact with a CSV file. It has
two properties:
    dataEntries: a list of dictionaries that represent the rows of the CSV file.
    filename:    the name of the CSV file that is being serviced.
"""
class CSVManipulator():
    def __init__(self, filename):
        self.filename    = filename
        self.dataEntries = self.format_data(self.read_csv())

    """
    open_csv is a method that takes no arguments and returns the current contents
    of the CSV file referenced by 'filename' without the column headings.
    """
    def read_csv(self):
        csvValues = []
        with open(self.filename, newline='') as f:
            csvReader = csv.reader(f, delimiter=' ')
            for row in csvReader:
                csvValues.append(row)
        return csvValues[1:]

    """
    write_csv is a method that takes a list of dictionaries newEntries in the
    same format as 'dataEntries' and a string representing the  mode for opening
    the CSV file. It writes the contents of newEntries to 'filename'.
    """
    def write_csv(self, newEntries, mode):
        with open(self.filename, mode, newline='') as f:
            csvWriter = csv.writer(f)
            if mode == 'w':
                csvWriter.writerow(["question|answer|distractors"])
            for newEntry in newEntries:
                csvWriter.writerow(newEntry.split(','))

    """
    format_data takes a 2D iterable of strings that represent rows of 'filename'
    and returns a list of dictionaries that represent each row of 'filename'.
    Output has the format:
          {'question' : '...', 'answer' : '...', 'distractors' : '...'}
    """
    def format_data(self, dataEntries):
        formattedData = []
        for row in dataEntries:
            question    = row[2] + ' ' + row[3] + ' ' + row[4].split('|')[0]
            answer      = row[4].split('|')[1]
            distractors = row[4].split('|')[-1] + ' ' + ' '.join(row[5:])
            formattedData.append({'question'    : question,
                                  'answer'      : answer,
                                  'distractors' : distractors})
        return formattedData

    """
    unformat_data takes a list of dictionaries dataEntries and returns a list of
    strings that can be written to 'filename'.
    """
    def unformat_data(self, dataEntries):
        unformattedData = []
        for row in dataEntries:
            unformattedData.append("What is " + row['question'] + '|'
                                              + row['answer']   + '|'
                                              + row['distractors'])
        return unformattedData

    """
    add_to takes a data entry as a string, adds it to 'dataEntries', and appends
    it to 'filename'.
    """
    def add_to(self, entry):
        self.dataEntries.extend(self.format_data([entry.split(' ')]))
        self.write_csv([entry], 'a')

    """
    delete_from takes a question as a string, and if the question exists in
    'dataEntries', it removes the corresponding dictionary from 'dataEntries'.
    It always writes the result to 'filename'.
    """
    def delete_from(self, question):
        newEntries = []
        for row in self.dataEntries:
            if question != row["question"]:
                newEntries.append(row)
        self.dataEntries = newEntries
        self.write_csv(self.unformat_data(self.dataEntries), 'w')

    """
    edit_question takes a question as a string and if the question exists in
    'dataEntries', it edits the corresponding dictionary in the list. It always
    writes the result to 'filename'.
    """
    def edit_question(self, question, newString):
        newQ = self.format_data([newString.split(' ')])[0]
        for row in self.dataEntries:
            if question == row['question']:
                row['question']    = newQ['question']
                row['answer']      = newQ['answer']
                row['distractors'] = newQ['distractors']

        self.write_csv(self.unformat_data(self.dataEntries), 'w')

    """
    filter_find is a higher order method that filters dataEntries based on if a
    predicate returns True or False. The type of the predicate must be
    'a -> bool, where 'a represents a consistent polymorphic type.
    """
    def filter_find(self, predicate):
        filteredData = []
        for row in self.dataEntries:
            if predicate(row):
                filteredData.append(row)
        return filteredData

    """
    typeconv is a method that returns a function based on the 'attributes'
    entry of a dictionary req. typeconv returns the proper type conversion
    function for either questions or answers.
    """
    def typeconv(self, req):
        if req['attribute'] == 'answer':
            return float
        else:
            return lambda x : (float(x.split(' ')[0]), float(x.replace('?','').split(' ')[2]))

    """
    filter_for calls filter_find with various predicates based on the entries of
    req. It can search for a question/answer, find all entries less than a
    question/answer, or find all entries greater than a question/answer.
    """
    def filter_for(self, req):
        typeconv = self.typeconv(req)

        if req['operation'] == "FIND":
            pred = lambda x : typeconv(x[req['attribute']]) == typeconv(req['value'])
        elif req['operation'] == "GT":
            pred = lambda x : typeconv(x[req['attribute']]) > typeconv(req['value'])
        elif req['operation'] == "LT":
            pred = lambda x : typeconv(x[req['attribute']]) < typeconv(req['value'])
        return self.filter_find(pred)

    """
    sort_by takes two strings operation and attribute. It sorts 'dataEntries' by
    operation based on the given attribute ('question', 'answer'). It then writes
    the results to 'filename'.
    """
    def sort_by(self, operation, attribute):
        choose = lambda r : self.typeconv({'attribute' : attribute})(r[attribute])

        if operation == "LT":
            self.dataEntries = sorted(self.dataEntries, key=choose)
        if operation == "GT":
            self.dataEntries = sorted(self.dataEntries, reverse=True, key=choose)
        self.write_csv(self.unformat_data(self.dataEntries), 'w')
