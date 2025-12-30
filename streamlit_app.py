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
import pandas as pd
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Bring in both columns (FRUIT_NAME + SEARCH_ON)
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)

# ✅ Make a Pandas version called pd_df (lab requirement)
pd_df = my_dataframe.to_pandas()

# Multiselect should show fruit names (FRUIT_NAME)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # ✅ Lab-required lookup pattern using loc + iloc
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        # ✅ Lab-required sentence
        st.write("The search value for ", fruit_chosen, " is ", search_on, ".")

        st.subheader(f"{fruit_chosen} Nutrition Information")

        # ✅ Use SEARCH_ON value for the API call
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        )

        st.dataframe(smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! " + name_on_order, icon="✅")


