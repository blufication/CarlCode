
#Meet Carl: your friend

#import necessary libraries
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
import xlrd
import ibm_db as DB2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages
# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only

# Keyword Matching
RUN_ORDER = ["pp1", "pp2", "ppr", "ppost", "capfinal", "release notification"]
CALENDAR_CHECK = ["January","February","March","April","May","June","July","August","September","October","November","December"]
SEGMENT_CHECK = ["mahp", "leo", "m&r", "nhp", "mhp", "pcp"]
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation

sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

# month check from the input


def monthcheck(userinput):
    for word in userinput.split():
        if word in CALENDAR_CHECK:
            return word

#What is the segment from the input


def segmentcheck(userinput):
    for word in userinput.split():
        if word.lower() in SEGMENT_CHECK:
            return word.lower()

#Preprocessing
lemmer = WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))



def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

#here we need to get the data from Excell sheet of current date
def getmonth(userinput):
    month = monthcheck(userinput)
    loc = ('C:/Users/lbaddela/Documents/MyJabberFiles/sshar233@corpimsvcs.com/calendar.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_name(month)
    print(sheet.cell_value(0, 0))
    for i in range(sheet.nrows):
       value = sheet.cell_value(i, 0)
    return value

#here we need to ge the data of FAQ's
def getFAQ():
    #for now hold
    return  "FAQS here funtion"

#here we need to get the data form the excell sheet of current data
def getToday():
    date = int(4)
    loc = ('C:/Users/lbaddela/Documents/MyJabberFiles/sshar233@corpimsvcs.com/calendar.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_name("March")
    value = sheet.cell_value(date - 1, 1)
    return value

#here we need to get data from the excell sheet
def processTomorrow():
    date = int(4)
    loc = ('C:/Users/lbaddela/Documents/MyJabberFiles/sshar233@corpimsvcs.com/calendar.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_name("March")
    value = sheet.cell_value(date , 1)
    return value

#here we need both the db2 connection and excell sheet data
def getstatus(userinput):
    segment = segmentcheck(userinput)
    db_connect = DB2.connect("DATABASE=DB0T;HOSTNAME=GWYA0002;PORT=50000;PROTOCOL=TCPIP;UID=tsupb9f;PWD=apr19apr;", "",
                             "")
    SQLCommand = ("SELECT CAL_DESC, GRP_NM FROM D6744DBC.CAL_RUN WHERE CAL_CYC_RN = '"+ str(segment).upper() +"' ORDER BY CAL_RUN_DT DESC FETCH FIRST ROW ONLY; COMMIT;")
    stmt = DB2.exec_immediate(db_connect, SQLCommand)
    rslt = DB2.fetch_tuple(stmt)
    return "for "+segment+" segment,"+ rslt[0] + " status is " + rslt[1]
    # add DB2 coloumn for this approval

#here we need the DB2 connection
def Getapproval(userinput):

    segment = segmentcheck(userinput)
    if (segment == None):
        db_connect = DB2.connect("DATABASE=DB0T;HOSTNAME=GWYA0002;PORT=50000;PROTOCOL=TCPIP;UID=tsupb9f;PWD=apr19apr;", "",
                             "")
        SQLCommand = ("SELECT CAL_DESC FROM D6744DBC.CAL_RUN WHERE CAL_CYC_RN ='" + str(segment).upper() + "' with ur;")
        stmt = DB2.exec_immediate(db_connect, SQLCommand)
        rslt = DB2.fetch_tuple(stmt)
        # write a close connection statement
        if rslt[0] == "pp1":
            return "all jobs for this segment are Approved"
        else:
            print("Carl:pending approval for this job , please approve by saying yes or no")
            decision = input()
            if decision == "Yes" or decision == "yes":
                return "approval accepted - approved by <user>"
            else:
                return "Thanks, do you want to know anything more ?"
        #send a mail what's the reason for not approving the run.
    else:
        return "what is the segment ?"


# Generating response
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! i din't get you ! time need to sit under a banyan tree !"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx+1]
        return robo_response


flag=True
print("Carl: This is Carl at your Service!")
while(flag==True):
    user_response = input()
    user_original = user_response
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("Carl: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("Carl: "+greeting(user_response))
            else:
                print("Carl: ",end="")
                bot_response = response(user_response)
                if(bot_response=="processfaq."):
                    bot_response = getFAQ()
                else:
                    if bot_response == "getmonth.":
                        bot_response = getmonth(user_original)
                    else:
                        if bot_response == "processtoday.":
                            bot_response = getToday()
                        else:
                            if bot_response == "getapproval.":
                                bot_response = Getapproval(user_response)
                            else:
                                if bot_response == "processtomorrow.":
                                    bot_response = processTomorrow()
                                else:
                                    if bot_response == "getstatus.":
                                        bot_response = getstatus(user_response)

                print(bot_response)
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("Carl: Bye! take care..")



