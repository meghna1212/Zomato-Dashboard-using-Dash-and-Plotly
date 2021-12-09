#!/usr/bin/env python
# coding: utf-8

# ## Zomato Dashboard using Plotly and Dash

# Zomato is an Indian multinational restaurant aggregator and food delivery company, which has recently expanded to other global locations, and has completely disrupted the food delivery industry.
# 
# It is one of the most comprehensive and user-friendly apps where people can search for nearby restaurants and cafés, order food online, and get it delivered at their doorstep in no time. Moreover, you can also get accurate information about restaurants as it provides menus, reviews, and ratings.
# 
# Through this dashboard, I have tried to provide information about Zomato at-a-glance. I have tried to visually represent the performance of the company, using graphs and charts and show how they are distributed across the globe.
# 
# This dashboard has been made using Dash and Plotly

# - Dash is a python framework created by plotly for creating interactive web applications. It has two building blocks, layout (consisting of HTML components and Core Components) and callbacks
# - Plotly is a graphing library that is used to make interactive and publication-quality graphs

# ### Importing the Python Libraries

# In[1]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import seaborn as sns


# Here we have installed all the libraries which will be required in the creation of our dashboard

# ### Loading the dataset and understanding it

# I have used a kaggle dataset for creating this dashboard. The link for the same is as follows:
# 
# https://www.kaggle.com/shrutimehta/zomato-restaurants-data?select=zomato.csv

# In[2]:


file = "C://Users//Meghna//Desktop//Zomato Dashboard//zomato.csv"
df = pd.read_csv(file, encoding = "ISO-8859-1")
#Encoding attribute is mentioned here as certain characters could not be read by the default encoding mechnaism


# In[3]:


df.head()


# In[4]:


df.info()


# As we can see, our dataset has 21 different columns. These columns contain all the information about the restraunts which are available on the Zomato app along with their locations, ratings, average cost, availability of delivery, Rating color (denoting number of stars) etc.

# In[5]:


df.describe()


# The Kaggle dataset also had a Excel file containing the various countries along with their contry codes. That file has been loaded into our Jupyter notebook as well, as follows:

# In[6]:


contry_code_df = pd.read_excel("C:\\Users\\Meghna\\Desktop\\Zomato Dashboard\\Country-Code.xlsx")


# In[7]:


contry_code_df


# Now, I will merge the df and country_code_df datasets, using the Country Code column so that we can better identify what country is a particular restaurant located in.

# In[8]:


#Merging both the datasets and removing the Country Code column
zomato_dataset = pd.merge(df,contry_code_df,on='Country Code',how='left')
zomato_dataset.head()


# In[9]:


#Deleting the Country code column from the zomato dataset
zomato_dataset.drop(columns='Country Code', axis=1, inplace= True)


# In[10]:


zomato_dataset.head()


# In[11]:


zomato_dataset.shape


# Now, our final dataset has 9551 rows and 21 columns

# In[12]:


sns.heatmap(zomato_dataset.corr(),annot=True)


# ### Handling Missing Values

# Let us try to find out wether there are any missing values in the dataset or not, and if there are, we will try to handle them correctly.

# In[13]:


import missingno as msn
msn.bar(zomato_dataset)


# In[14]:


zomato_dataset.isnull().sum()


# As we can see that the Cuisines column has 9 missing values. Let us see how we can handle these NULL values.

# In[15]:


zomato_dataset['Cuisines'].value_counts()


# In[16]:


zomato_dataset['Cuisines'].value_counts().count()


# There are 1825 distinct values in the Cuisines column. So, in order to handle the missing values in the column, we'll replace the NULL values with "Other" to depict that these retaurants serve a different type of cuisine than these 1825 values.

# In[17]:


zomato_dataset['Cuisines'].fillna("Other", inplace=True)


# In[18]:


zomato_dataset['Cuisines'].isnull().sum()


