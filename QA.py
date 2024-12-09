import json
import csv

def get_json_file_data(file_path):
    with open(file_path, encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

def get_problem(text):
    problem_keyword='#Problem#'
    solution_keyword='#Solution#'
    text_lower = text.lower()
    problem_index=text_lower.find(problem_keyword.lower())
    solution_index = text_lower.find(solution_keyword.lower())
    if(problem_index!=-1 and solution_index!=-1):
        problem_text = text[problem_index+len(problem_keyword):solution_index].strip()
        print(problem_text)
        return problem_text
    elif(problem_index!=-1 and solution_index==-1):
        problem_text = text[problem_index+len(problem_keyword):].strip()
        return problem_text
    else:
        print("Error: Problem or Solution not found in text.")

def get_solution(text):
    solution_keyword = '#Solution#'
    solution_index = text.lower().find(solution_keyword.lower())
    if solution_index!=-1:
        solution_text = text[solution_index+len(solution_keyword):].strip()
        print(solution_text)
        return solution_text
    else:
        print("Error: Solution not found in text.")

def get_question_and_answer_from_description(data_entry):
    print(data_entry)

    print(data_entry['id'],data_entry['description'])
    question_data=get_problem(data_entry['description'])
    solution_data =get_solution(data_entry['description'])
    print("question and answer from description",question_data,solution_data)
    return question_data,solution_data

# def get_qadict_from_comments(comments_list):
#     print('comments_list',comments_list)
#     print("--------------------------------------------------------------------------------")
#     comments_list.sort(key=lambda item:item['timestamp'], reverse=True)
#     print("latest",comments_list)
#     qa_dict={}
#     for i in range(0,len(comments_list)):
        
#         print("comments_list[i]['data']",comments_list[i]['data'])
#         question_data=get_problem(comments_list[i]['data'])
#         print(question_data)
#         solution_data=get_solution(comments_list[i]['data'])
#         print(solution_data)
#         if(question_data!=None and ('Question' not in qa_dict)):
#             print('entered in question data')
#             qa_dict['Question']=question_data
#         if(solution_data!=None and ('Solution' not in qa_dict)):
#             print('entered in solution data')
#             qa_dict['Solution']=solution_data
#         if('Question' in qa_dict and qa_dict['Question']) and ('Solution' in qa_dict and qa_dict['Solution']):
#             print("All values are there")
#             break
#         print(qa_dict)
#     return qa_dict

def get_comments_list(data_entry):
        print(data_entry['id'],data_entry['comments'])
        rtc_comments_data=data_entry['comments']
        print(type(rtc_comments_data))
        print(len(rtc_comments_data))
        rtc_comment_dict={}
        rtc_comment_list=[]
        if(len(rtc_comments_data)!=0):
            for j in range(0,len(rtc_comments_data)):
                print(rtc_comments_data)
                rtc_comment_dict['data']=rtc_comments_data[j]['data']
                rtc_comment_dict['timestamp']=rtc_comments_data[j]['timestamp']
                print("rtc_comments_dict",rtc_comment_dict)
                print(rtc_comment_dict)
                rtc_comment_list.append(rtc_comment_dict)
                rtc_comment_dict={}
            print('rtc comment list',rtc_comment_list)
        return rtc_comment_list


def restructure_qa_dict(qa_dict,data_entry):
    if 'Question' not in qa_dict:
        qa_dict['Question']=data_entry['summary']
    if 'Solution' in qa_dict:
        qa_dict['Solution'] += '\n'+data_entry['link']
    else:
        qa_dict['Solution']='Solution not available'+'\n'+data_entry['link']
    print('qa_dict',qa_dict)
    return qa_dict


def get_problem_from_comments(data_entry,qa_dict):
    rtc_comment_list=get_comments_list(data_entry)
    rtc_comment_list.sort(key=lambda item:item['timestamp'], reverse=True)
    print(rtc_comment_list)
    for i in range(0,len(rtc_comment_list)):
        question_data=get_problem(rtc_comment_list[i]['data'])
        print(question_data)
        if(question_data!=None):
            print(question_data)
            break
    if question_data!=None:
        qa_dict['Question']=question_data
    return qa_dict

def get_solution_from_comments(data_entry,qa_dict):
    rtc_comment_list=get_comments_list(data_entry)
    rtc_comment_list.sort(key=lambda item:item['timestamp'], reverse=True)
    print(rtc_comment_list)
    for i in range(0,len(rtc_comment_list)):
        solution_data=get_solution(rtc_comment_list[i]['data'])
        if(solution_data!=None):
            print(solution_data)
            break
    if solution_data!=None:
        qa_dict['Solution']=solution_data
    return qa_dict

def extract_question_and_answer(json_data):
    csv_data_list=[]
    for i in range(0,len(json_data['tickets'])):
        qa_dict={}
        print(json_data['tickets'][i])
        if('description' in json_data['tickets'][i]):
            question_data,solution_data=get_question_and_answer_from_description(json_data['tickets'][i])
        if question_data !=None and solution_data!=None:
            qa_dict['Question']=question_data
            qa_dict['Solution']=solution_data
            qa_dict=restructure_qa_dict(qa_dict,json_data['tickets'][i])
            csv_data_list.append(qa_dict)
            qa_dict={}

        elif question_data !=None and solution_data==None:
            qa_dict['Question']=question_data
            if('comments' in json_data['tickets'][i]):
                qa_dict=get_solution_from_comments(json_data['tickets'][i],qa_dict)
            qa_dict=restructure_qa_dict(qa_dict,json_data['tickets'][i])
            csv_data_list.append(qa_dict)
            qa_dict={}
        elif question_data==None and solution_data!=None:
            qa_dict['Solution']=solution_data
            if('comments' in json_data['tickets'][i]):
                qa_dict=get_problem_from_comments(json_data['tickets'][i],qa_dict)
            qa_dict=restructure_qa_dict(qa_dict,json_data['tickets'][i])
            csv_data_list.append(qa_dict)
            qa_dict={}

        elif question_data==None and solution_data==None:
            if('comments' in json_data['tickets'][i]):
                qa_dict=get_problem_from_comments(json_data['tickets'][i],qa_dict)
                qa_dict=get_solution_from_comments(json_data['tickets'][i],qa_dict)
            qa_dict=restructure_qa_dict(qa_dict,json_data['tickets'][i])
            # rtc_comment_list=get_comments_list(json_data['tickets'][i])
            # qa_dict=get_qadict_from_comments(rtc_comment_list)

            csv_data_list.append(qa_dict)
            qa_dict={}
    print(csv_data_list)
    write_csv_list_file(csv_data_list)
        # elif question_data !=None and solution_data==None:
        #     qa_dict['Question']=question_data
        # elif question_data==None and solution_data!=None:
        #     qa_dict['Solution']=solution_data

# def write_csv_list_file(csv_list):
#     print(str(csv_list))
# # Get a list of all keys in the dictionaries
#     all_keys = []
#     for d in csv_list:
#         all_keys += list(d.keys())
#     all_keys = list(set(all_keys))
#     print(all_keys)
#     # Write the CSV file
#     with open('output.csv', 'w', newline='',encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=all_keys)
#         writer.writeheader()
#         for d in csv_list:
#             writer.writerow(d)

def write_csv_list_file(csv_data_list):

    fieldnames = ['Question', 'Response']
    with open('output.csv', 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data_list:
            # Create a new dictionary with the desired field names
            row_new = {fieldnames[0]: row['Question'], fieldnames[1]: row['Solution']}
            writer.writerow(row_new)

if __name__ == "__main__":
    #defining global variables
    # file_path='./rtc-ticket-data.json'
    file_path='./rtc-ticket-data.json'
    json_data=get_json_file_data(file_path)

    extract_question_and_answer(json_data)
