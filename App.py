
import streamlit as st
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
from PIL import Image

# Настройка заголовка и текста
st.title("Система анализа данных о потребности в трудовых ресурсах")

# Настройка боковой панели
st.sidebar.title("О системе")
st.sidebar.info(
    """
    Система анализа данных о потребности в трудовых ресурсах
    """
)


# Создадим функцию для загрузки данных
def load_data(data):
    df = pd.read_csv(data, delimiter=',')
    return df


# Поле для выбора категории графиков
select_event = st.sidebar.selectbox('Выбрать данные', ('Актуальность', 'Все профессии', 'IT - рынок'))
if select_event == 'Актуальность':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(" ")
        image = Image.open('img1.png')
        st.image(image)
    with col2:
        st.markdown("### Задача, которую решает сервис для основных пользователей:")
        st.markdown("##### демонстрировать реальную и перспективную ситуацию на рынке труда, \
        иметь возможность предвидеть политические, экономические и социальные риски")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Для чего эта аналитическая система?")
        st.markdown("Информационно - аналитическая система поможет управлять человеческими ресурсами ")
        st.markdown("- предприятия")
        st.markdown("- города")
        st.markdown("- региона")
        st.markdown("- федерального округа")
        st.markdown("- страны в целом")
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        image = Image.open('img2.png')
        st.image(image)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        image = Image.open('img3.png')
        st.image(image)
    with col4:
        st.markdown("#### Для кого эта аналитическая система?")
        st.markdown("- Ученики школ")
        st.markdown("- Абитуриенты")
        st.markdown("- Руководители ВУЗов и ССУЗов")
        st.markdown("- Жители региона")

# Графики по всем профессиям
if select_event == 'Все профессии':
    st.title(f"Данные по всем профессиям")
    st.markdown("#### Размер шара:")
    st.markdown("- средний размер заработной платы, в руб.")
    st.markdown("#### Цвет соответствует выбранной группе профессий:")
    st.markdown("- ОКЗ: Общероссийский классификатор занятий")
    st.markdown("#### Размеры выборки для анализа:")
    st.markdown("- 1 499 983 классифицированных резюме")
    st.markdown("- 878 555 квалифицированных вакансий")

    # загрузка данных для всех профессий
    data1 = 'data/ip.csv'
    data2 = 'data/ipp.csv'
    data3 = 'data/yip.csv'
    data4 = 'data/ypp.csv'
    data_des1 = 'data/yip_des.csv'
    data_des2 = 'data/subgroups.csv'

    ip = load_data(data1)
    ip = ip.drop(ip.columns[[0]], axis=1)
    yip = load_data(data3)
    yip = yip.drop(yip.columns[[0]], axis=1)

    # Загрузка описаний
    yip_des = load_data(data_des1)
    yip_des = yip_des.drop(yip_des.columns[[0]], axis=1)
    ypp_des = load_data(data_des2)
    ypp_des = ypp_des.drop(ypp_des.columns[[0]], axis=1)

    # Показ описаний
    show_describe = st.sidebar.checkbox("Показать описание")
    if show_describe:
        col1, col2 = st.columns([3, 1])
        st.markdown("### Соответвие групп профессий и их названий")
        st.write(yip_des)


    # функция для построения графика по подгруппам профессий
    def draw_schedule_ip(i):
        fig = px.scatter(i,
                         x=i.count_candidate,
                         y=i.work_places,
                         size=i.vac_avg_salary,
                         color=i.group_id,
                         hover_name=i.group_name,
                         log_x=True,
                         log_y=True)
        fig.update_layout(
            title='Спрос и предложение на рынке труда по подгруппам профессий',
            legend_title_text='Группы профессий',
            xaxis=dict(
                title='Число соискателей, чел.',
                gridcolor='white',
                gridwidth=2,
            ),
            yaxis=dict(
                title='Кол-во рабочих мест, ед.',
                gridcolor='white',
                gridwidth=2,
            ),
            plot_bgcolor='rgb(232, 246, 255)'
        )
        return fig


    ip['group_id'] = ip['group_id'].astype('category')
    st.plotly_chart(draw_schedule_ip(ip), use_container_width=True)

    if show_describe:
        st.markdown("### Соответвие подгрупп профессий и их названий")
        st.write(ypp_des)

    # по профессиям
    ipp = load_data(data2)
    ipp = ipp.drop(ipp.columns[[0]], axis=1)
    ypp = load_data(data4)
    ypp = ypp.drop(ypp.columns[[0]], axis=1)


    def draw_schedule_ipp(i):
        fig = px.scatter(i,
                         x=i.count_candidate,
                         y=i.work_places,
                         size=i.vac_avg_salary,
                         color=i.okz_subgroup,
                         hover_name=i.okpdtr_name,
                         log_x=True)

        fig.update_layout(
            title='Структура рынка в разрезе подгрупп профессий',
            legend_title_text='Подгруппы профессий',
            xaxis=dict(
                title='Число соискателей, чел.',
                gridcolor='white',
                type='log',
                gridwidth=2,
            ),
            yaxis=dict(
                title='Кол-во рабочих мест, ед.',
                gridcolor='white',
                type='log',
                gridwidth=2,
            ),
            plot_bgcolor='rgb(232, 246, 255)'
        )
        return fig


    ipp['okz_subgroup'] = ipp['okz_subgroup'].astype('category')
    st.plotly_chart(draw_schedule_ipp(ipp), use_container_width=True)

    # графики по годам
    show_timerange = st.sidebar.checkbox("Выбрать год")
    if show_timerange:
        # Вычислим даты для создания временного слайдера
        min_y = min(yip['year'])
        max_y = max(yip['year'])
        y_date = st.sidebar.slider("Выбор года", min_value=min_y, max_value=max_y, value=max_y)

        st.markdown("#### Динамика по годам")

        st.write(f"Данные по группам професиий по {y_date} году")
        yip = yip[(yip['year'] == y_date)]
        yip['group_id'] = yip['group_id'].astype('category')
        st.plotly_chart(draw_schedule_ip(yip), use_container_width=True)

        ypp = ypp[(ypp['year'] == y_date)]
        ypp['okz_subgroup'] = ypp['okz_subgroup'].astype('category')
        st.write(f"Данные по подгруппам професиий по {y_date} году")
        st.plotly_chart(draw_schedule_ipp(ypp), use_container_width=True)

        ipp = (ypp.groupby("year")[["count_candidate", "work_places"]].sum()
              .join(ypp.groupby("year")["vac_avg_salary"].mean()))

        st.markdown("#### Общая информация")
        ipp = ipp[(ipp.index == y_date)]
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Количество кандидатов", value=ipp.count_candidate)
        col2.metric(label="Рабочих мест", value=ipp.work_places)
        col3.metric(label="Среднняя заработная плата", value=ipp.vac_avg_salary)


    # Вывод графиков по IT рынку
