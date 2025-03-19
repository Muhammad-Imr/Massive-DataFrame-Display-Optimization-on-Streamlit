import streamlit as st
import pandas as pd
import pyarrow.parquet as pq
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO

@st.cache_data
def load_data():
    df = pd.read_csv("psych_table.csv")  
    return df

df = load_data()

def make_clickable(link):
    if pd.notna(link):
        return f'<a href="{link}" target="_blank">🔗</a>'
    return ""

df['link'] = df['link'].apply(make_clickable)

builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_default_column(resizable=True, wrapText=True, filterable=True)
builder.configure_column('Item DB', width=80)
builder.configure_column('Variable ID', width=80)
builder.configure_column('Item Text', width=300)
builder.configure_column('link', width=50, cellRenderer='''function(params) { return params.value; }''')

st.title("Massive DataFrame Viewer")
st.write("Displaying full DataFrame (~120K rows × ~1K columns) with optimized performance")

grid_response = AgGrid(
    df,
    gridOptions=builder.build(),
    allow_unsafe_jscode=True,
    height=700,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=True,
    theme='streamlit'
)

csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False)
st.download_button(label="Download CSV", data=csv_buffer.getvalue(), file_name="psych_table.csv", mime="text/csv")

st.subheader("Optimization Techniques Used:")
st.markdown("""
- **@st.cache_data**: Ensures the DataFrame loads only once per session.
- **AgGrid**: Allows smooth scrolling and efficient large DataFrame rendering.
- **JavaScript Custom Renderer**: Ensures hyperlinks are properly clickable.
- **Custom Column Widths**: Ensures better readability without unnecessary horizontal scrolling.
- **Streamlit Theme**: Provides a consistent UI experience.
""")
