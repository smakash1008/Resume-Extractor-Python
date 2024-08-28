# Importing the Required Libraries:

import re
import pdfminer
from pdfminer.high_level import extract_text
import docx2txt
import os
import sys
import json

# Extracting the File Extension:

def file_extension_extract(file_name):
    file_name_split = file_name.split(".",1)
    if len(file_name_split) == 2:
        return file_name_split[1]
    else:
        return None

file_name = input("Enter the File Name: ")
file_extension = file_extension_extract(file_name)
print(file_extension)

# Extracting the text from the Pdf or Word Document:

def file_text_extraction(file_extension):
    if (file_extension == "pdf"):
        text = extract_text(file_name)
        return text
    elif (file_extension == "docx"):
        text = docx2txt.process(file_name)
        return text
    else:
        return None
    
text_extracted = file_text_extraction(file_extension)
print(text_extracted)

# Extracting the Required Fields from the Extracted Text:

final_data = {}
print(final_data)
Personal_Information = {}
print(Personal_Information)

def start_section_extraction(text_extracted):
   start_pattern = r'^(.*?)(Professional Summary|Profile Summary|$)'
   match = re.search(start_pattern,text_extracted,re.DOTALL)
   if match:
      start_section = match.group().strip()
      return start_section
   else:
      return "Not Found..."
   
start_text = start_section_extraction(text_extracted)
print(start_text)
education_text = start_text.replace("\n"," ")
print(start_text)

# Extracting the Name:

def name_extraction(start_text):
  name_pattern = [r'\b[A-Z][a-zA-Z]*[\s]?[A-Z][a-zA-Z]*[\s]?[A-Z][a-zA-Z]*[\s]?\b',r'\b[A-Z][a-zA-Z]*[\s]?[A-Z][a-zA-Z]*?\b',r'\b[A-Z][a-zA-Z]*\b']
  combine_name_pattern = '|'.join(name_pattern)
  name_match = re.search(combine_name_pattern,start_text,re.DOTALL)
  if name_match:
     name_grp = name_match.group()
     return name_grp
  else:
     return None

name = name_extraction(text_extracted)
if '\n' in name:
   name = name.replace("\n"," ")
   print(name)
else:
   print(name)
Personal_Information['Name'] = name
print(Personal_Information)

# Extracting the Gender:

def personal_section_extraction(text_extracted):
   personal_pattern = r'(Personal Profile|Personal Details)(.*?)(Summary|$)'
   match = re.search(personal_pattern,text_extracted,re.DOTALL)
   if match:
      personal_section = match.group().strip()
      return personal_section
   else:
      return "Not Found..."
   
personal_text = personal_section_extraction(text_extracted)
print(personal_text)
personal_text = personal_text.replace("\n"," ")
print(personal_text)

genders_list = ["Male","Female","Transgender","Gender Neutral","Non-Binary","Agender","Pangender","Genderqueer","Two-Spirit","Non Binary","Two Spirit","Third Gender"]

def gender_extraction(personal_text,genders_list):
  for genders in genders_list:
    gender_pattern = r"\b{}\b".format(re.escape(genders))
    gender_match = re.search(gender_pattern,personal_text,re.IGNORECASE)
    if gender_match:
      gender_extracted = gender_match.group()
      return gender_extracted
    else:
       return None

gender = gender_extraction(personal_text,genders_list)
print(gender)
Personal_Information['Gender'] = gender
print(Personal_Information)

# Extracting the Nationality:

def nationality_extraction(personal_text):
    nationality_pattern = r'\b(?:Indian|Afghan|American|Armenian|Australian|Austrian|British|Bangladeshi|Canadian|Dutch|Danish|Japanese|Malaysian|Pakistani|Qatari|Russian|Taiwanese|Thai|Chinese)\b'
    nationality_match = re.search(nationality_pattern,personal_text,re.IGNORECASE)
    print(nationality_match)
    if nationality_match:
      nationality_extracted = nationality_match.group()
      return nationality_extracted
    else:
       return None

nationality = nationality_extraction(personal_text)
print(nationality)
Personal_Information['Nationality'] = nationality
print(Personal_Information)

# Extracting the Marital Status:

def marital_status_extraction(personal_text):
    marital_pattern = r'\b(?:Single|Married|Widowed|Divorced|Separated|Unmarried)\b'
    marital_match = re.search(marital_pattern,personal_text,re.IGNORECASE)
    if marital_match:
      marital_extracted = marital_match.group()
      return marital_extracted
    else:
       return None

