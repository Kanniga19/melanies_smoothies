# Import required libraries
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Set up Streamlit app
st.title("🥤 Customize Your Smoothie 🥤")
st.write("Choose the fruit you want in your custom smoothie!")

# Establish Snowflake connection
connection_parameters = {
    "account": st.secrets["connections.snowflake"]["World Data Emp"],
    "user": st.secrets["connections.snowflake"]["kannniga"],
    "password": st.secrets["connections.snowflake"]["Kanniga@19!11!2004"],
    "warehouse": st.secrets["connections.snowflake"]["compute_wh"],
    "database": st.secrets["connections.snowflake"]["smoothies"],
    "schema": st.secrets["connections.snowflake"]["public"]
}
session = Session.builder.configs(connection_parameters).create()

# Get user input for smoothie name
name_on_order = st.text_input("Name on Smoothie:")
st.write(f"The name on smoothie will be: {name_on_order}")

# Fetch fruit options from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
fruit_options = [row.FRUIT_NAME for row in my_dataframe]

# User selects up to 5 ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_options, max_selections=5)

# Process user selection
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    # Construct parameterized SQL query
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
        VALUES (?, ?)
    """

    submit_order = st.button("Submit Order")
    
    if submit_order:
        session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")

# Close the Snowflake session after operations
session.close()
