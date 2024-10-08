# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
streamlit.title('my parents new healthy diner')
# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """ Choose the fruits you want in your custom Smoothie!
    """
)
from snowflake.snowpark.functions import col

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'choose up to 5 ingredienten'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # More readable than concatenation

    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (?, ?)
    """

    # Button to submit the order
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        try:
            session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"Error placing order: {e}")

    st.write(f"Ingredients: {ingredients_string}")
    st.write(f"Name on order: {name_on_order}")