marital_status = marital_status_extraction(personal_text)
print(marital_status)
Personal_Information['Marital_Status'] = marital_status
print(Personal_Information)

# Extracting the Languages Known:

languages = ['English','Tamil','Hindi','Kannada','Telugu','Malayalam','Marati','Bengali','Russian','Spanish','French','Mandarin','Persian','German','Japanese','Malay','Arabic','Marathi','Italian','Turkish','Portuguese','Chinese','Oriya']

def languages_extraction(text_extracted,languages):
    found_language = []
    for language in languages:
        language_pattern = r'\b{}\b'.format(re.escape(language))
        language_match = re.search(language_pattern,text_extracted,re.IGNORECASE)
        if language_match:
            language_grp = language_match.group()
            found_language.append(language_grp)
    return found_language

languages = languages_extraction(text_extracted,languages)
print(languages)
Personal_Information['Languages_Known'] = languages
print(Personal_Information)

# Extracting the Date Of Birth:

def Date_of_Birth_Extraction(personal_text):
  dob_pattern = r'\b\d{1,2}(?:st|nd|th|rd|ST|ND|RD|TH)?[-./\s]?[A-Za-z]+[-./\s]?\d{2,4}\b'
  dob_match = re.search(dob_pattern,personal_text)
  if dob_match:
     dob_grp = dob_match.group()
     return dob_grp
  else:
     return None

dob = Date_of_Birth_Extraction(personal_text)
print(dob)
Personal_Information['Date_Of_Birth'] = dob
print(Personal_Information)

final_data['Personal_Information'] = Personal_Information
print(final_data)

# Extracting the Email-Address:

Contact_Information = {}

def email_address_extraction(text_extracted):
  combine_text = text_extracted.replace("\n"," ")
  email_pattern = r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z.-]+(?:\s|\n)?[a-zA-Z.-]*\.[a-zA-Z]{2,})\b'
  email_match = re.search(email_pattern,combine_text)
  if email_match:
    email_grp = email_match.group()
    return email_grp
  else:
     return None
    
email_address = email_address_extraction(text_extracted)
if " " in email_address:
   email_address = email_address.replace(" ","")
   print(email_address)
else:
   print(email_address)
Contact_Information['Email_Address'] = email_address
print(Contact_Information)

# Extracting the Phone Number:

def phone_num_extraction(text_extracted):
    phone_num_extract = [r"\(?\+\d{1,3}\)?[-.\s]?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}", r"\d{10}", r"\d{5} \d{5}", r"\+\d{1,3} \d{5} \d{5}", r"\(?\+\d{1,3}\)? \d{5} \d{5}", r"\(?\+\d{1,3}\)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{4}", r"\d{3} \d{4}", r"\d{7}", r"\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{4}", r"\+\d{1,3}[-.\s]?\d{7}"]
    combine_pattern = '|'.join(phone_num_extract)
    phone = re.search(combine_pattern,text_extracted)
    if phone:
        phone_nums = phone.group()
        return phone_nums
    else:
       return None
    
phone_number = phone_num_extraction(text_extracted)
print(phone_number)
Contact_Information['Phone_Number'] = phone_number
print(Contact_Information)

final_data['Contact_Information'] = Contact_Information
print(final_data)

# Extracting the Technical Skills:

def skills_section_extraction(text_extracted):
   skills_pattern = r'(Professional Summary|Profile Summary|Summary)(.*?)($)'
   match = re.search(skills_pattern,text_extracted,re.DOTALL)
   if match:
      skills_section = match.group().strip()
      return skills_section
   else:
      return "Not Found..."
   
skills_text = skills_section_extraction(text_extracted)
print(skills_text)
skills_text = skills_text.replace("\n"," ")
print(skills_text)

Technical_Information = {}