# As we can see, there are no more NULL values in the Cuisines column of the dataset.
# 
# Now, let us see what restaurants have "Other" as the cuisine that is served there:

# In[19]:


zomato_dataset[zomato_dataset['Cuisines']=="Other"]


# ### Analysing and Visualizing the dataset

# Let's see the different countries from which restaurants are listed on Zomato

# In[20]:


country_wise_df = (zomato_dataset['Country'].value_counts())
country_wise_df


# As we can clearly see, the majority of restaurants listed on Zomato are from India, which makes sense as Zomato is a company that has its home-base in India itself. It has only recently started expanding to other countries.
# 
# Let's visulaize this data clearly using a pie-chart

# In[21]:


pie_country_wise = px.pie(country_wise_df, values=country_wise_df.values, names=country_wise_df.index, color_discrete_sequence=px.colors.sequential.Reds_r)
pie_country_wise.update_traces(textposition='inside')
pie_country_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie_country_wise.update_layout(title_text="Zomato's Presence around the World", title_x=0.5)


# In[22]:


zomato_dataset['Rating color'].value_counts()


# In[23]:


country_df = zomato_dataset[zomato_dataset['Country']=='India']
rating_df = country_df[country_df['Rating color']=='Orange']
rating_wise_city_df = rating_df['City'].value_counts()
pie_rating_wise = px.pie(rating_wise_city_df, values=rating_wise_city_df.values, names=rating_wise_city_df.index, color_discrete_sequence=px.colors.sequential.Reds_r, hole=0.6)
pie_rating_wise.update_traces(textposition='inside')
pie_rating_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie_rating_wise.update_layout(title_text="Country wise % of restaurants having selected number of stars", title_x=0.5)
pie_rating_wise


# Now lets take a look at the cities in India from where maximum number of restaurants are listed on Zomato

# In[24]:


country_wise_df = zomato_dataset[zomato_dataset['Country']=='India']
city_count = (country_wise_df['City'].value_counts())
city_count


# In[25]:


country_wise_df = zomato_dataset[zomato_dataset['Country']=='India']
city_count = (country_wise_df['City'].value_counts())
fig = px.bar(city_count, x=city_count.index, y=city_count.values,labels={'x': "Cities","y": "Number of Restaurants"},color_discrete_sequence=px.colors.qualitative.Set1)
fig.update_layout(plot_bgcolor="#f4f4f2")
#fig.update_yaxes(range=[10,20])
fig.update_layout(title_text='Cities in India listed on Zomato', title_x=0.5)


# Clearly, most of the restaurants listed on Zomato are located in New Delhi and least are in Mohali and Panchkula

# Lets take a look at how many of these restaurants in each city of India have online delivery services

# In[26]:


fig2=px.histogram(country_wise_df, x=country_wise_df['City'], color="Has Online delivery",barmode='group',
                      color_discrete_sequence=px.colors.sequential.Reds_r)
fig2.update_layout(plot_bgcolor="#f4f4f2")
fig2.update_layout(title_text='Restraunts having online delivery service', title_x=0.5)


# As expected, New Delhi has the maximum number of restaurants offering online delivery service via Zomato

# Now let's take a look at how does the rating of a restaurant vary with it's average cost for two and wether a higher cost affects rating or not

# In[27]:


city_wise_df = zomato_dataset[zomato_dataset['City']=='New Delhi']
fig = px.scatter(city_wise_df, x="Average Cost for two", y="Aggregate rating",color="Average Cost for two",
                 color_continuous_scale=px.colors.sequential.Reds_r,hover_data=["Restaurant Name"])
fig.update_layout(plot_bgcolor="#f4f4f2")
fig.update_layout(title_text='Cost for Two vs. Rating', title_x=0.5)
fig.show()


# Now, lets take a look at the rating of the restaurants in India. Let's see in which city are majority of the 5 star rating restaurants located using a donut graph.

