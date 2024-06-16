import numpy as np
from ultralytics import YOLO
import streamlit as st
import pandas as pd
import altair as alt
import pickle
import plotly.express as px

st.set_page_config(page_title="Player Stats", layout="wide")
@st.cache_data
def df():
    with open('stubs/df.pkl', 'rb') as f:
        dfs = pickle.load(f)
    return dfs
dfs = df()
df_velo_dis = dfs[0]
df_possesion = dfs[1]
df_possesion_n = dfs[2]


st.markdown('# :fire: Elitify ')

st.markdown('### Output')
st.video('output_videos/draw_change.mp4',format = 'video/mp4')    



#------------------ 2행 -------------------------- 
for _ in range(3):
    st.write("")

col2,col3,col4 = st.columns([2,2,2])
with col2:
    st.markdown('### :racehorse: Velocity - 속력')

    # 트랙 아이디 선택
    track_id = st.selectbox('선수의 번호', list(df_velo_dis.keys()))

    # 선택된 트랙 아이디에 해당하는 데이터프레임
    df = df_velo_dis[track_id]
    # 데이터프레임 표시
    max_velocity = df['velocity'].max()
    max_velocity_point = df[df['velocity'] == max_velocity]
    

    st.write(f'경기 중 속력 그래프')

    line_chart = alt.Chart(df).mark_line(
         color='red'
    ).encode(    
        x=alt.X('seconds', title = '초'),
        y=alt.X('velocity', title = 'km/h')
    ).properties()

    text_label = alt.Chart(max_velocity_point).mark_text(
    align='left',
    baseline='middle',
    dx=7,  # x축 오프셋
    dy=-7,  # y축 오프셋
    color='white',
    size=14
    ).encode(
        x=alt.X('seconds', title = '초'),
        y=alt.X('velocity', title = 'km/h'),
        text=alt.value('Fastest!!!')  # 라벨 텍스트
    )
    chart = line_chart + text_label

    st.altair_chart(chart, use_container_width=True)
with col4:
    st.markdown('### :runner: Distance covered - 활동량')
    user_input = st.text_input("스탯을 보고싶은 선수들의 번호를 입력해주세요 (쉼표로 구분):", "4, 5, 6, 7")

    # 입력받은 문자열을 리스트로 변환
    try:
        select_ids = [int(num) for num in user_input.split(',')]
    except ValueError:
        st.error("올바른 숫자를 쉼표로 구분하여 입력하세요.")

    if 'select_ids' in locals():
        filtered_data = {track_id: df_velo_dis[track_id] for track_id in select_ids if track_id in df_velo_dis}
        total_distances = {track_id: df['total_distance'].iloc[-1] for track_id, df in filtered_data.items()}

        if total_distances:
            distance_df = pd.DataFrame({
                '선수 번호': list(total_distances.keys()),
                '활동량(m)': list(total_distances.values())
            })

            bar_chart = alt.Chart(distance_df).mark_bar().encode(
                x=alt.X('선수 번호:O', title='선수 번호', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('활동량(m):Q', title='활동량(m)'),
                color=alt.Color('선수 번호:O', scale=alt.Scale(scheme='reds'))
            ).properties()

            st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.write("선택된 선수에 대한 데이터가 없습니다.")
    else:
        st.write("선수 번호를 입력하세요.")

with col3:
    st.markdown('### :bar_chart: Possesion - 점유율')
    Team1 = df_possesion.loc[df_possesion.index[-1],'ratio_1']
    Team2 = df_possesion.loc[df_possesion.index[-1],'ratio_2']
    data = pd.DataFrame({'Team' : ['Team1','Team2'],
                         'Values' : [Team1, Team2]})
    fig = px.pie(data, values= 'Values', names = 'Team',
                 color_discrete_sequence=['#FF6666', '#FF9999'])
    st.plotly_chart(fig)


    df_possesion_n['ratio_2'] = df_possesion_n['ratio_2'] * -1
    with st.expander("시간별 점유율 그래프"):
        fig = px.bar(df_possesion_n, x='frame_number', y=['ratio_1', 'ratio_2'], title='', barmode='overlay',
                     color_discrete_sequence=['#FF9999', '#FF6666'])
        
        fig.update_layout(
        legend=dict(
            title="", 
            xanchor="right", 
            x=1.15, 
            yanchor="top", 
            y=1
        )
    )
    
    # 범례 요소 이름 변경
        fig.for_each_trace(lambda t: t.update(name={'ratio_1': 'Team1', 'ratio_2': 'Team2'}[t.name]))
        fig.update_xaxes(title_text='초')
        fig.update_yaxes(title_text='점유율',
        tickvals=[-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        ticktext=['60%', '50%', '40%', '30%', '20%', '10%', '0', '10%', '20%', '30%', '40%', '50%', '60%']
    )
        st.plotly_chart(fig)

     