skills = ["Hadoop","Java","SQL","HTML","CSS","Javascript","C","C++","Sqoop","Spark","Hive","Oozie","Kafka","Nifi","HDFS","Yarn","Mapreduce","C#", "Html5", "Xml","Pyspark","Scala Spark","Python","Scala","Mysql","Wordpress","Cms","Delta","Siemens","Embedded","Fundamental of C++","Flexray","Linux","Windows","Mac","MacOS","Oracle","PostgreSQL","Aws","Gcp","MongoDB","React","ReactJS","Mocha","API","Azure","Jenkins","Git","Github","Docker","NHibernate","ExpressJS","Express JS","NestJS","Nest JS","React JS","R","PHP","NodeJS","Node JS","Node.js","AngularJS","Angular JS","Pycharm","Pycharm Ide","Microsoft VS Code","VS Code","Altova Map Force","Asp.Net Core","Asp.Net MVC","Elasticsearch","Elastic Search","Kibana","Sap","Kubernetes","Objective-C","Objective C","Asp.Net","Ruby","Golang","Django","Laravel","Microsoft Windows","TensorFlow","Tensor Flow","AML","scikit-learn","Cisco CCNA","Cisco","Matlab","AutoCAD","Google Cloud ML Engine","data mining","data modeling","statistical analysis","Cam","Verilog","Simulink","Pspice","ETAP","Multisim","Amazon Web Services","Bash","Prometheus","BLOB Storage","Azure SQL","Oracle VM","Azure VM","Grade","VMware","Agile","Asana","Salesforce","CRM Systems","Hubspot","CSS3","iQuery","Adobe","RDBMS","Adobe Creative Suite","Office 365","Microsoft Office","Xhtml","Bootstrap","Bootstrap html","MS Excel","MS Word","MS Access","MS Powerpoint","Snap 10","Hootsuite Certified",".Net","Ajax","Perl","J2P","J2EE","ColdFusion","Cold Fusion","Typescript","Rust","Swift","Microsoft .Net","Google colab","colab","Jupyter","Jupyter Notebook","HortonWorks","Apache","Cloudera","Figma","Sketch","Adobe XD","Invision Studio","AdobeXD","Adobe","Photoshop","Zeplin","Skeleton","Foundation","Premiere Pro","After Effects","MSSQL","RabbitMQ","AWS Lambda","MVC","jenkin","JSON","web services","express","php","DynamoDB","MS SQL Server","Chai","Angular","Material UI","Node","SDLC","Agile","AWS Cloud","S3","EC2","Load Balancer","API Gateway","SNS","SQS","Cloud Font","Cloud Watch","lambda","Jquery","MS SQL Server","Amazon S3","Amazon Web Services","Rest API","API","MSSQL Server","Oracle 8i","9i","10g","11g","12c","RAC","Postgre","Oracle 12c","18c","19c","Autonomous Database","Kubernetes Cluster","Postgre Database","AWS RDS","ATPSQLT","AHF","SQLHC","COE","RMAN","AWR","SecureCRT","DataPump","OEM","ADDM","Exachk","JIRA","Service Now","Maven","IntelliJ","Oracle SQL","TestNG","Tosca","Appium","Selenium Web Driver","Waterfall","Perfecto","Browser Stack","TestRail","Clevertap","Klaviyo","Google Analytics","Firebase","Proxyman","Clear Quest","HP-ALM"]

def skills_extraction(skills_text,skills):
    found_skills = []
    for skill in skills:
        skill_pattern = r"\b{}\b".format(re.escape(skill))
        skill_match = re.search(skill_pattern,skills_text,re.IGNORECASE)
        if skill_match:
            grp_skill = skill_match.group()
            found_skills.append(grp_skill)
    return found_skills

Extracted_skills = skills_extraction(skills_text,skills)
print(Extracted_skills)
Technical_Information['Skills'] = Extracted_skills
print(Technical_Information)

# Extracting the Work Domain:

work_domains = ["Insurance","Health","Media","Telecom","Healthcare","Travel","Finance","Advertising","Medical","Banking","Sales","Railways","Airways","Gaming","eCommerce","E commerce","e commerce","Big Data","Application Development","Software Development","Data Science","Artificial Intelligence","Testing","Defense","Web Development","Scientific Development","Business Development","Embedded Systems","Devops","Dev ops","Dev-ops","Defense Systems","E-commerce","Advertisement","Telecommunication","Telecom","Mainframes","Main Frames","Main-frames","Tourism and Travel","App Development","IoT","Airlines","Hospitality","Blockchain","Cybersecurity","Cyber Security","Block Chain"]

def work_domain_extraction(text_extracted,work_domains):
  found_work_domain = []
  for domain in work_domains:
    work_domain_pattern = r'\b{}\b'.format(re.escape(domain))
    work_domain_match = re.search(work_domain_pattern,text_extracted,re.IGNORECASE)
    if work_domain_match:
      work_domain_grp = work_domain_match.group()
      found_work_domain.append(work_domain_grp)
  return found_work_domain

