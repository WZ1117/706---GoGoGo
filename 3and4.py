import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

## Read data

df = pd.read_csv('nhanes_filtered.csv')

df = df.dropna(subset=["Family_Income","Age_Group","Diabetes"])
<<<<<<< HEAD
df['Diabetes'] = df['Diabetes'].map({'yes': 1, 'no': 0})

# Slider bar of year
year = st.slider("Year", 2009, 2013, 2017)
subset = df[df["Year"] == year]

=======
df['Diabetes'] = df['Diabetes'].map({'yes': 100, 'no': 0})

# Slider bar of year
# year = st.slider("Year", value=2009, 2013, 2017)
# subset = df[df["Year"] == year]

df['Year'] = df['Year'].replace(to_replace = [2009, 2011, 2013, 2015, 2017], value=['2009-2010', '2011-2012', '2013-2014', '2015-2016', '2017-2018'])

year =st.select_slider(
    'Select a range of year',
    options=['2009-2010', '2011-2012', '2013-2014', '2015-2016', '2017-2018'])
subset = df[df["Year"] == year]

income_type = st.radio(
    "What\'s your family income range?",
    ('<10000','10000-20000','20000-35000', '35000-55000', '55000-75000',
       '75000-100000', '>100000'))

>>>>>>> 643ad89a97f6b9d2aeda9c2f9a5f6911b843742d
# Plot of income
plot3_income = alt.Chart(subset).transform_joinaggregate(
    Rate_Family_Income='mean(Diabetes)',
    groupby=['Family_Income']
).transform_window(
    rank='rank(Rate_Family_Income)',
    sort=[alt.SortField('Rate_Family_Income', order='descending')]
).mark_bar().encode(
    y=alt.Y('Family_Income:N', sort='-x', title="Family Income Range"),
    x=alt.X('mean(Diabetes):Q', title="Diabetes Rate", axis=alt.Axis(tickCount=5)),
<<<<<<< HEAD
    color=alt.Color('Family_Income:N', title="Family_Income Range"),
    tooltip=["Family_Income", "mean(Diabetes):Q"] # tooltips upon mouse hover
).properties(
    title=f"{year} Family income vs prevalence of diabetes",
    width=600,
    height=600
)

plot3_income
=======
    color=alt.condition(
        alt.datum.Family_Income == income_type,  
        alt.value('orange'),     # which sets the bar orange.
        alt.value('steelblue')),
    tooltip=[alt.Tooltip("Family_Income", title="Family Income Range"),
             alt.Tooltip("mean(Diabetes):Q",title="Diabetes Rate")]
).properties(
    title=f"{year} Family income vs prevalence of diabetes"
)
plot3_income
st.write("Your Family Income Group is highlighted in orange.")

age_type = st.radio(
    "What\'s your age group?",
    ('<18','19-25', '26-35', '36-45', '46-55', '56-65', '>65'))

plot3_age = alt.Chart(subset).transform_joinaggregate(
    Rate_Age='mean(Diabetes)',
    groupby=['Age_Group']
).transform_window(
    rank='rank(Rate_Age)',
    sort=[alt.SortField('Rate_Age', order='descending')]
).mark_bar().encode(
    y=alt.Y('Age_Group:N', sort='-x', title="Age Group"),
    x=alt.X('mean(Diabetes):Q', title="Diabetes Rate", axis=alt.Axis(tickCount=5)),
    color=alt.condition(
        alt.datum.Age_Group == age_type,  
        alt.value('orange'),     # which sets the bar orange.
        alt.value('#9467bd')),
    tooltip=[alt.Tooltip("Age_Group", title="Age Group"),
             alt.Tooltip("mean(Diabetes):Q",title="Diabetes Rate")]
).properties(
    title=f"{year} Age Group vs Prevalence Of Diabetes"
)

plot3_age
st.write("Your Age Group is highlighted in orange.")

# Plot4
# Change data from wide to long
disease_long = pd.melt(df, id_vars=["Year","Diabetes","Gender"], value_vars=["High_Blood_Pressure","Kidney_Issue","Coronory_Heart_Disease","Thyroid_Issue","Liver_Issue"],var_name="Disease_type")
disease_long = disease_long.dropna(subset=["Disease_type","value"])
disease_long['Disease_type'] = disease_long['Disease_type'].replace(to_replace = ["High_Blood_Pressure","Kidney_Issue","Coronory_Heart_Disease","Thyroid_Issue","Liver_Issue"], value=['High Blood Pressure', 'Kidney Issue', 'Coronory Heart Disease', 'Thyroid Issue', 'Liver Issue'])
disease_long = disease_long[disease_long["value"] != "no"]

# disease multiselect
disease = st.multiselect('Do you have underlying health conditions:',
                  ['High Blood Pressure', 
                   'Kidney Issue', 
                   'Coronory Heart Disease', 
                   'Thyroid Issue', 
                   'Liver Issue'],
                   'High Blood Pressure')
subset = disease_long[disease_long["Disease_type"].isin(disease)]


disease_selection = alt.selection_single(
    fields=['Disease_type'], 
    bind='legend'
)

# multiple barchart
plot4 = alt.Chart(subset).transform_joinaggregate(
    Rate='mean(Diabetes)',
    groupby=['Disease_type']
).mark_bar(size=18).encode(
    # Tried to move it bottom, but did not work: header=alt.Header(titleOrient='bottom', labelOrient='bottom')
    column=alt.Column('Year:N', title="Year Range", header=alt.Header(labelAngle=-45)),
    x=alt.X("Disease_type:N", axis=alt.Axis(labels=False), title=None),
    y=alt.Y("mean(Diabetes):Q", title="Diabetes Rates"),
    color=alt.Color("Disease_type:N", title="Disease Type"),
    tooltip=[alt.Tooltip("Disease_type", title="Disease Type"),
             alt.Tooltip("mean(Diabetes):Q",title="Diabetes Rate")]
).add_selection(
    disease_selection
).properties(
    title="Diabetes Rate Under Certain Disease"
)

# plot4


year_range = ['2009-2010', '2011-2012', '2013-2014', '2015-2016', '2017-2018']
year_dropdown = alt.binding_select(options=year_range)
year_select = alt.selection_single(fields=['Year'], bind=year_dropdown, name="Select", init={'Year':year_range[0]})

subset['Diabetes_cat'] = subset['Diabetes'].map({100:'Diabetic Population', 0:'Non-diabetic Population'})

pie_chart = alt.Chart(subset
).transform_joinaggregate(
    # num_count_year='count(Disease_type)/100',
    groupby=['Year']
).mark_arc().encode(
     theta = alt.Theta(shorthand='count(Disease_type):Q'),
     color = alt.Color(field='Diabetes_cat', type='nominal', title="Health Condition"),
     tooltip=[alt.Tooltip("count(Disease_type):Q", title="Number of people"),
              alt.Tooltip("Diabetes_cat",title="Diabetes Status")]
).transform_filter(
    disease_selection
).properties(
    title="Diabetic and Non-diabetic Population Breakdown From 2009 To 2018"
    #f"{year} Age Group vs prevalence of diabetes"
)

# chart = alt.hconcat()
# for type in disease:
#     chart = base.transform_filter(datum.Disease_type== type)


final_plot = alt.vconcat(plot4, pie_chart).resolve_scale(
    color='independent'
)

final_plot