if select_event == 'IT - рынок':
    st.title("Данные по IT-рынку")

    # Загружаем данные
    data5 = 'data/main_it.csv'
    data6 = 'data/year_it.csv'

    m_it = load_data(data5)
    m_it['okpdtr'] = m_it['okpdtr'].astype('category')


    # Создадим функции для визуализации графика
    def draw_schedule_it(it):
        fig = px.scatter(it,
                         x=it.count_candidate,
                         y=it.work_places,
                         size=it.vac_avg_salary,
                         color=it.okpdtr,
                         hover_name=it.name,
                         log_x=True,
                         log_y=True)

        fig.update_layout(
            title='Структура рынка IT профессий',
            legend_title_text='Номер профессии',
            showlegend=False,
            xaxis=dict(
                title='Число соискателей, чел.',
                gridcolor='white',
                gridwidth=2,
            ),
            yaxis=dict(
                title='Кол-во рабочих мест, ед.',
                gridcolor='white',
                gridwidth=2,
            ),
            plot_bgcolor='rgb(232, 246, 255)'
        )
        return fig


    st.plotly_chart(draw_schedule_it(m_it), use_container_width=True)

    y_it = load_data(data6)
    y_it = y_it.drop(y_it.columns[[0]], axis=1)
    y_it['okpdtr'] = y_it['okpdtr'].astype('category')

    itt = (y_it.groupby("year")[["count_candidate", "work_places"]].sum()
           .join(y_it.groupby("year")["vac_avg_salary"].mean()))

    show_timerange = st.sidebar.checkbox("Выбрать год")
    if show_timerange:
        # Вычислим даты для создания временного слайдера
        min_y = min(y_it['year'])
        max_y = max(y_it['year'])
        y_date = st.sidebar.slider("Выбор года", min_value=min_y, max_value=max_y, value=2021)
        st.markdown("#### Данные об IT профессиях по годам")
        st.write(f"Данные по {y_date} году")
        y_it = y_it[(y_it['year'] == y_date)]
        st.plotly_chart(draw_schedule_it(y_it), use_container_width=True)

        st.markdown("#### Общая информация")
        itt = itt[(itt.index == y_date)]
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Количество кандидатов", value=itt.count_candidate)
        col2.metric(label="Рабочих мест", value=itt.work_places)
        col3.metric(label="Среднняя заработная плата", value=itt.vac_avg_salary)

        with st.expander("Подробнее"):
            st.write("""
                Для годов 2022-2027 используются данные из предсказания
            """)

    show_data = st.sidebar.checkbox('Показать таблицу с данными')
    if show_data:
        y_it_w = y_it.copy()
        y_it_w = y_it_w.reindex(columns=['okpdtr', 'name', 'year', 'cv_count', 'count_candidate', 'work_places',
                                         'vacancy_count', 'cv_avg_salary', 'vac_avg_salary'])
        y_it_w.rename(columns={'okpdtr': 'Код профессии'}, inplace=True)
        y_it_w.rename(columns={'name': 'Название профессии'}, inplace=True)
        y_it_w.rename(columns={'year': 'Год'}, inplace=True)
        y_it_w.rename(columns={'cv_count': 'Количество резюме'}, inplace=True)
        y_it_w.rename(columns={'count_candidate': 'Количество кандидатов'}, inplace=True)
        y_it_w.rename(columns={'work_places': 'Рабочие места'}, inplace=True)
        y_it_w.rename(columns={'vacancy_count': 'Количество вакансий'}, inplace=True)
        y_it_w.rename(columns={'cv_avg_salary': 'Средняя зарплата по резюме'}, inplace=True)
        y_it_w.rename(columns={'vac_avg_salary': 'Средняя зарплата по вакансиям'}, inplace=True)

        st.markdown("#### Данные об IT профессиях")
        st.write(y_it_w)

# streamlit run App.py