work_domain = work_domain_extraction(text_extracted,work_domains)
print(work_domain)
Technical_Information['Work_Domain'] = work_domain
print(Technical_Information)

final_data['Technical_Information'] = Technical_Information
print(final_data)

# Extracting the Education Course Details:

def education_section_extract(text_extracted):
   education_start_pattern = r'(Education|Educational Qualification|Graduation|Academic|Academic Details)(.*?)(Career Graph|Work Experience|Personal Details|Experience|$)'
   match = re.search(education_start_pattern,text_extracted,re.DOTALL)
   if match:
      education_section = match.group().strip()
      return education_section
   else:
      return "Not Found..."
   
education_text = education_section_extract(text_extracted)
print(education_text)
education_text = education_text.replace("\n"," ")
print(education_text)

Education_Information = {}

def courses_extraction(education_text):

    course_pattern = [r'\b(?:Master|Bachelors|Masters|B\.A\.|B\.Sc\.|Bachelor|M\.A\.|M\.Sc\.|Ph\.D\.|Doctorate|Diploma|Associate|B\.Tech\.|B\.E\.|B\.E|B\.Tech|B\.Sc|B\.A|M\.A|M\.Sc|BE|BTech|BSc|Bsc|MSc|Msc|Btech|ME|MTech|Mtech|BA|MA|MBA|M\.B\.A\.|Mba|MBBS|M\.B\.B\.S\.|M\.B\.A|M\.B\.B\.S|MD|M\.D\.|M\.D|LLB|L\.L\.B\.|L\.L\.B|Llb|LLb|B\.Com|M\.Com|B\.Com\.|M\.Com\.|BBA|B\.B\.A\.|B\.B\.A|BBa|Bba|HSC|SSLC|Hsc|Sslc|Higher Secondary|Secondary|B\.tech\.|B\.tech|M\.Tech\.|M\.Tech|M\.tech\.|M\.tech|PG Diploma|10th|10TH|MCA|BCA)\s*(?:of\s*|in\s*)?.*?(?:Science|Arts|Engineering|Technology|Mathematics|Physics|Chemistry|Biology|Finance|Economics|History|Literature|Law|Philosophy|Sociology|Computer Science|IT|ECE|EEE|Mech|MECH|Civil|CSE|Mechatronics|AI|DS|Artificial Intelligence|Data Science|Artificial Intelligence and Data Science|Food Technology|CIVIL|Legislative Law|General|Commerce|Business Administration|Computer Application)\)?[\s]?(?:-\s*|in\s*)?.*?\(?(?:Information Technology|Computer Science & Engineering|Electronics & Communication Engineering)?\b\)?',r'\b(?:Master|Bachelors|Masters|B\.A\.|B\.Sc\.|Bachelor|M\.A\.|M\.Sc\.|Ph\.D\.|Doctorate|Diploma|Associate|B\.Tech\.|B\.E\.|B\.E|B\.Tech|B\.Sc|B\.A|M\.A|M\.Sc|BE|BTech|BSc|Bsc|MSc|Msc|Btech|ME|MTech|Mtech|BA|MA|MBA|M\.B\.A\.|Mba|MBBS|M\.B\.B\.S\.|M\.B\.A|M\.B\.B\.S|MD|M\.D\.|M\.D|LLB|L\.L\.B\.|L\.L\.B|Llb|LLb|B\.Com|M\.Com|B\.Com\.|M\.Com\.|BBA|B\.B\.A\.|B\.B\.A|BBa|Bba|HSC|SSLC|Hsc|Sslc|Higher Secondary|Secondary|B\.tech\.|B\.tech|M\.Tech\.|M\.Tech|M\.tech\.|M\.tech|PG Diploma|10th|10TH|MCA|BCA)\b',r'\(?\b(?:Master|Bachelors|Masters|B\.A\.|B\.Sc\.|Bachelor|M\.A\.|M\.Sc\.|Ph\.D\.|Doctorate|Diploma|Associate|B\.Tech\.|B\.E\.|B\.E|B\.Tech|B\.Sc|B\.A|M\.A|M\.Sc|BE|BTech|BSc|Bsc|MSc|Msc|Btech|ME|MTech|Mtech|BA|MA|MBA|M\.B\.A\.|Mba|MBBS|M\.B\.B\.S\.|M\.B\.A|M\.B\.B\.S|MD|M\.D\.|M\.D|LLB|L\.L\.B\.|L\.L\.B|Llb|LLb|B\.Com|M\.Com|B\.Com\.|M\.Com\.|BBA|B\.B\.A\.|B\.B\.A|BBa|Bba|HSC|SSLC|Hsc|Sslc|Higher Secondary|Secondary|B\.tech\.|B\.tech|M\.Tech\.|M\.Tech|M\.tech\.|M\.tech|PG Diploma|10th|10TH|BCA|MCA)\s*(?:of\s*|in\s*)?.*?\(?(?:Science|Arts|Engineering|Technology|Mathematics|Physics|Chemistry|Biology|Finance|Economics|History|Literature|Law|Philosophy|Sociology|Computer Science|IT|ECE|EEE|Mech|MECH|Civil|CSE|Mechatronics|AI|DS|Artificial Intelligence|Data Science|Artificial Intelligence and Data Science|Food Technology|CIVIL|Legislative Law|General|Commerce|Business Administration|Computer Application)\)?\b']
    combine_course_pattern = '|'.join(course_pattern)
    courses = re.findall(combine_course_pattern,education_text)
    return courses

