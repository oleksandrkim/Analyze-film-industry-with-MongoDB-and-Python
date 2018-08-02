
################################
import pandas as pd
import json
countries=[]
admissions=[]
ticket_prices=[]
gdp_s=[]
gdp_per_capita=[]
population=[]
cinemas=[]
for line in open("C:/Users/alexa/Desktop/GC/GC2/Data collection and curation/mongodb/merged_t.json", 'r'):
    #lines.append(line)
    js = json.loads(line)
    countries.append(js['country'])
    gdp_s.append(js['gdp'])
    gdp_per_capita.append(js['gdp_capita'])
    population.append(js['population'])
    admissions.append(js['cinemas'][0]['admiss'])
    cinemas.append(js['cinemas'][0]['cinemas'])
    ticket_prices.append(js['ticket_price'][0]['ticket_price'])


dict={}

dict["countries"] = countries
dict["admissions"] = admissions
dict["ticket_prices"] = ticket_prices
dict["gdp_s"] = gdp_s
dict["gdp_per_capita"] = gdp_per_capita
dict["population"] = population
dict["cinemas"] = cinemas

df = pd.DataFrame(data=dict)

pd.set_option('display.max_colwidth', -1)

df.head()

##Question 1
df['tickets_sold'] = df.apply(lambda row: row['admissions'] / row['ticket_prices'], axis=1)

#remove outliers - 68-95-99 rule is applied on "admission" column
df = df[(df['countries'] != 'Brazil') & (df['countries'] != 'China') & 
        (df['countries'] != 'Mexico') & (df['countries'] != 'Republic of Korea') &
        (df['countries'] != 'Russian Federation') & (df['countries'] != 'United States of America')]
#Brazil, China, Mexico, Republic of Korea, Russia, US

#correlation
df['tickets_sold'].corr(df['population'])

from scipy.stats import ttest_ind
ttest_ind(df['tickets_sold'], df['population'])



##Question 2

#correlation
df['cinemas'].corr(df['gdp_s'])

from scipy.stats import ttest_ind
ttest_ind(df['cinemas'], df['gdp_s'])


##Question 3
df['tickets_population_ratio'] = df.apply(lambda row: row['tickets_sold'] / row['population'], axis=1)

#top 10
df[df.Ticket == 1].sort_values('Age').head(10)


#df.to_csv('C:/Users/alexa/Desktop/GC/GC2/Data collection and curation/mongodb/merged_two.csv')