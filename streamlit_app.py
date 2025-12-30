## Import python packages
##import streamlit as st
##import requests
#from snowflake.snowpark.context import get_active_session
##from snowflake.snowpark.functions import col

# Write directly to the app
##st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
##st.write(
##  """Choose the fruits you want in your custom Smoothie!"""
##)


##name_on_order = st.text_input('Name on Smoothie:')
##st.write('The name on your smoothie will be:', name_on_order)

##cnx = st.connection("snowflake")
##session = cnx.session()
#session = get_active_session()
##my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
##st.dataframe(data=my_dataframe, use_container_width=True)
##st.stop()

##ingredients_list = st.multiselect(
##    'Chose up to 5 ingredients:'
##    , my_dataframe
##    , max_selections=5
##)


##if ingredients_list: 
##    ingredients_string = ''

##    for fruit_chosen in ingredients_list:
##         ingredients_string += fruit_chosen + ' '
##         #st.subheader(fruit_chosen + 'Nutrition Information')
##         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
         #st.text(smoothiefroot_response.json())
##         sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

##    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
##            values ('""" + ingredients_string + """', '""" +name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()

    #st.writ`e(my_insert_stmt)
##    time_to_insert = st.button('Submit Order')

##    if time_to_insert:
##        session.sql(my_insert_stmt).collect()
##        st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")


import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Pull both columns
fruit_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))
    .to_pandas()
)

# Build mapping: label -> api_name
fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

# Multiselect shows FRUIT_NAME labels
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_label in ingredients_list:
        ingredients_string += fruit_label + " "

        api_name = fruit_map[fruit_label]  # <- THIS is the whole point
        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + api_name
        )

        st.subheader(f"{fruit_label} Nutrition Information")
        st.dataframe(smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! " + name_on_order, icon="✅")