course_details = courses_extraction(education_text)
course = list(dict.fromkeys(course_details))
print(course)
Education_Information['Course_Details'] = course
print(Education_Information)

# Extracting the Institution Details:

def institution_extraction(education_text):
  institution_pattern = [r'\b[A-Z][a-zA-Z]*\s(?:[A-Z][a-zA-Z]*\s)?(?:[A-Z][a-zA-Z]*\s)?(?:[A-Z][a-zA-Z]*\s)?(?:[A-Z][a-zA-Z]*\s)?(?:[a-z][a-zA-Z]*\s)?(?:University|College|Institute of Technology|Institute of Science and Technology|School|Institute|Academy|Center|Faculty|Polytechnic|Conservatory)\b',r'\b[A-Z][a-zA-Z]*\s(?:[a-z][a-zA-Z]*\s)?(?:[a-z][a-zA-Z]*\s)?(?:[a-z][a-zA-Z]*\s)?(?:college|University|College|Institute|School|Academy|Center|Faculty|Polytechnic|Conservatory)\s(?:[a-z][a-zA-Z]*\s)?(?:[a-z][a-zA-Z\,]*\s)',r'\b[A-Z][A-Z]*(?:U)\b']
  combine_institution_pattern = '|'.join(institution_pattern)
  institutions = re.findall(combine_institution_pattern,education_text)
  return institutions

education_institution = institution_extraction(education_text)
print(education_institution)
Education_Information['Education_Institution'] = education_institution
print(Education_Information)

# Extracting the Graduation Year:

def graduation_year_extraction(education_text):
   graduation_year_pattern = [r'\b(?:19|20)\d{2}\b',r'\b\d{4}[\s]?[\-][\s]?\d{4}\b']
   combine_graduation_year_pattern = "|".join(graduation_year_pattern)
   graduation_year_match = re.findall(combine_graduation_year_pattern,education_text)
   if graduation_year_match:
      return graduation_year_match
   else:
      return None

graduation_year = graduation_year_extraction(education_text)
print(graduation_year)
Education_Information['Graduation_Year'] = graduation_year
print(Education_Information)

# Extracting the CGPA:

def cgpa_extraction(education_text):
   cgpa_pattern = r'\b\d\.(?:\d*)?[\s]?(?:CGPA|GPA|Gpa|Cgpa)?\b'
   cgpa_match = re.search(cgpa_pattern,education_text,re.IGNORECASE)
   if cgpa_match:
      cgpa_extracted = cgpa_match.group()
      return cgpa_extracted
   else:
      return None

cgpa = cgpa_extraction(education_text)
print(cgpa)
Education_Information['CGPA'] = cgpa
print(Education_Information)

# Extracting the Degree and School Exams Percentage:

def education_percent(education_text):
  percent_pattern = [r'\d{1,2}[\.]?[\d{1}]?[\s]?[%]?[\s]?[-to]+[\s]?\d{1,2}[\.]?[\d{1}]?[\s]?[%]',r'\d{1,2}[\.]?[\d{1}]*[\s]?[%]']
  combine_percent_pattern = "|".join(percent_pattern)
  percent_match = re.findall(combine_percent_pattern,education_text)
  return percent_match

