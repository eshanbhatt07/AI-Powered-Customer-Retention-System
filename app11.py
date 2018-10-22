#import necessary packages
from flask import Flask, request
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse

import pandas as pd
import numpy as np
import predict_function




text = 'I have attempted to get a loan modification from GMAC, nka OCWEN for 4 years. I have sent in XXXX modification packages with over XXXX documents in each one with delivery confirmation, have mailed the documents using delivery confirmation, have faxed them in and have emailed them. Every time they start to process, something is missing on their end. In total, I have faxed over XXXX pages of documents trying to facilitate their processing. Now the servicing agent, OCWEN, has started a foreclosure action, even though there is a modification package on file that is, again, in process. I thought GMAC scammed us all but the real scammer here is OCWEN. They now claim I owe {$74000.00} more than my original amount owed due to late fees, interest, penalties, real estate taxes and home owner '+'s insurance. I owe more since they have nothing but give me the run around about needing more and more documents. All in an effort to make more money.'
app = Flask(__name__)
#extract the optimal customer data for the bank to evaluate current consumer score
retention_data = pd.read_csv("/Users/nuexb14/Desktop/Personal/UNCC/x2.csv")


addresses = retention_data['Address']
addresses = list(addresses)
x = '123, UNCC'
global customer_score

#Pushing Coupons based on complaint category
complaint_cat = ['Mortgage','Credit reporting', 'Debt collection']


complaint_coup = ['Sorry for the inconvenience caused! We have forwarded your complaint to the Support Staff. Meanwhile, we declare in reduction of x% in interest on your Payment for the month of October',
                      'We regret for the incovenience caused. We have forwarded your complaint to the Support Staff. Meanwhile, please login to your Web Banking Account to claim your Cashback for the month of October',
                      'We regret for the incovenience caused. We have forwarded your complaint to the Support Staff. Meanwhile, based on your purchase history we would like to reimburse you with XYZ.']


#API Route to scrap SMS data
@app.route('/sms', methods=['POST'])
def sms():

    number = request.form['From']
    
    text = request.form['Body']
    #Calling predict_sample() to classify the category of the complaint
    category = predict_function.predict_sample(text)
    
    
    my_score = list()
    
    address = retention_data.loc[retention_data['PhoneNumber'] == 7045474186, 'Address'][0]
    
    if address in addresses:
        #Calculating mean values if multiple occurences exists of the same address
        u_bal = retention_data.groupby(by='Address')['Balance'].mean()[0]
        u_sal = retention_data.groupby(by='Address')['EstimatedSalary'].mean()[0]
        u_age= retention_data.groupby(by='Address')['Age'].mean()[0]
        u_noprods = retention_data.groupby(by='Address')['NumOfProducts'].mean()[0]
        u_cs= retention_data.groupby(by='Address')['CreditScore'].mean()[0]
        
        #Calculating values based on single occurence of address. 
        bal,sal,age,noprods,cs = retention_data['Balance'][0],retention_data['EstimatedSalary'][0],retention_data['Age'][0],retention_data['NumOfProducts'][0],retention_data['CreditScore'][0]

    #Calculating customer scores based on top features
    if(u_age >37 or age > 37):
        my_score.append(2)
    else:
        my_score.append(-2)
        
    if(u_sal > 99000 or sal > 99000):
        my_score.append(1.5)
    else:
        my_score.append(-1.5)
        
    if(u_cs > 650 or cs > 650):
        my_score.append(1)
    else:
        my_score.append(-1)
    
    if(u_bal > 72000 or bal > 72000):
        my_score.append(0.5)
    else:
        my_score.append(-0.5)
    
    if(u_noprods > 1) or noprods > 1:
        my_score.append(0.2)
    else:
        my_score.append(-0.2)
        
    #Using mean value as the threshold, to evaluate the category of the customer.
    if(sum(my_score) >= 5.2):
        index_comp = complaint_cat.index(category)
        message_body = complaint_coup[index_comp]
        print("Coupon")
        
    else:
        message_body = "Sorry for the incovenience. We have forwarded your complaint to the suppport staff"
        print("Invalid")
    
    
    
    resp = MessagingResponse()
    #replyText = getReply(message_body)
    
    
    resp.message("Hello {} .{}. {} ".format(number,message_body, category))
    return str(resp)

if __name__ == '__main__':
    app.run()
    
    
    
#text1 = 'I have been divorced since XX/XX/2007 and it appears on my credit report that my ex husband is my spouse or my co-applicant. I have attach my divorce decree.'
#predict_function.predict_sample(text)