# The Rating color column in the dataset represents the stars of the restaurant. The order is as follows:
# - Dark Green: 5 stars
# - Green: 4 stars
# - Yellow: 3 stars
# - Orange: 2 stars
# - Red: 1 star
# - White: No Rating

# In[28]:


country_df['Rating color'].value_counts()


# In[29]:


rating_df = country_df[country_df['Rating color']=='Dark Green']
rating_wise_city_df = rating_df['City'].value_counts()
pie_rating_wise = px.pie(rating_wise_city_df, values=rating_wise_city_df.values, names=rating_wise_city_df.index, 
                             color_discrete_sequence=px.colors.sequential.Reds_r, hole=0.6)
pie_rating_wise.update_traces(textposition='inside')
pie_rating_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie_rating_wise.update_layout(title_text="% of restaurants having selected number of ★", title_x=0.5)


# Naturally, most of them are in New Delhi.

# Now, lets see in which country are the majority of restaurants having 5 star rating located on the world map.

# In[30]:


rating_df_cmap = zomato_dataset[zomato_dataset['Rating color']=='Dark Green']
cmap_df = (rating_df_cmap['Country'].value_counts())
cmap_df


# In[31]:


fig = px.choropleth(cmap_df, locations=cmap_df.index, locationmode='country names',color=cmap_df.values ,color_continuous_scale=px.colors.sequential.Reds)
fig.update_layout(geo=dict(bgcolor= '#f4f4f2'), title_text = 'Restaurants having selected number of ★ by Country',title_x=0.5)


# Clearly a vast majority of them are in India itself.

# ### Creating the Dashboard using Dash and Plotly

# The first thing that we have to do is initialize the Dash app as follows:

# In[32]:


app = dash.Dash(__name__)


# Next, we specify the layout of the app, which describes what the application is supposed to look like. We have used the components such as html.Div, html.H1, html.P, dcc.Dropdown, dcc.Slider and dcc.Graph.
# 
# - The dash_core_components are higher-level components that are interactive and are generated with JavaScript, HTML, and CSS through the React.js library
# - The html_components are normal components which are used in HTML

# In[33]:


