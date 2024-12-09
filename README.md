# QA_Extraction
##Question and Answer extraction from JSON file and storing the result as csv file.

Getting Started

Prerequisites

To run the Python script, you need to have Python 3.x installed on your system.

Installation
	• Clone this repository to your local machine.
	• Open a terminal and navigate to the directory where you cloned the repository.
	• Run the Python script using the following command:
		python my_script.py
		
Explanation of the script:
	• This python script takes the input as json file
	• This function  get_json_file_data(file_path) returns the JSON data as a result from the json file .
	• In this function extract_question_and_answer(json_data),sending  input as json data from json file 
		○ There are four cases
			§  if both problem keyword and the solution keyword is present in the description field of the json entry,framing a dictionary named(qa_dict) with Question and Solution as keys storing that dictionary into the list for writing  in csv file.
			§ If only the problem keyword is present in the description field ,frame a dictionary named(qa_dict) with Question ,in this case check if the solution keyword is present in the latest comment,if found add a key named Solution  with the result and  storing that dictionary into the list for writing  in csv file.
			§ If only the solution keyword is present in the description field ,frame a dictionary named(qa_dict) with Solution ,in this case check if the Problem keyword is present in the latest comment, if found add a key named Question with the result and  storing that dictionary into the list for writing  in csv file.
			§ If both problem keyword and the solution keyword are not present in the description field, check in the latest comment ,if found ,framing a dictionary named(qa_dict) with Question and Solution as keys storing that dictionary into the list for writing  in csv file.
	• If problem keyword is not present in both description and comments added the summary of that particular json entry
	• If solution keyword not present in both description and comments added the text as Solution not available with the link of that entry.
	• Finally create a csv file with the list of all dictionaries.
		
