import pandas as pd 
import streamlit as st 
import plotly.express as px 
from PIL import Image

st.set_page_config(page_title='Survey_result.xlsx')
st.header('Top 500 Indian City literacy Survey')
st.subheader('Was the tutorail helpful ?')


# Load Data frame

excel_file ='Survey_result.xlsx'
sheet_name ='DATA'

df = pd.read_excel(excel_file,
				   sheet_name=sheet_name,
				   usecols='A:E',
				   header=0)


df_participants = pd.read_excel(excel_file,
								sheet_name=sheet_name,
								usecols='F:G',
								header=0)

df_participants.dropna(inplace=True)




# -- Streamlit selection 

state = df['State'].unique().tolist()
population_total = df['population_total'].tolist()


population_total_selection = st.slider('Population_total:',
							min_value = min(population_total),
							max_value = max(population_total),
							value = (min(population_total),max(population_total)))

state_selection = st.multiselect('State:',
								 state,
								 default = state)

# -- Filter data frame based on selection 

mask = (df['population_total'].between(*population_total_selection)) & (df['State'].isin(state_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Availabe Results:{number_of_result}*')
							

# -- Group dataframe after selection 

df_grouped = df[mask].groupby(by=['State']).count()[['Rating']]
df_grouped = df_grouped.rename(columns={'Rating':'State_literacy_occurance'})
df_grouped = df_grouped.reset_index()



# ---PLOT BAR CHART

bar_chart = px.bar(df_grouped,
                  x='State',
                  y='State_literacy_occurance',
                  text = 'State_literacy_occurance',
                  color_discrete_sequence = ['#F63366']*len(df_grouped),
                  template = 'plotly_white')
                                    
st.plotly_chart(bar_chart)                   

# -- Display Image and Data Frame

col1, col2 = st.columns(2)
image = Image.open('images/survey.jpg')
col1.image(image,
	    caption = 'SURVEY',
	    use_column_width =  True,
	    )


col2.dataframe(df)

# -- Plot Pie Chart 

pie_chart = px.pie(df_participants,
			        title='Total No.of Participants',
			        values='literates_total',
			        names='States')

st.plotly_chart(pie_chart)