app.layout = html.Div(children=[
    
    #This is the main header of the dashboard displaying the name - ZOMATO DASHBOARD
    html.Div(children=[
        
            html.H1(children='ZOMATO DASHBOARD'), 
            html.Div(children='A one-stop dashboard to get all your information about Zomato')],
            style={'textAlign': 'center','backgroundColor':'#E23744','color': 'white','font-family':['Open Sans','sans-serif'], 
                   'font-style': ['italic'],'padding-top':'20px','padding-bottom':'40px','fontSize':17}
            ),
    
    #This is the first row of the dashboard displaying three cards
    html.Div(children=[
            
            #The first one is for the number of restaurants on Zomato app from across the world
            html.Div([
                html.H3(children="NUMBER OF RESTAURANTS WORLDWIDE", style={'fontSize':25}),
                html.P(zomato_dataset.shape[0], style={'fontSize':30})],
                style={'display':'inline-block','width': '30%','textAlign': 'center','backgroundColor': '#2D2D2D',
                       'color': 'white','margin':'25px','border-radius':'5px','box-shadow':'2px 2px 2px #1f2c56'}),
            
            #The second one displays the number of restaurants on Zomato app which are located in the country that has been
            #selected from the first dropdown
            html.Div([
                html.H3(children="NUMBER OF RESTAURANTS IN SELECTED COUNTRY", style={'fontSize':25}),
                html.P(id="numOfRestCountry", children=8652, style={'fontSize':30})],
                style={'display':'inline-block','width': '30%','textAlign': 'center','backgroundColor': '#2D2D2D',
                       'color': 'white','margin':'25px','border-radius':'5px','box-shadow':'2px 2px 2px #1f2c56'}),
        
            #The third card displays the number of restaurants on Zomato app which are located in the city that has been
            #selected from the second dropdown
            html.Div([
                html.H3(children="NUMBER OF RESTAURANTS IN SELECTED CITY", style={'fontSize':25}),
                html.P(id="numOfRestCity",children=20, style={'fontSize':30})],
                style={'display':'inline-block','width': '30%','textAlign': 'center','backgroundColor': '#2D2D2D',
                       'color': 'white','margin':'25px','border-radius':'5px','box-shadow':'2px 2px 2px #1f2c56'}),   
        
        ]),
    
    #This is the second row of the dashboard
    html.Div(children=[
            
            #This first div in the second row contains three different Dash core components 
            #Two dropdown lists and a slider
            html.Div(children=[
                    
                #The first component in this Div is a dropdown menu which displays the different countries from which
                #different restaurants are displayed on the Zomato App
                html.P('SELECT COUNTRY: ', style={'color':'white'}),
                dcc.Dropdown(
                        id="countries_dropdown",
                        multi=False,
                        clearable=True,
                        value='India',
                        placeholder="Select Countries:",
                        options=[{'label':c, 'value':c} for c in (contry_code_df['Country'])]),
                html.Br(),
                html.Br(),
                    
                #The second component in this Div is another dropdown menu which displays the different cities from the
                #selected country in earlier dropdown list, from which different restaurants are displayed on Zomato App
                html.P('SELECT CITY: ', style={'color':'white'}),
                dcc.Dropdown(
                        id="cities_dropdown",
                        multi=False,
                        clearable=True,
                        value='New Delhi',
                        placeholder="Select Cities:",
                        options=[]),
                html.Br(),
                html.Br(), 
                    
                #The final component in this Div is a slider which allows us to select ratings from 0 to 5.  
                #These ratings are based on the Rating colors specified for each restaurant. 
                #0 means No Rating and 5 means Highest Rating 
                html.P('SELECT RATING: ', style={'color':'white'}),
                html.Br(),
                dcc.Slider(
                        id='slider',
                        min=0,
                        max=5,
                        step=None,
                        marks=
                        {
                            0: '0★',
                            1: '1★',
                            2: '2★',
                            3: '3★',
                            4: '4★',
                            5: '5★'
                        },
                        value=5)
                ],
                style={'display':'inline-block','textAlign': 'left','backgroundColor': '#2D2D2D','color': 'black',
                        'margin-left':'25px','margin-right':'25px','width':'30%','border-radius':'5px',
                        'box-shadow':'2px 2px 2px #1f2c56','padding':'25px'}
            ),
            
            
            #The second div in the second row displays a static pie chart showcasing the presence of Zomato across the globe
            html.Div([
                    dcc.Graph(
                            id="pie-chart1", figure=pie_country_wise, 
                            style={'display':'inline-block','width':'57vh',
                                    'margin-left':'25px','margin-right':'25px','align':'center'})
                    ]),
        
            #This third div in the second row displays a bar chart 
            #This bar chart represents the Top 10 cities(from selected country) having the maximum number of restaurants listed
            #on Zomato
            html.Div([
                    dcc.Graph(
                            id="bar-chart", 
                            style={'display':'inline-block','width':'57vh','margin-left':'25px','margin-right':'25px',
                                   'align':'center'})]
                    )], 

            style={'display':'flex'}
        ),
    
    #This is the third row of the dashboard
    html.Div([
            
            #The first div in this row displays a grouped bar chart
            #This grouped bar chart depicts the number of restaurants having and not having online delivery service, from the 
            # Top 10 cities having maximum number of listings from selected country
            html.Div([
                    dcc.Graph(
                            id="grouped-bar-chart", 
                            style={'display':'inline-block','width':'57vh','margin-left':'25px','margin-right':'25px'})
                    ]),
            
        
            #The second div in this row displays a scatter plot
            #It shows how the rating of restaurant varies with the average price for two people for all restaurants in 
            #the selected city
            html.Div([
                    dcc.Graph(
                            id="scatter_plot", 
                            style={'display':'inline-block','width':'62vh','margin-left':'25px','margin-right':'1px'})
                    ]),

        
            #The third div in this row displays a donut chart
            #This chart shows the percentage of restaurants having selected number of stars(from slider) from different cities
            #of the selected city
            html.Div([
                    dcc.Graph(
                            id="donut_graph", 
                            style={'display':'inline-block','width':'57vh','margin-left':'25px','margin-right':'25px'})]
                    )], 

            style={'display':'flex','margin-top':'25px'}
        ),
    
        
    #This is the fourth row of the dashboard
    html.Div([
        
        #This is the a graph which depicts the denisty of restaurants in a country having selected number of stars
        html.Div([dcc.Graph(id="world_map")],style={'width':'90%','align':'center','margin-left':'25px','margin-right':'25px'})
            
            
        ]),
    
    #This is the footer of the dashboard
    html.Div(children=[
         
            html.Div(children='Created by: Meghna Rai')],
            style={'textAlign': 'center','backgroundColor':'#E23744','color': 'white','font-family':['Open Sans','sans-serif'], 
                   'font-style': ['italic'],'padding-top':'20px','padding-bottom':'20px','fontSize':17}
            )
    
])


