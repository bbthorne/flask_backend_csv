/*
InputHandler is a class that interacts with the API endpoints in app.py and
displays results to index.html. It has three properties:
  operation: the current operation the user would like to perform on the CSV.
  userInput: any user input that influences the operation request.
  options  : the current additional information required to do the operation.
*/
class InputHandler {
  constructor() {
    this.operation = "None";
    this.userInput = "None";
    this.options   = [];
  }
  /*
  handle_input is called when the submit button is pressed. It processes all of
  the commands provided by the user and calls the appropriate functions.
  */
  handle_input()
  {
    switch(this.operation) {
      case "CREATE":
        this.create_question();
        break;
      case "DELETE":
        this.delete_question();
        break;
      case "EDIT":
        this.edit_question();
        break;
      case "FILTER":
        this.filter_questions();
        break;
      case "SORT":
        this.sort_questions();
        break;
      default:
        return "Operation not Supported";
    }
  }

  /* Methods to edit internal variables based on actions on the page. */
  edit_operation(op)
  {
    this.operation = op
  }

  edit_options(opts)
  {
    this.options = opts
  }

  edit_userInput(input)
  {
    this.userInput = this.validate(input)
  }

  /* validate checks to see if user input is malicious for this application */
  validate(input)
  {
    let newInput = input.replace(/<>[]{}\(\)!@#\$%\^&~``'"/, "");
    return newInput
  }

  /*
  formatted_fullQ takes aString and runs it against a regular expression to see
  if it has the correct format for a question. It then returns an edited version
  that can be sent as input to API endpoints. If the input is in the wrong
  format, it returns "Ill-Formatted".
  */
  formatted_fullQ(aString) {
    let regex = /^((\-)*[0-9]+ [\+\-\*\/] (\-)*[0-9]+ = (\-)*[0-9]+(, (\-)*[0-9]+)*)$/;
    if (regex.test(aString)) {
      let input       = aString.split(' ')
      let commaSep    = input.slice(4,input.length)
      let answer      = commaSep[0].replace(',','')
      let distractors = ""
      for (let i=1; i<commaSep.length-1; i++) {
        distractors = distractors + commaSep[i] + " ";
      }
      distractors += commaSep[commaSep.length-1]
      return "What is " + input[0] + " " + input[1] + " " + input[2] + "?" + "|" + answer + "|" + distractors;
    } else {
      return "Ill-Formatted";
    }
  }

  /*
  formatted_partialQ is similar to formatted_fullQ, but for questions only, not
  an entire entry. It returns an edited version of aString if the input is in
  the correct form, and "Ill-formatted" otherwise.
  */
  formatted_partialQ(aString) {
    let regex = /^((\-)*[0-9]+ [\+\-\*\/] (\-)*[0-9]+)$/;
    if (regex.test(aString)) {
      return aString + "?";
    } else {
      return "Ill-Formatted";
    }
  }

  /*
  create_question is a method that makes an XMLHttpRequest to /api/createQ given
  that 'userInput' is in the correct format. It displays a success or failure
  message to index.html.
  */
  create_question()
  {
    let self    = this;
    let request = new XMLHttpRequest();

    request.open("POST", "http://127.0.0.1:5000/api/createQ", true);
    request.onreadystatechange = function() {
      if (request.readyState == 4 && request.status == 200) {
        let data = request.responseText;
        if (data == "Success!") {
          document.getElementById("results").innerHTML = self.userInput + " was successfully added.";
        } else {
          document.getElementById("results").innerHTML = self.userInput + " could not be added.";
        }
      }
    }
    let msg = this.formatted_fullQ(this.userInput);
    if (msg != "Ill-Formatted") {
      request.send(msg);
    } else {
      document.getElementById("results").innerHTML = "Please use the format 'arg1 op arg2 = ans, dist1, dist2, ..., distn' to add a question.";
    }
  }

  /*
  delete_question is a method that makes an XMLHttpRequest to /api/deleteQ given
  that 'userInput' is in the proper format. It displays a success or failure
  message to index.html.
  */
  delete_question()
  {
    let self    = this;
    let request = new XMLHttpRequest();

    request.open("POST", "http://127.0.0.1:5000/api/deleteQ", true);
    request.onreadystatechange = function() {
      if (request.readyState == 4 && request.status == 200) {
        let data = request.responseText;
        if (data == "Success!") {
          document.getElementById("results").innerHTML = self.userInput + " was successfully deleted.";
        } else {
          document.getElementById("results").innerHTML = self.userInput + " could not be deleted.";
        }
      }
    }
    let msg = this.formatted_partialQ(this.userInput);
    if (msg != "Ill-Formatted") {
      request.send(msg);
    } else {
      document.getElementById("results").innerHTML = "Please use the format 'arg1 op arg2' to delete a question.";
    }
  }

  /*
  edit_question is a method that makes an XMLHttpRequest to /api/editQ given
  that 'userInput' is a valid partial question and 'options' contains a string
  representing a valid full question. It displays a success or failure message
  to index.html.
  */
  edit_question()
  {
    let self    = this;
    let request = new XMLHttpRequest();

    request.open("POST", "http://127.0.0.1:5000/api/editQ", true);
    request.setRequestHeader("Content-Type", "application/json");

    request.onreadystatechange = function() {
      if (request.readyState == 4 && request.status == 200) {
        let data = request.responseText;
        if (data == "Success!") {
          document.getElementById("results").innerHTML = self.userInput + " was successfully edited to " + self.options[0] + ".";
        } else {
          document.getElementById("results").innerHTML = self.userInput + " could not be edited to " + self.options[0] + ".";
        }
      }
    }
    let q    = this.formatted_partialQ(this.userInput);
    let newQ = this.formatted_fullQ(this.options[0]);
    if (q != "Ill-Formatted" && newQ != "Ill-Formatted") {
      request.send(JSON.stringify({"question" : q, "newQ" : newQ}))
    } else {
      document.getElementById("results").innerHTML = "Please use the format 'arg1 op arg2' to select a question to edit\n\
                                                      and 'arg1 op arg2 = ans, dist1, dist2, ..., distn' to change it.";
    }
  }

  /*
  filter_questions is a method that makes an XMLHttpRequest to /api/filter
  given that 'userInput' is in the correct format based on the contents of
  'options'. It displays a success or failure message to index.html.
  */
  filter_questions()
  {
    let self    = this;
    let request = new XMLHttpRequest();

    request.open("POST", "http://127.0.0.1:5000/api/filter", true);
    request.setRequestHeader("Content-Type", "application/json");

    request.onreadystatechange = function() {
      if (request.readyState == 4 && request.status == 200) {
        let data = self.format_output(JSON.parse(request.responseText))
        let responseString = ""
        if (data.length == 0) {
          document.getElementById("results").innerHTML = "Filter Result(s):<br/>None";
        }
        else if (data[0]["question"] !== "Failure!") {
          let displayString = "Question = Answer | Distractors<br/>";
          for (let i = 0; i < data.length; i++) {
            displayString += data[i]["question"].replace("?", "");
            displayString += " = " + data[i]["answer"] + " | " + data[i]["distractors"] + "<br/>";
          }
          document.getElementById("results").innerHTML = "Filter Result(s):<br/>" + displayString;
        } else {
        }
      }
    }
    let question = ""
    if (this.options[1] == "question") {
      question = this.formatted_partialQ(this.userInput)
    } else if (this.options[1] == "answer") {
      if (/^[0-9]+$/.test(this.userInput)) {
        question = this.userInput;
      }
    } else {
        question = "Ill-Formatted"
    }
    if (question != "Ill-Formatted") {
      request.send(JSON.stringify({"operation" : this.options[0],
                                   "attribute" : this.options[1],
                                   "value"     : question}))
    } else {
      document.getElementById("results").innerHTML = "Please enter a question or an answer.";
    }
  }

  /*
  sort_questions is a method that makes an XMLHttpRequest to /api/sort based on
  the contents of 'options'. It displays a success or failure message to index.html.
  */
  sort_questions()
  {
    let request = new XMLHttpRequest();

    request.open("POST", "http://127.0.0.1:5000/api/sort");
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
      if (request.readyState == 4 && request.status == 200) {
        if (request.responseText == "Success!") {
          document.getElementById("results").innerHTML = "Entries successfully sorted.";
        } else {
          document.getElementById("results").innerHTML = "The entries could not be sorted."
        }
      }
    }
    request.send(JSON.stringify({"operation" : this.options[0],
                                 "attribute" : this.options[1]}));
  }

