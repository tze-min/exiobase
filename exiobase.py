import streamlit as st
import altair as alt
import pandas as pd

def get_data():
    data = pd.read_csv('exiobase_2022.csv')
    return data

def filter_data(intensity_data, selected_categories, selected_market):
    subset = intensity_data[intensity_data['exiobase_category'].isin(selected_categories)]
    subset = subset[subset['market'] == selected_market]
    subset['ef_kgco2e_per_euro'] = round(subset['ef_kgco2e_per_euro'], 2)
    return subset

def plot_data(intensity_data, selected_categories, selected_market, transaction_amount=1):
    subset = filter_data(intensity_data, selected_categories, selected_market)
    subset['emissions_kgco2e'] = subset['ef_kgco2e_per_euro'] * transaction_amount
    c = alt.Chart(subset).encode(
        x = 'region',
        y = 'emissions_kgco2e',
        color = 'exiobase_category',
        text = 'emissions_kgco2e'
    )
    return c.mark_point() + c.mark_text(align='left', dy=0, dx=7)

def plot_efs(intensity_data, selected_categories, selected_market):
    subset = filter_data(intensity_data, selected_categories, selected_market)
    c = alt.Chart(subset).encode(
        x = 'region',
        y = 'ef_kgco2e_per_euro',
        color = 'exiobase_category',
        text = 'ef_kgco2e_per_euro'
    )
    return c.mark_point() + c.mark_text(align='left', dy=0, dx=7)


intensity_data = get_data()

with st.sidebar:
    st.title('exiobase')

    exio_categories = st.multiselect(
        'choose product categories',
        intensity_data.exiobase_category.unique(),
        ['Cattle', 'Products of meat cattle']
    )
    market = st.selectbox(
        'choose market',
        intensity_data.market.unique(),
        2
    )
    transaction_amount = st.number_input(
        'transaction amount in euros', value=1
    )

st.markdown('emissions')
emissions_chart = plot_data(intensity_data, exio_categories, market, transaction_amount)
st.altair_chart(emissions_chart, use_container_width=True)

st.markdown('emission factors')
intensity_chart = plot_efs(intensity_data, exio_categories, market)
st.altair_chart(intensity_chart, use_container_width=True)
st.dataframe(intensity_data)