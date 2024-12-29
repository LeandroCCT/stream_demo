import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to load preprocessed data
@st.cache_data
def load_data():
    return pd.read_csv("forecast_final.csv")  
# Load data
df_merged = load_data()

# Create the figure
fig = go.Figure(
    data=[
        go.Scatter(
            x=df_merged.index,
            y=df_merged['Value_ire'],
            mode='lines',
            name='Ireland',
            line=dict(color='mediumseagreen')
        ),
        go.Scatter(
            x=df_merged.index,
            y=df_merged['Value_spa'],
            mode='lines',
            name='Spain',
            line=dict(color='salmon')
        ),
        go.Scatter(
            x=df_merged.index,
            y=df_merged['Value'],
            mode='lines',
            name='Poland',
            line=dict(color='steelblue')
        )
    ],
    layout=go.Layout(
        title="Animated Time Series Comparison",
        xaxis=dict(
            title='Date',
            range=[df_merged.index[0], df_merged.index[-1]]
        ),
        yaxis=dict(
            range=[
                df_merged[['Value_ire', 'Value_spa', 'Value']].min().min(),
                df_merged[['Value_ire', 'Value_spa', 'Value']].max().max()
            ]
        ),
        showlegend=True,
        width=1000,
        height=700,
        updatemenus=[dict(
            type='buttons',
            xanchor='left',
            y=-0.35,
            direction='left',
            buttons=[
                dict(
                    label='Play',
                    method='animate',
                    args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]
                ),
                dict(
                    label='Pause',
                    method='animate',
                    args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')]
                )
            ]
        )]
    )
)

# Add animation frames
frames = [go.Frame(
    data=[
        go.Scatter(
            x=df_merged.index[:k],
            y=df_merged['Value_ire'][:k],
            mode='lines',
            name='Ireland',
            line=dict(color='mediumseagreen')
        ),
        go.Scatter(
            x=df_merged.index[:k],
            y=df_merged['Value_spa'][:k],
            mode='lines',
            name='Spain',
            line=dict(color='salmon')
        ),
        go.Scatter(
            x=df_merged.index[:k],
            y=df_merged['Value'][:k],
            mode='lines',
            name='Poland',
            line=dict(color='steelblue')
        )
    ],
    name=str(k)
) for k in range(1, len(df_merged) + 1)]

fig.frames = frames

# Add range slider
fig.update_xaxes(rangeslider_visible=True)

# Display the Plotly figure in Streamlit
st.plotly_chart(fig, use_container_width=True)