  /*
  view_all is a method that makes an XMLHttpRequestq to /api/viewall. It
  displays the contents of the CSV file serviced by the API.
  */
  view_all()
  {
    let request = new XMLHttpRequest();
    let self    = this;
    request.open("GET", "http://127.0.0.1:5000/api/viewall");
    request.onreadystatechange = function () {
      if (request.readyState == 4 && request.status == 200) {
        let data = self.format_output(JSON.parse(request.responseText));
        let displayString = "Question = Answer | Distractors<br/>";
        for (let i = 0; i < data.length; i++) {
          displayString += data[i]["question"].replace("?", "");
          displayString += " = " + data[i]["answer"] + " | " + data[i]["distractors"] + "<br/>";
        }
        document.getElementById("results").innerHTML = displayString;
      }
    }
    request.send();
  }

  /*
  format_output takes output as a string and adds proper whitespace to align the
  output of each row in the string.
  */
  format_output(output)
  {
    let maxQLength = 0;
    let maxALength = 0;

    for (let i = 0; i < output.length; i++) {
      if (maxQLength < output[i]['question'].length) {
        maxQLength = output[i]['question'].length;
      }
      if (maxALength < output[i]['answer'].length) {
        maxALength = output[i]['answer'].length;
      }
    }
    for (let i = 0; i < output.length; i++) {
      let j = output[i]['question'].length;
      let k = output[i]['answer'].length;
      for (;j < maxQLength; j++) {
        output[i]['question'] += '&nbsp;';
      }
      for (;k < maxALength; k++) {
        output[i]['answer'] += '&nbsp;';
      }
    }
    return output
  }
}