# Next, we specify the callback section of our Dash app. The callbacks are used to establish interactivity and communication between the different components of our Dashboard.
# These are the functions that are automatically called by Dash whenever an input component's property changes, in order to update some property in another component (the output).

# In[34]:


#This callback function is used to set the values in the City Dropdown menu from Selected Country in Country Dropdown menu
@app.callback(
    Output("cities_dropdown", "options"),
    Input("countries_dropdown", "value"))
def get_city_options(countries_dropdown):
    df_result = zomato_dataset[zomato_dataset['Country']==countries_dropdown]
    return [{'label':i , 'value': i} for i in df_result['City'].unique()]


#This callback function is used to set the selected value in the City Dropdown menu as first city listed in the entire city list
@app.callback(
    Output("cities_dropdown", "value"),
    Input("cities_dropdown", "options"))
def get_city_options(cities_dropdown):
    return [k['value'] for k in cities_dropdown][0]


#This callback function is used to set the value displayed in the SECOND card
#The total number of restaurants listed on Zomato from country selected in dropdown menu 
@app.callback(
    Output("numOfRestCountry", "children"),
    Input("countries_dropdown", "value"))
def get_city_options(countries_dropdown):
    df_result = zomato_dataset[zomato_dataset['Country']==countries_dropdown]
    return df_result.shape[0]


#This callback function is used to set the value displayed in the THIRD card
#The total number of restaurants listed on Zomato from city selected in dropdown menu 
@app.callback(
    Output("numOfRestCity", "children"),
    Input("cities_dropdown", "value"))
def get_city_options(cities_dropdown):
    df_result = zomato_dataset[zomato_dataset['City']==cities_dropdown]
    return df_result.shape[0]


#This callback function is used to update the bar chart displayed in the second row depending upon the country that has been
#selected
@app.callback(
    Output("bar-chart", "figure"),
    [Input("countries_dropdown", "value")])
