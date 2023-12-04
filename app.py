from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import time

from sort import mergesort, quicksort

app = Flask(__name__)

google_playstore_df = pd.read_csv('data/Google-Playstore.csv')

# get rid of all NaN values, there should still be over 1 million rows
google_playstore_df.dropna(inplace=True)

# get rid of unwanted columns
col_to_drop = ['Rating Count', 'Minimum Installs', 'Maximum Installs', 'Size', 
               'Minimum Android', 'Developer Id', 'Developer Website', 'Developer Email',
               'Last Updated', 'Content Rating', 'Privacy Policy', 'Ad Supported',
               'Editors Choice', 'Scraped Time', 'App Id']
google_playstore_df.drop(columns=col_to_drop, inplace=True)

# clean up the install column to convert str values to ints and rename
google_playstore_df['Installs'] = google_playstore_df['Installs'].str.replace(',', '')
google_playstore_df['Installs'] = google_playstore_df['Installs'].str.rstrip('+').astype(np.int64)
google_playstore_df.rename(columns={'Installs': 'Approximate Installs'}, inplace=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    categories = google_playstore_df['Category'].unique()
    currencies = google_playstore_df['Currency'].unique()

    if request.method == 'POST':
        # find the selected categories, currencies, and in app purchase types
        selected_categories = request.form.getlist('selected_categories')
        selected_currencies = request.form.getlist('selected_currencies')
        in_app_purchases = request.form.getlist('in_app_purchases')
        sorting_alg = request.form.get('sort')
        sort_by = request.form.get('sort_by')

        # find the number of results to display
        if request.form.get('num_res') == None or request.form.get('num_res') == '': 
            num_res = 100   # if there is invalid input, use 100 as default
        else:
            num_res = int(request.form.get('num_res'))
        
        # make sure the user selected things or else it will be empty
        if selected_categories and selected_currencies and in_app_purchases:
            # start timer
            start = time.time()

            # create table from the user input
            res_df = filter(google_playstore_df, selected_categories, selected_currencies, in_app_purchases)
            num_matches = res_df.shape[0]  # obtain the number of filtered results before sorting
            res_df = perform_sort(res_df, sorting_alg, sort_by, num_res)
            num_rows = res_df.shape[0]  # obtain the number of rows in the resulting table

            # limit the amount of results shown to avoid using too much memory
            if num_rows > 1000:
                res_df = res_df.head(1000)
            res_df_html = format(res_df)

            # end timer
            end = time.time()
            total_time = end - start
            
            # render the results
            return render_template('index.html', categories=categories, currencies=currencies, 
                                   res_df_html=res_df_html, num_matches = num_matches, 
                                   num_rows = num_rows, total_time = total_time)
    
    # render the default template
    return render_template('index.html', categories=categories, currencies=currencies)

def filter(df, categories, currencies, in_app_purchases):
    # find the selected categories, currencies
    df = df[google_playstore_df['Category'].isin(categories)]
    
    # filter currency type
    df = df[df['Currency'].isin(currencies)]

    # filter by whether in app purchases are included
    if 'True' in in_app_purchases and 'False' in in_app_purchases:
        pass
    elif 'True' in in_app_purchases:
        df = df[df['In App Purchases'] == True]
    elif 'False' in in_app_purchases:
        df = df[df['In App Purchases'] == False]
    
    return df

def perform_sort(df, sorting_alg, sort_by, num_res=100):
    # note: both are descending
    if sorting_alg == 'mergesort':
        df = mergesort(df, sort_by)
    else:
        df = quicksort(df, sort_by)
    return df.iloc[:num_res]

def format(df):
    # converts the pandas dataframe to html
    df.reset_index(drop=True, inplace=True)
    return df.to_html(classes='table table-striped', header="true", index=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