education_percentage = education_percent(education_text)
print(education_percentage)
Education_Information['Exams_Percentage'] = education_percentage
print(Education_Information)

final_data['Education_Information'] = Education_Information
print(final_data)

# Extracting the Company Names:

def work_section_extract(text_extracted):
   work_start_pattern = r'(Career Graph|Work Experience|PROFESSIONAL EXPERIENCE|Organization Experience|CGPA)(.*?)(Projects|PROJECTS|Project Handled|Awards|$)'
   match = re.search(work_start_pattern,text_extracted,re.DOTALL)
   if match:
      work_section = match.group().strip()
      return work_section
   else:
      return "Not Found..."
   
work_text = work_section_extract(text_extracted)
print(work_text)
work_text = work_text.replace("\n"," ")
print(work_text)

Work_Information = {}

def company_extract(work_text):
    company_pattern = [r'\b[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\s(?:Inc|Inc.|Ltd|Ltd.|Limited|Corporation|Corp.|Corp|Group|LLC|Companies|Tv|Co|TV|Co.|Incorporated|Consulting|Consultancy|Technologies)\b',r'\b[A-Z][a-zA-Z0-9]*\s(?:[a-z][a-z]*\s)*?(?:[A-Z][a-zA-Z]*\s)*?(?:Inc|Inc.|Ltd|Ltd.|Limited|Corporation|Corp.|Corp|Group|LLC|Companies|Tv|Co|TV|Co.|Incorporated|Consulting|Consultancy|Technologies)\b',r'\b[A-Z][a-zA-Z]*(?:ite|usa|zon|tum|iapp|dus|xus|tra|ia|amm|ron|yal|tic|eem|gal|ic|ncy|ency|AI|tez|ight|oft|kart|ato|que|sys|ho|tra|ma|gle|soft)\b',r'\b[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\s[a-z][a-z]*\s(?:[A-Z][a-zA-Z]*\s)*?(?:Inc|Inc.|Ltd|Ltd.|Limited|Corporation|Corp.|Corp|Group|LLC|Companies|Tv|Co|TV|Co.|Incorporated|Consulting|Consultancy|Technologies)\b',r'\b[A-Z][a-zA-Z]*\s[a-z][a-z]*\s[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*[\s]+[A-Z][a-zA-Z]*\s(?:Inc|Inc.|Ltd|Ltd.|Limited|Corporation|Corp.|Corp|Group|LLC|Companies|Tv|Co|TV|Co.|Incorporated|Consulting|Consultancy|Technologies)\b',r'\b[A-Z][a-zA-Z]*[\s]?(?:[A-Z][a-zA-Z]*)?(?:Inc|Inc.|Ltd|Ltd.|Limited|Corporation|Corp.|Corp|Group|LLC|Companies|Tv|Co|TV|Co.|Incorporated|Consulting|Consultancy|Technologies|AI|Apps|Tech|dra|gal|ic|ncy|ency|AI|tez|ight|oft|kart|ato|que|sys|ho|tra|ma|gle|soft)\b']
    combine_company_pattern = '|'.join(company_pattern)
    companies = re.findall(combine_company_pattern,work_text,re.DOTALL)
    return companies

company_name = company_extract(work_text)
print(company_name)
Work_Information['Company_Name'] = company_name
print(Work_Information)

# Extracting the Total Work Experience:
 
def total_work_experience_extraction(text_extracted):
  total_work_experience_pattern = [r'\b\d+[\+]?[-\s]?years?(\s+of)?\s+experience\b',r'\b\d+[\+]?[-\s]?years?\b',r'\b\d+\.\d+[\+]?[-\s]?years?(\s+of)?\s+experience\b']
  combine_total_exp_pattern = '|'.join(total_work_experience_pattern)
  total_experience_match = re.search(combine_total_exp_pattern,text_extracted)
  if total_experience_match:
    total_experience = total_experience_match.group()
    return total_experience
  else:
     return None

total_work_experience = total_work_experience_extraction(text_extracted)
print(total_work_experience)
Work_Information['Total_Work_Experirence'] = total_work_experience
print(Work_Information)

final_data['Work_Information'] = Work_Information
print(final_data)

# Project Section Extraction:

