import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from pymongo import MongoClient

"""
Access data from database and make a basic histogram plot.

"""


def get_results():
    client = MongoClient('localhost', 27017)
    if client is None:
        print "Couldn't connect!"
    else:
        print ("Connected.")

    # change dbc values to the ones appropriate for your setup.
    # dbc = client.yelp.review_category  # ...
	dbc = client.mongo2.review_1 
    
    # Query database - get data in ascending date.
    
    client.close()
    print "Disconnected."

    return list(dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", 1).limit(5))
    


def plot_month_results(results):
    
    grouped_by_month = {'01': [], '02': [], '03': [], '04': [], '05': [], '06': [],
                         '07': [], '08': [], '09': [], '10': [], '11': [], '12': []
                         } 
    
    for review in results:
        date_splitted = review['date'].split('-')

        grouped_by_month[date_splitted[1].encode('ascii','ignore')].append(review)    # a.encode('ascii','ignore')
    
    #print grouped_by_month['04'] # IT WORKS! it prints out all the reviews of april


    def count_month_subtotals(month_key):    # month_key EX.: '01' '03' '10' ...
        total = len(grouped_by_month[month_key])
        positives = 0
        negatives = 0
        neutrals = 0

        for review in grouped_by_month[month_key]:
            
        
            sentiment = review['sentiment']

            if sentiment['type'] == 'positive':
                positives = positives + 1
            elif sentiment['type'] == 'negative':
                negatives = negatives + 1
            else:
                neutrals = neutrals + 1
        print total, positives, negatives, neutrals # IT WORKS! it prints out the subtotals of the month
            

         

    count_month_subtotals('01')
    count_month_subtotals('02')
    count_month_subtotals('03')
    count_month_subtotals('04')
    count_month_subtotals('05')
    count_month_subtotals('06')
    count_month_subtotals('07')
    count_month_subtotals('08')
    count_month_subtotals('09')
    count_month_subtotals('10')
    count_month_subtotals('11')
    count_month_subtotals('12')
        







    #total_plot_dict = {'1': [{'total'}], '2': [], '3': [], '4': [], '5': [], '6': [],
        #                 '7': [], '8': [], '9': [], '10': [], '11': [], '12': []
         #                } 

    #for reviews_of_month in grouped_by_month.iteritem():
        




     #   total = len(reviews_of_month)
      #  positives = 0
       # negatives = 0
       # neutrals = 0

        #for reviews in reviews_of_month:
         #   if review['sentiment'].['type'] == "positive":
          #      positives += 1
           # elif review['sentiment'].['type'] == "negative":
            #    negatives += 1
            #else:
             #   neutrals += 1

    #total_plot_dict = {'total': total, 'positives': positives,  'negatives': negatives, 'neutrals': neutrals}

    #print total_plot_dict['positives']
        #exit()
#print month_list


   # for date, grouped_daily_reviews in grouped_by_day.iterreviews():
    #    total_daily_review_count = len(grouped_daily_reviews)
     #   print(total_daily_review_count)
        # negative = []
        # positive = []
        # neutral = []
        # plot daily review count

        # for review in grouped_daily_reviews:
            # see the sentiment and add to each array respectively
        # calculate the percentage
        # plot

    # matrix_needed = HERE DO CALCULATIONS TO CREATE THE MATRIX

    # plt.plot(matrix_needed, 'g')
    # plt.show()


if __name__ == '__main__':
    
    basic_result = get_results()
    # simple_plot(basic_result)
    #plot_daily_results(basic_result) #(daily results does not make sense: too feew reviews)
    #print basic_result
    plot_month_results(basic_result)
    # print basic_result[7] #.['date'].split('-')



