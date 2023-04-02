from pathlib import Path
import os 
from dotenv import load_dotenv
import openai

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

openai.api_key = os.environ['OPENAI_API_KEY']

def get_questions(job = "Data scientist", experience = '1'):
    prompt_input = '''
give me your complete name 
m ami
Recall: what is the job that you postulate for ?
data scientist
Recall: what is the average year of experience for this field (not including studies)
2

AI: 
You are given a dataset on cancer detection. You have built a classification model and achieved an accuracy of 96 percent. Why shouldn't you be happy with your model performance? What can you do about it?

AI:
answer (2) : Cancer detection results in imbalanced data. In an imbalanced dataset, accuracy should not be based as a measure of performance. It is important to focus on the remaining four percent, which represents the patients who were wrongly diagnosed. Early diagnosis is crucial when it comes to cancer detection, and can greatly improve a patient's prognosis.
Hence, to evaluate model performance, we should use Sensitivity (True Positive Rate), Specificity (True Negative Rate), F measure to determine the class wise performance of the classifier.

You: imagine you are data scientist experimented ask me a detailled technical problem on specific life situation to see if i am a good candidate, this question has to require deep knowledge on the job with 3 year of experience
AI: 
You are a data scientist working with a healthcare organization. They have a large dataset that contains medical records of patients who have been diagnosed with a particular type of cancer. Your goal is to develop a model that can accurately predict the likelihood of a patient developing the cancer in the future. How would you approach this problem? What techniques would you use to build the model and evaluate its performance?

You: imagine you are data scientist experimented ask me a detailled technical problem on specific life situation to see if i am a good candidate, this question has to require deep knowledge on the job with " year of experience
AI: 
You are a data scientist with 3 years of experience. You have been tasked with building a predictive model to predict the risk of a particular type of cancer in a population. Your dataset includes demographic information, medical history, and lifestyle factors. How would you approach this problem? What techniques would you use to build the model and evaluate its performance?


You: imagine you are Driver experimented ask me a detailled technical problem on specific life situation to see if i am a good candidate, this question has to require deep knowledge on the job with 1 year of experience
AI: You are a delivery driver for a company that specializes in transporting hazardous materials. One day, while on your route, you are notified of a road closure due to a chemical spill. How would you handle this situation to ensure the safe and timely delivery of the hazardous materials? How would you communicate this situation to the company and to other drivers on the road?
'''

    # define list of prompts
    conv = f"imagine you are {job} experimented ask me a detailled technical problem on specific life situation to see if i am a good candidate, this question has to require deep knowledge on the job with {experience} year of experience\n"
    prompt_input += f"\nYou: {conv}\nAI: "
    prompts = [get_chatgpt_response(prompt_input)]

    for i in range(1):
        prompt_input += "\nYou: give me a new question\nAI: "
        prompts.append(get_chatgpt_response(prompt_input))
        prompt_input += get_chatgpt_response(prompt_input)

    return prompts