def project_section_extract(text_extracted):
   project_start_pattern = r'(Projects|PROJECTS|Project Handled)(.*?)(Personal Profile|Courses & Certifications|EDUCATION|Graduation|Academic Details|$)'
   match = re.search(project_start_pattern,text_extracted,re.DOTALL)
   if match:
      project_section = match.group().strip()
      return project_section
   else:
      return "Not Found..."
   
project_text = project_section_extract(text_extracted)
print(project_text)
project_text = project_text.replace("\n"," ")
print(project_text)

# Extracting the Project Title:

Project_Information = {}
'''
def project_title_extraction(project_text):
  project_title_pattern = [r'\b[A-Z][a-zA-Z]*\s(?:[A-Z][a-zA-Z]*\s)(?:[a-z][A-Za-z]*\s)(?:[A-Z][a-zA-Z]*)\b',r'\b[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\b', r'\b[A-Z][a-z][a-z]\b',r'\b[a-z][a-z][a-z][a-z][a-z][a-z][a-z]\b',r'\b[a-z][a-zA-Z]*\s[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\b',r'\b[A-Z][a-zA-Z]*\s[a-z][a-zA-Z]*\s[a-z][a-zA-Z]*\b',r'\b[A-Z][A-Z\'][a-z]\s[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*\b']
  combine_title_pattern = '|'.join(project_title_pattern)
  project_title_match = re.findall(combine_title_pattern,project_text)
  if project_title_match:
     return project_title_match
  else:
     return None

project_title = project_title_extraction(project_text)
print(project_title)
Project_Information['Project_Title'] = project_title
print(Project_Information)'''

# Extracting the Project Roles:

project_roles = ["Developer","Senior Software Developer","Software Developer","DBA","Cloud Operation Analyst","Senior Cloud DB Migration Engineer","Junior Cloud DB Migration Engineer","Senior Cloud Database Consultant","Technical Lead","Database Architect","Software Engineer","Oracle DBA","Lead DBA","Sr. DBA","DMA","Development Manager","Database Administrator","Health Business Analyst","Consultant","Oracle Golden Gate DBA","Oracle Apps DBA","Senior Database Administrator","Database Architect","Technical Consultant","Associate Consultant","Principal Consultant","Test Engineer","Test Automation Team Lead"]

def project_role_extraction(project_text,project_roles):
  found_project_roles = []
  for roles in project_roles:
    project_role_pattern = r'\b{}\b'.format(re.escape(roles))
    project_role_match = re.search(project_role_pattern,project_text,re.IGNORECASE)
    if project_role_match:
      project_role_grp = project_role_match.group()
      found_project_roles.append(project_role_grp)
  return found_project_roles

project_role = project_role_extraction(project_text,project_roles)
print(project_role)
Project_Information['Project_Roles'] = project_role
print(Project_Information)

# Extracting the Project Domain:

project_domains = ["Tourism","Travel","Airways","Railways","Banking","Retail","E-Commerce","E Commerce","Insurance","Media","Telecom","Telecommunication","Transportation","Health","Hospitality","Healthcare","Health Care","Gaming","Medical","Sales","Advertising","Finance","Airlines"]

def project_domain_extraction(project_text,project_domains):
  found_project_domain = []
  for domains in project_domains:
    project_domain_pattern = r'\b{}\b'.format(re.escape(domains))
    project_domain_match = re.search(project_domain_pattern,project_text,re.IGNORECASE)
    if project_domain_match:
      project_domain_grp = project_domain_match.group()
      found_project_domain.append(project_domain_grp)
  return found_project_domain

project_domain = project_domain_extraction(project_text,project_domains)
print(project_domain)
Project_Information['Project_Domain'] = project_domain
print(Project_Information)

# Extracting the Project Technologies:

