# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your smoothie!"""
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe,use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients,name_on_order)
    values('"""+ ingredients_string +"""','"""+name_on_order+"""')"""

    time_to_insert = st.button("SUBMIT ORDER")
    #st.write(my_insert_stmt)
    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.write('Your Smoothie is Ordered,'  +name_on_order+ '!',icon = '✅')


#New section to display fruitvice nutrition information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruitvice_response.json)
fv_df = st.dataframe(data=fruityvice_response.josn(),use_container_width=True)