def update_bar_chart(countri):
    country_wise_df = zomato_dataset[zomato_dataset['Country']==countri]
    city_count = (country_wise_df['City'].value_counts())
    fig = px.bar(city_count, x=city_count.index[:10], y=city_count.values[:10],
                 labels={"x": "Cities","y": "Number of Restaurants"},color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(plot_bgcolor="#f4f4f2")
    fig.update_layout(title_text='Top 10 cities in Selected Country', title_x=0.5)
    return fig


#This callback function is used to update the grouped bar chart displayed in the third row 
#It takes the country selected in the dropdown as input and accordingly displays the Top 10 cities in that country having or not
#having online delivery service
@app.callback(
    Output("grouped-bar-chart", "figure"),
    [Input("countries_dropdown", "value")])
def update_grouped_bar_chart(countri):
    country_wise_df = zomato_dataset[zomato_dataset['Country']==countri]
    city_count = (country_wise_df['City'].value_counts())
    top_10_cities = list(city_count.index[:10])
    
    top_10_cities_df = country_wise_df[country_wise_df["City"].isin(top_10_cities)]
    
    fig2=px.histogram(top_10_cities_df, y=top_10_cities_df['City'], color="Has Online delivery",barmode='group',
                      color_discrete_sequence=px.colors.sequential.Reds_r)
    fig2.update_layout(plot_bgcolor="#f4f4f2")
    fig2.update_layout(title_text='Restraunts having online delivery service', title_x=0.5)
    
    return fig2


#This callback function is used to update the scatter displayed in the third row 
#It takes the city selected in the dropdown as input and accordingly displays how the rating of restaurants in that city varies
#with their average prices
@app.callback(
    Output("scatter_plot", "figure"),
    [Input("cities_dropdown", "value")])
def update_scatter_plot(city):
    city_wise_df = zomato_dataset[zomato_dataset['City']==city]
    fig = px.scatter(city_wise_df, x="Average Cost for two", y="Aggregate rating",color="Average Cost for two",
                     color_continuous_scale=px.colors.sequential.Reds_r,hover_data=["Restaurant Name"])
    fig.update_layout(plot_bgcolor="#f4f4f2")
    fig.update_layout(title_text='Cost for Two vs. Rating per City', title_x=0.2)
    return fig


#This callback function is used to update the donut graph displayed in the third row 
#It takes the country selected in the dropdown as well as the rating selected in the slider as input 
#It accordingly displays a graph depecting the % of restaurants in each city of that country having those many stars
@app.callback(
    Output("donut_graph", "figure"),
    [Input("countries_dropdown", "value"),Input("slider", "value")])
def update_scatter_plot(countri,val):
    country_df = zomato_dataset[zomato_dataset['Country']==countri]
    
    op='Dark Green'
    if(val == 0):
        op = 'White'
    elif(val==1):
        op = 'Red'
    elif(val==2):
        op = 'Orange'
    elif(val==3):
        op = 'Yellow'
    elif(val==4):
        op = 'Green'
    elif(val==5):
        op = 'Dark Green'
    rating_df = country_df[country_df['Rating color']==op]
    rating_wise_city_df = rating_df['City'].value_counts()
    pie_rating_wise = px.pie(rating_wise_city_df, values=rating_wise_city_df.values, names=rating_wise_city_df.index, 
                             color_discrete_sequence=px.colors.sequential.Reds_r, hole=0.6)
    pie_rating_wise.update_traces(textposition='inside')
    pie_rating_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    pie_rating_wise.update_layout(title_text="% of restaurants having selected number of ★")
    return pie_rating_wise


#This callback function is used to update the world map choropleth displayed in the fourth row 
#It takes the country selected in the dropdown as input 
#This map depicts the denisty of restaurants having selected number of stars, from across the world
@app.callback(
    Output("world_map", "figure"),
    [Input("slider", "value")])
def update_world_map(val):
    
    op='Dark Green'
    if(val == 0):
        op = 'White'
    elif(val==1):
        op = 'Red'
    elif(val==2):
        op = 'Orange'
    elif(val==3):
        op = 'Yellow'
    elif(val==4):
        op = 'Green'
    elif(val==5):
        op = 'Dark Green'
        
    rating_df_cmap = zomato_dataset[zomato_dataset['Rating color']==op]
    cmap_df = (rating_df_cmap['Country'].value_counts())
    
    fig_world = px.choropleth(cmap_df, locations=cmap_df.index, locationmode='country names',color=cmap_df.values ,
                              color_continuous_scale=px.colors.sequential.Reds)
    fig_world.update_layout(geo=dict(bgcolor= '#f4f4f2'), title_text = 'Restaurants having selected number of ★ by Country',
                            title_x=0.5)
    return fig_world


# Finally, we run the application on our local server and get the final outcome.

# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=False)