project_technologies = ["Hadoop","Java","SQL","HTML","CSS","Javascript","C","C++","Sqoop","Spark","Hive","Oozie","Kafka","Nifi","HDFS","Yarn","Mapreduce","C#", "Html5", "Xml","Pyspark","Scala Spark","Python","Scala","Mysql","Wordpress","Cms","Delta","Siemens","Embedded","Fundamental of C++","Flexray","Linux","Windows","Mac","MacOS","Oracle","PostgreSQL","Aws","Gcp","MongoDB","React","ReactJS","Mocha","API","Azure","Jenkins","Git","Github","Docker","NHibernate","ExpressJS","Express JS","NestJS","Nest JS","React JS","R","PHP","NodeJS","Node JS","Node.js","AngularJS","Angular JS","Pycharm","Pycharm Ide","Microsoft VS Code","VS Code","Altova Map Force","Asp.Net Core","Asp.Net MVC","Elasticsearch","Elastic Search","Kibana","Sap","Kubernetes","Objective-C","Objective C","Asp.Net","Ruby","Golang","Django","Laravel","Microsoft Windows","TensorFlow","Tensor Flow","AML","scikit-learn","Cisco CCNA","Cisco","Matlab","AutoCAD","Google Cloud ML Engine","data mining","data modeling","statistical analysis","Cam","Verilog","Simulink","Pspice","ETAP","Multisim","Amazon Web Services","Bash","Prometheus","BLOB Storage","Azure SQL","Oracle VM","Azure VM","Grade","VMware","Agile","Asana","Salesforce","CRM Systems","Hubspot","CSS3","iQuery","Adobe","RDBMS","Adobe Creative Suite","Office 365","Microsoft Office","Xhtml","Bootstrap","Bootstrap html","MS Excel","MS Word","MS Access","MS Powerpoint","Snap 10","Hootsuite Certified",".Net","Ajax","Perl","J2P","J2EE","ColdFusion","Cold Fusion","Typescript","Rust","Swift","Microsoft .Net","Google colab","colab","Jupyter","Jupyter Notebook","HortonWorks","Apache","Cloudera","Figma","Sketch","Adobe XD","Invision Studio","AdobeXD","Adobe","Photoshop","Zeplin","Skeleton","Foundation","Premiere Pro","After Effects","MSSQL","RabbitMQ","AWS Lambda","MVC","jenkin","JSON","express","php","DynamoDB","MS SQL Server","Chai","Angular","Material UI","Node","SDLC","Agile","AWS Cloud","S3","EC2","Load Balancer","API Gateway","SNS","SQS","Cloud Font","Cloud Watch","lambda","Jquery","MS SQL Server","Amazon S3","Amazon Web Services","Rest API","API","MSSQL Server","Oracle 8i","9i","10g","11g","12c","RAC","Postgre","Oracle 12c","18c","19c","Autonomous Database","Kubernetes Cluster","Postgre Database","AWS RDS","ATPSQLT","AHF","SQLHC","COE","RMAN","AWR","SecureCRT","DataPump","OEM","ADDM","Exachk","JIRA","Service Now","Maven","IntelliJ","Oracle SQL","TestNG","Tosca","Appium","Selenium Web Driver","Waterfall","Perfecto","Browser Stack","TestRail","Clevertap","Klaviyo","Google Analytics","Firebase","Proxyman","Clear Quest","HP-ALM"]

def project_technologies_extraction(project_text,project_technologies):
  found_project_technologies = []
  for technologies in project_technologies:
    project_technology_pattern = r'\b{}\b'.format(re.escape(technologies))
    project_technology_match = re.search(project_technology_pattern,project_text,re.IGNORECASE)
    if project_technology_match:
      project_technology_grp = project_technology_match.group()
      found_project_technologies.append(project_technology_grp)
  return found_project_technologies

project_technologies = project_technologies_extraction(project_text,project_technologies)
print(project_technologies)
Project_Information['Project_Technologies'] = project_technologies
print(Project_Information)

# Extracting the Project Duration:

def project_duration_extraction(project_text):
  project_duration_pattern = [r'\b\d+[\s]?(?:Days|days)\b',r'\b(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)[\’]?[\s]?\d{2,4}[\s]?[-to]+[\s]?(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)[\’]?[\s]?\d{2,4}\b',r'\b(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)[\’]?[\s]?\d{2,4}[\s]?[-to]+[\s]?(?:Present|present|till date|Till Date|Current|current|till|Till Now|Till now|till now|Till date)\b',r'\b\d+[\s]?(?:Years|years|months|Months|Year|year|Month|month)[,]?[\s]+\d+[\s]?(?:Months|months|Days|days|month|Month|day|Day)\b',r'\b(?:since|Since)[\s]?(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)[\’]?[\s]?\d{2,4}']
  combine_project_duration = '|'.join(project_duration_pattern)
  project_duration_match = re.findall(combine_project_duration,project_text)
  if project_duration_match:
     return project_duration_match
  else:
     return None

project_duration = project_duration_extraction(project_text)
print(project_duration)
Project_Information['Project_Duration'] = project_duration
print(Project_Information)

final_data['Project_Information'] = Project_Information
print(final_data)