def get_correction(question, user_answer):
    prompt_compare = '''
You: imagine you are data scientist experimented ask me a detailled technical problem on specific life situation to see if i am a good candidate, this question has to require deep knowledge on the job with 4 year of experience

AI:
You are a data scientist with 4 years of experience. You have been tasked with building a predictive model to predict the risk of a particular type of cancer in a population. Your dataset includes demographic information, medical history, lifestyle factors, and genomic data. How would you approach this problem? What techniques would you use to build the model and evaluate its performance?
You: compare answer (1) : i use machine learning 
 answer (2) : 

To approach this problem, I would first explore the data to understand the characteristics of the population and to identify any correlations between the different variables. I would then use a variety of techniques to build the predictive model, such as logistic regression, decision trees, and random forests. I would use cross-validation to evaluate the performance of the model, as well as other metrics such as precision and recall. Additionally, I would use feature selection techniques to identify the most important features in the model. Finally, I would use the model to make predictions on new data and compare the results to the ground truth. by giving a grade to answer (1) and explain what is missing or what is wrong compared to answer (2) 

your answer is graded as 9/100. Answer only mentions using machine learning techniques to build the predictive model, but does not mention any of the other steps involved in the process such as exploring the data, evaluating the model performance, or making predictions. Additionally, you should provide more details about the techniques that could be used to build the model as well as the metrics that could be used to evaluate its performance.
AI: 
You are a software engineer with 1 year of experience. You have been tasked with building a web-based application that allows users to search for medical information related to a particular type of cancer. How would you approach this problem? What technologies would you use to build the application and ensure that it is secure and reliable?
You: compare answer (1) : i will use javascript 
 answer (2) : 
I would approach this problem by first doing research to better understand the needs of the users and the type of medical information that needs to be searched. Next, I would determine the requirements for the application and identify the technologies that are best suited for the task. I would then design the application architecture and create the user interface.

To build the application, I would use a combination of technologies such as HTML, CSS, JavaScript, and a server-side language such as PHP or Node.js. I would also use a database such as MySQL or MongoDB to store the medical information. To ensure security and reliability, I would use encryption technologies such as SSL, TLS, and HTTPS. Additionally, I would use authentication and authorization protocols such as OAuth and SAML. Finally, I would use a version control system such as Git to manage the codebase. by giving a grade to answer (1) and explain what is missing or what is wrong compared to answer (2) 

Your answer is graded as 2/10. Answer only mentions using JavaScript to build the application, but does not mention any of the other steps involved in the process such as researching user needs, determining requirements, designing the application architecture, creating the user interface, or using encryption technologies. Additionally, you should provide more details about the technologies that could be used to build the application and ensure security and reliability.
You: imagine you are data engineer experimented ask me a detailled technical problem on specific life situation to see if i am a good candidate, this question has to require deep knowledge on the job with 1 year of experience

AI: 
You are a data engineer with 1 year of experience. You have been tasked with developing a data pipeline that can ingest data from multiple sources, clean and transform it, and store it in a data warehouse. How would you approach this problem? What techniques would you use to build the pipeline and evaluate its performance?
You: compare answer (1) : To approach this problem, I would first analyze the data sources to understand the data format, structure, size, and frequency of the data. Based on this analysis, I would decide on the appropriate data storage solution that can handle the volume and velocity of the data, such as a data lake, data warehouse, or a NoSQL database.  Next, I would design the data pipeline architecture, taking into account the data sources, storage solution, and any other components that need to be included, such as data quality checks, data transformation, and data validation. I would also consider the scalability of the pipeline, as the data sources may grow over time.  To ingest the data, I would use technologies such as Apache Kafka, Kinesis or RabbitMQ for real-time data streaming, and Apache Nifi or Apache Airflow to manage the data flow and data transformations.  For data processing, I would use technologies such as Apache Spark or Apache Flink, which are highly scalable and can perform operations such as filtering, aggregation, and transformation in parallel. I would also use Apache Hive or Presto for SQL-like querying and data analysis.  To ensure data accuracy and up-to-date, I would use techniques such as data validation, data quality checks, and data deduplication to detect and correct any errors in the data. I would also use data partitioning and bucketing to improve the performance of the pipeline.  I would also use a data governance strategy to ensure data lineage, data security and compliance.  To monitor the pipeline, I would use monitoring tools such as Prometheus and Grafana, to track the pipeline performance, and identify and troubleshoot any issues.  Finally, I would use data storage technologies such as Apache Parquet, Apache Avro or Apache ORC to store the data in a columnar format for faster querying and data analysis.  Overall, this approach would provide a comprehensive solution to the problem, by covering all the key steps involved in the process, and using specific technologies and techniques to create the pipeline, ensure data accuracy and up-to-date, and monitor the performance of the pipeline. 
 answer (2) : 
To approach this problem, I would first identify the data sources and their formats. Then, I would create a data model that can accommodate the data from all sources, taking into account any data transformations that need to be applied. I would use ETL (Extract, Transform, Load) techniques to build the pipeline and ensure that the data is properly ingested, cleaned, and transformed. I would also use data profiling to evaluate the performance of the pipeline, to ensure that the data is accurate and complete. Finally, I would use a data warehouse to store the transformed data. by giving a grade to answer (1) and explain what is missing or what is wrong compared to answer (2) 

Your answer is graded as 9/10. Answer mentions all the steps involved in the process, including analyzing the data sources, designing the pipeline architecture, using technologies for data ingestion, processing, and storage, using data governance, and monitoring the pipeline. Additionally, you provide specific details about the technologies and techniques that could be used to build the pipeline, ensure data accuracy and up-to-date, and monitor performance. However, you should also mention data profiling as a technique to evaluate the performance of the pipeline.

AI: 
You are a data scientist with 5 years of experience. You have been tasked with creating a predictive model to predict the likelihood of a particular medical condition in a population. Your dataset includes demographic information, medical history, and lifestyle factors. How would you approach this problem? What techniques would you use to build the model and evaluate its performance? What strategies would you employ to ensure the model is accurate and reliable?
You: compare answer (1) :  I would pre-process the data as necessary, such as normalizing numerical variables or encoding categorical variables.  Then, I would split the data into training and testing sets to evaluate the performance of the model.  For building the model, I would try different techniques such as Linear regression, Random forest,  depending on the characteristics of the data.  To evaluate the performance of the model, I would use metrics such as mean absolute error,. I would also look at the R-squared value to evaluate the goodness of fit of the model. 
 answer (2) : 
To approach this problem, I would first conduct exploratory data analysis (EDA) to gain an understanding of the data. I would look for patterns, trends, and correlations between the different variables. I would also examine the distribution of each variable to identify any outliers or anomalies.

Once I understand the data, I would then build the predictive model. I would use supervised machine learning techniques such as logistic regression, decision trees, and random forests to create the model. I would use cross-validation to evaluate the performance of the model and tune the hyperparameters to optimize the model.

To ensure the model is accurate and reliable, I would use a variety of strategies. I would use data augmentation techniques such as oversampling and undersampling to address any class imbalance. I would also use regularization techniques such as L1 and L2 regularization to avoid overfitting. Additionally, I would use feature selection methods such as recursive feature elimination to select the most relevant features for the model. Finally, I would use a variety of metrics such as accuracy, precision, recall, and F1 score to evaluate the performance of the model. by giving a grade to answer (1) and explain what is missing or what is wrong compared to answer (2) 

Your answer is graded as 7/10. Answer mentions the techniques that could be used to build the model and evaluate its performance, but does not mention any of the other steps involved in the process such as conducting exploratory data analysis, using data augmentation techniques, using regularization techniques, using feature selection methods, or using various metrics to evaluate the model. Additionally, you should provide more details about the techniques that could be used to build the model and ensure accuracy and reliability.

'''

    # get correct answer and prompt for ChatGPT
    correct_answer = prompt_compare + f"To the question : '{question}', user answer: '{user_answer}', Grade user's answer around 10 and comment the grading "

    return get_chatgpt_response(correct_answer)

def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text

def create_keyword_questions(user_answer):
        prompt_key ='''
            You : Generate the 3 most relevant keyword for a technical interview in this sentence : 'I will preprocess dataset then use machine learning' 
            AI : ['Preprocessing', 'Data preprocessing', 'Machine learning']
        '''

        keywords = get_chatgpt_response(prompt_key + f"You : Generate the 3 most relevant keyword for a technical interview in this sentence : '{user_answer}' ")
        keywords = keywords.strip()
        keywords = keywords[4:]
        keywords = eval(keywords)

        questions = []
        
        for keyword in keywords:
            question = f"Create a technical with deep knowledge question on {keyword}"
            sub_quest = get_chatgpt_response(question)
            questions.append(sub_quest)

        return questions