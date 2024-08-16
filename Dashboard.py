import streamlit as st
# import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
# import matplotlib.pyplot as plt
# import seaborn as sns



st.set_page_config(layout='wide')


file_path = './PEDE_PASSOS_DATASET_FIAP.csv'
df = pd.read_csv(file_path, delimiter=';')

#*********************** FUNCOES *********************************************
def filter_columns(df, filters: list): 
    selected_columns = [True] * len(df.columns)  
    for index, column in enumerate(df.columns):
        if any(filter in column for filter in filters): selected_columns[index] = False
    return df[df.columns[selected_columns]]

def cleaning_dataset(df):
  _df = df.dropna(subset=df.columns.difference(['NOME']), how='all') 
  _df = _df[~_df.isna().all(axis=1)] 
  return _df

def formata_numero(valor):
    return f'{valor:.2f}' 

def analyse_corr_plotly(df):
  df = df.apply(pd.to_numeric, errors='coerce')
  corr_matrix = df.corr()
  fig = px.imshow(corr_matrix,text_auto=True, aspect="auto", title="Análise do nível de correlação entre os indicadores")
  st.plotly_chart(fig)
#   fig.show()
#*************************************************************************

# gerando dataframes separados por ano (2020, 2021, 2022)
df_2020 = filter_columns(df, ['2021', '2022'])
df_2020 = cleaning_dataset(df_2020)

df_2021 = filter_columns(df, ['2020', '2022'])
df_2021 = cleaning_dataset(df_2021)

df_2022 = filter_columns(df, ['2020', '2021'])
df_2022 = cleaning_dataset(df_2022)
dados_2022 = df_2022

# criando a coluna ANO 

df_2020['ANO'] = 2020
df_2021['ANO'] = 2021
df_2022['ANO'] = 2022

# renomeando as colunas com nomes padrão

df_2020 = df_2020.rename(columns={'IAA_2020':'IAA','IAN_2020':'IAN','IDA_2020':'IDA', 'IEG_2020':'IEG', 'INDE_2020':'INDE', 'IPP_2020':'IPP', 'IPS_2020':'IPS', 'IPV_2020':'IPV', 'PONTO_VIRADA_2020':'PONTO_VIRADA', 'PEDRA_2020':'PEDRA' })
df_2020 = df_2020.drop(df_2020.columns[df_2020.columns.str.contains('2020')], axis=1)

df_2021 = df_2021.rename(columns={'IAA_2021':'IAA','IAN_2021':'IAN','IDA_2021':'IDA', 'IEG_2021':'IEG', 'INDE_2021':'INDE', 'IPP_2021':'IPP', 'IPS_2021':'IPS', 'IPV_2021':'IPV', 'PONTO_VIRADA_2021':'PONTO_VIRADA', 'PEDRA_2021':'PEDRA' })
df_2021 = df_2021.drop(df_2021.columns[df_2021.columns.str.contains('2021')], axis=1)

df_2022 = df_2022.rename(columns={'IAA_2022':'IAA','IAN_2022':'IAN','IDA_2022':'IDA', 'IEG_2022':'IEG', 'INDE_2022':'INDE', 'IPP_2022':'IPP', 'IPS_2022':'IPS', 'IPV_2022':'IPV', 'PONTO_VIRADA_2022':'PONTO_VIRADA', 'PEDRA_2022':'PEDRA' })
df_2022 = df_2022.drop(df_2022.columns[df_2022.columns.str.contains('2022')], axis=1)

# concatenando os 3 dataframes
frames = [df_2020, df_2021, df_2022]
dados_pm = pd.concat(frames)

# retirando as linas que contem dados invalidos
dados_pm = dados_pm[(dados_pm.INDE != 'D980') & (dados_pm.INDE != '#NULO!')]

# Convertendo os indicadores para dados numericos
# convertendo dados para numericos
dados_pm['INDE'] = pd.to_numeric(dados_pm['INDE'])
dados_pm['IAA'] = pd.to_numeric(dados_pm['IAA'])
dados_pm['IEG'] = pd.to_numeric(dados_pm['IEG'])
dados_pm['IPS'] = pd.to_numeric(dados_pm['IPS'])
dados_pm['IDA'] = pd.to_numeric(dados_pm['IDA'])
dados_pm['IPP'] = pd.to_numeric(dados_pm['IPP'])
dados_pm['IPV'] = pd.to_numeric(dados_pm['IPV'])
dados_pm['IAN'] = pd.to_numeric(dados_pm['IAN'])

# **************************************** TABELAS ********************************
valor_medio_indicadores = dados_pm.groupby('ANO')[['INDE','IAA', 'IEG', 'IPS','IDA', 'IPP', 'IPV', 'IAN']].mean()
valor_medio_indicadores['taxa_crescimento_inde'] = valor_medio_indicadores['INDE'].diff()
df_valor_medio_indicadores = valor_medio_indicadores.reset_index()

# quantidde de pedra por ano
pedra_por_ano = dados_pm.groupby(['PEDRA', 'ANO']).size().reset_index()
pedra_por_ano = pd.DataFrame(pedra_por_ano)
pedra_por_ano.rename(columns={0:"TOTAL"}, inplace=True)

# quantidde de pedra por ano
virada_por_ano = dados_pm.groupby(['PONTO_VIRADA', 'ANO']).size().reset_index()
virada_por_ano = pd.DataFrame(virada_por_ano)
virada_por_ano.rename(columns={0:"TOTAL"}, inplace=True)

# indicadores
indicadores = valor_medio_indicadores[['IAA', 'IEG', 'IPS','IDA', 'IPP', 'IPV', 'IAN']].T.reset_index()
indicadores = indicadores.rename(columns={'index':'Indicador'})

#total de alunos por ano
alunos_por_ano = dados_pm.groupby('ANO')['NOME'].count().reset_index()
alunos_por_ano = alunos_por_ano.rename(columns={'NOME':'TOTAL'}) 
alunos_por_ano['taxa_crescimento'] = alunos_por_ano['TOTAL'].diff()
alunos_por_ano.set_index('ANO', inplace=True)



# ************************************* CRIANDO GRAFICOS ******************************************



fig_valor_medio = px.line(df_valor_medio_indicadores,
                          x = 'ANO',
                          y = 'INDE',
                          markers=True,
                         # range_y=(6, dados_pm['INDE'].max()),
                          color = 'ANO',
                          line_dash= 'ANO',
                          title= 'Valor Medio INDE (SCATTERPLOT)')


fig_valor_medio_indicadores = px.line(indicadores, 
                                      x='Indicador', 
                                      y=[2020, 2021, 2022], 
                                      markers=True,
                                      title="Variação dos valores médios dos indicadores no decorrer dos anos")

fig_valor_medio_bar = px.bar(df_valor_medio_indicadores,
                             x = 'ANO',
                             y = 'INDE',
                             range_y=(6,8),
                             text_auto=True,
                             title='Valor Médio INDE (BAR)',
                             color='ANO')






fig_pedra_por_ano = px.bar(pedra_por_ano,
                           x = 'ANO',
                           y = 'TOTAL',
                           text_auto=True,
                           title='Quantidade de pedras por ano',
                        #    range_x=('2020', '2022'),
                           color='PEDRA'
                           )


fig_pedra_por_ano.update_layout(yaxis_title = 'Total')

fig_virada_por_ano = px.bar(virada_por_ano,
                           x = 'ANO',
                           y = 'TOTAL',
                           text_auto=True,
                           title='Ponto de viradas por ano',
                        #    range_x=('2020', '2022'),
                           color='PONTO_VIRADA'
                           )
fig_virada_por_ano.update_layout(yaxis_title = 'Total')

fig_plot = px.box(dados_pm, x="INDE", y="PEDRA", title="BOX PLOT", color='PEDRA', template="seaborn")
fig_plot.update_traces(quartilemethod="inclusive")


fig_pedra_2020 = px.pie(virada_por_ano.query('ANO == 2020'), 
                        values='TOTAL', 
                        names='PONTO_VIRADA', 
                        title='Percentual de atingimento do ponto de virada em 2020', 
                        color_discrete_sequence=px.colors.sequential.RdBu)

fig_pedra_2021 = px.pie(virada_por_ano.query('ANO == 2021'), 
                        values='TOTAL', 
                        names='PONTO_VIRADA', 
                        title='Percentual de atingimento do ponto de virada em 2021', 
                        color_discrete_sequence=px.colors.sequential.RdBu)

fig_pedra_2022 = px.pie(virada_por_ano.query('ANO == 2022'), 
                        values='TOTAL', 
                        names='PONTO_VIRADA', 
                        title='Percentual de atingimento do ponto de virada em 2022', 
                        color_discrete_sequence=px.colors.sequential.RdBu)



# fig_corr = analyse_corr(dados_pm)


# **************************************************************************************************

# st.text(f'Variação do valor do INDE nos anos de 2020,2021,2022')
# with st.container(border=True):
#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric('Media INDE', formata_numero(dados_pm['INDE'].mean()))
#     with col2:   
#         st.metric('Quantidade de registros', dados_pm.shape[0])





#**************************************** VISUALIZACAO NO STREAMLIT********************************************
st.title("ANÁLISE DADOS PASSOS MÁGICOS")
st.header('História da Passos Mágicos')
st.write('''
        "A Associação Passos Mágicos tem uma trajetória de 30 anos de atuação, trabalhando na transformação da vida de crianças e jovens de baixa renda os levando a melhores oportunidades de vida. 
         A transformação, idealizada por Michelle Flues e Dimetri Ivanoff, começou em 1992, atuando dentro de orfanatos, no município de Embu-Guaçu.
         Em 2016, depois de anos de atuação, decidem ampliar o programa para que mais jovens tivessem acesso a essa fórmula mágica para transformação que inclui: educação de qualidade, 
         auxílio psicológico/psicopedagógico, ampliação de sua visão de mundo e protagonismo. Passaram então a atuar como um projeto social e educacional, criando assim a Associação Passos Mágicos." ''')



aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(['Contexto da Análise', 'Análise do INDE', 'Análise dos 7 Indicadores', 'Analise por Pedra-Conceito', 'Análise por Virada', 'Análise Ano 2022 - Bolsistas x Rede Pública'])

with aba1:
    st.header('Motivação da Análise')
    st.write('''
             Nos dados apresentados pela Passos Mágicos, temos uma série de 3 anos de avaliações, e com esses dados poderemos observar os impactos das ações da Passos Mágicos em seus estudantes.
             Esses dados só são perceptíveis quando avaliados de forma comparada, com o passar do tempo. Nessa análise tentaremos produzir resultados que sejam relevantes para a 
             Associação Passos Mágicos, e que possam observar uma aproximação da realidade e atingindo seu objetivo, que é o atendimento às crianças e jovens do município de Embu Guaçu. O foco
             principal será na análise do INDE (Índice de Desenvolvimento Educacional), que é a medida síntese do processo avaliativo, e composto por uma dimensão acadêmica, psicossocial e
             psicopedagógica, e seus resultados sao observados pelo resultado dos sete indicadores (IAN, IDA, IEG, IAA, IPS, IPP, IPV).
             Nessa análise foi usado um dataset de 3 anos (2020, 2021, 2022), onde temos várias colunas com diversas informações. Foi preciso consolidar os dados por ano, retirar campos nulos, 
             vazios e selecionar colunas que são comuns entre os 3 anos, para que pudéssemos ter uma análise temporal no contexto da Passos Mágicos. 

             Abaixo, algumas métricas:
                          ''')
    
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('Quantidade de Features', len(list(dados_pm.columns)))
        
    with col2:   
        st.metric('Quantidade de registros', dados_pm.shape[0])

    # with col3:
    #     lista = list(dados_pm['NOME'].unique())                
    #     st.metric('Quantidade de alunos em 2020', alunos_por_ano.loc[2020])

    # with col4:
    #     lista = list(dados_pm['NOME'].unique())                
    #     st.metric('Quantidade de alunos em 2021', alunos_por_ano.loc[2021])

    # with col5:
    #     lista = list(dados_pm['NOME'].unique())                
    #     st.metric('Quantidade de alunos em 2022', alunos_por_ano.loc[2022])

    with col3:
        lista_ano = list(dados_pm['ANO'].unique())
        st.metric('Total de anos analisados', len(lista_ano))



    anos = [2020,2021, 2022]
    anos_series = pd.Series(anos)
    cols = st.columns(anos_series.size)

    with st.container(border=True):
        for i, x in enumerate(cols):
            with cols[i]:
                texto_variacao = f'Media do INDE para o ano {anos[i]}'
                st.metric(f'Total de Alunos no Ano de: {anos[i]}', alunos_por_ano.loc[anos[i]]['TOTAL'], delta=alunos_por_ano.loc[anos[i]]['taxa_crescimento'], help=texto_variacao) 




    st.dataframe(dados_pm, width=1500 )

        

with aba2:
    st.write(''' Ao analisar a média do INDE nos 3 anos disponíveis, percebemos uma ligeira queda no ano de 2021. Essa queda pode ter sido por conta de vários fatores, dentre eles redução
             das notas dos 7 indicadores, ao qual analisaremos nas próximas etapas.
             ''')
    anos = [2020,2021, 2022]
    anos_series = pd.Series(anos)
    cols = st.columns(anos_series.size)

    for i, x in enumerate(cols):
        with cols[i]:
            texto_variacao = f'Media do INDE para o ano {anos[i]}'
            st.metric(f'Ano: {anos[i]}', formata_numero(valor_medio_indicadores.loc[anos[i]]['INDE']), delta=formata_numero(valor_medio_indicadores.loc[anos[i]]['taxa_crescimento_inde']), help=texto_variacao) 

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            # st.metric('Media INDE', formata_numero(dados_pm['INDE'].mean()))
            # st.dataframe(dados_pm, )
            st.plotly_chart(fig_valor_medio_bar)
        with col2:   
            # st.metric('Quantidade de registros', dados_pm.shape[0])
            st.plotly_chart(fig_valor_medio)

with aba3:
    st.write(''' Ao analisar a media do valor dos indicadores durante os 3 anos (2020, 2021, 2022), podemos inferir que o indicador IDA (Indicador de Desempenho Acacêmico) e o indicador IEG
             podem ter sido o responsável mais provável pela queda da média do INDE no ano de 2021. Percebe-se ligeiramente uma queda na linha do ano de 2021 no indicador referido.
             O indicador IDA expressa a proficiencia dos alunos da fase 0 até a fase 7 nas provas aplicadas pelos passos mágicos (0 a 10 pontos), e o IEG são atividades extraclasses (0 a 10 pontos).
             Essa dedução pode ser baseada pelo alto correlacionamento desses indicadores citados com o INDE, como podemos observar nos graficos abaixo.
             ''')
    st.plotly_chart(fig_valor_medio_indicadores)

    analyse_corr_plotly(dados_pm[['INDE','IAA', 'IEG', 'IPS','IDA', 'IPP', 'IPV', 'IAN']])


with aba4:

    st.write(''' Aplicando os mesmos critérios de padronização das notas do INDE, foram determinados limites de quatro faixas de desempenho que resultam nas Pedras-conceito. Pedra-conceito
             Quartzo corresponde ao INDE que esteja entre 6,047 e 6,663. A pedra Ágata corresponde ao intervalo de 6,663 até 7,437. A pedra Ametista fica entre 7,437 a 8,241, enquanto que a pedra
             Topázio começa em 8,241 e vai até o valor máximo obervado. Abaixo temos a quantidade de alunos classificados pela Pedra-conceito.   
             ''')

    st.plotly_chart(fig_pedra_por_ano)
    # st.plotly_chart(fig_plot)




    # st.plotly_chart(dados_pm[['INDE','IAA', 'IEG', 'IPS','IDA', 'IPP', 'IPV', 'IAN']])


with aba5:

    st.write(''' Indicador do Ponto de Virada - IPV, é um indicador de conselho da dimensão psicopedagógica, e seus resultados foram obtidos por meio de avaliações individuais, feitas por
             membros da equipe de professores e psicopedagogos da Passos Mágicos. Esse indicador demonstra de forma ativa o estágio do desenvolvimento do estudante, ou seja, 
             passar por esse ponto significa estar apto a iniciar a transformação na sua vida por meio da educação. A avaliação é um um conjunto de aspectos que engloba o seu desenvolvimento
             emocional, sua integração à associação e o seu potencial acadêmico. Abaixo temos gráficos que apresentam os valores de IPV alcançados durante os anos analisados.  
             ''')
    
    st.plotly_chart(fig_virada_por_ano)

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.plotly_chart(fig_pedra_2020)
        with col2:
            st.plotly_chart(fig_pedra_2021)
        with col3:
            st.plotly_chart(fig_pedra_2022)        


# st.dataframe(dados_pm[['INDE']].style.highlight_max(axis=0))

with aba6:
    st.write(''' Analisando especificamente o ano de 2022, ano que tem as informações mais completas, podemos verificar que o desempenho de alunos bolsistas e levemente superior aos
             alunos da rede privada. Esse levantamentofoi feito pelo cálculo da média do INDE, análise o Ponto de Virada, análise da Pedra-Conceito e análise das disciplinas
             ministradas na Passos Mágicos (Matemática, Português e Inglês)  
             ''')

    ################TABELAS########################
    bolsistas_2022 = dados_2022.groupby(['ANO', 'INDICADO_BOLSA_2022'])['INDE_2022'].mean().reset_index()
    px.bar(data_frame=bolsistas_2022, x = 'INDICADO_BOLSA_2022', y = 'INDE_2022')

    fig_histograma = px.histogram(dados_2022, x="PONTO_VIRADA_2022", color='BOLSISTA_2022', nbins=8, text_auto=True,  title='Histograma comparativo dos alunos bolsistas com alunos não bolsistas')

    dados_2022['BOLSISTA_2022'].value_counts(normalize=True).reset_index()
    fig_proporcao_bolsista = px.pie(data_frame=dados_2022['BOLSISTA_2022'].value_counts(normalize=True).reset_index(), 
                                    values='proportion', 
                                    names='BOLSISTA_2022', 
                                    title="Proporção de Alunos Bolsistas")

    media_indicadores_2022 = dados_2022.groupby('BOLSISTA_2022')[['INDE_2022','IAA_2022', 'IEG_2022', 'IPS_2022','IDA_2022', 'IPP_2022', 'IPV_2022', 'IAN_2022']].mean().reset_index()
    fig_media_indicadores_bolsistas = px.bar(data_frame=media_indicadores_2022, 
                                             x='BOLSISTA_2022', 
                                             y=['INDE_2022','IAA_2022', 'IEG_2022', 'IPS_2022','IDA_2022', 'IPP_2022', 'IPV_2022', 'IAN_2022'], 
                                             text_auto=True, 
                                             barmode='group', 
                                             orientation='v',
                                            title='Media dos Indicadores x Alunos Bolsistas e nãao Bolsistas' )

    media_ponto_virada_2022 = dados_2022.groupby(['BOLSISTA_2022','PONTO_VIRADA_2022'])[['INDE_2022','IAA_2022', 'IEG_2022', 'IPS_2022','IDA_2022', 'IPP_2022', 'IPV_2022', 'IAN_2022']].mean().reset_index()
    fig_bolsista_ponto_virada_2022 = px.bar(data_frame=media_ponto_virada_2022, 
                                            x='PONTO_VIRADA_2022', 
                                            y=['INDE_2022','IAA_2022', 'IEG_2022', 'IPS_2022','IDA_2022', 'IPP_2022', 'IPV_2022', 'IAN_2022'], 
                                            text_auto=True, 
                                            barmode='group', 
                                            orientation='v',
                                            title='Ponto de Virada x Alunos Bolsistas e nãao Bolsistas'  )

    media_pedra_2022 = dados_2022.groupby('PEDRA_2022')[['INDE_2022','IAA_2022', 'IEG_2022', 'IPS_2022','IDA_2022', 'IPP_2022', 'IPV_2022', 'IAN_2022']].mean().reset_index()
    fig_pedra_2022 = px.bar(data_frame=media_pedra_2022, 
                            x='PEDRA_2022', 
                            y=['INDE_2022','IAA_2022', 'IEG_2022', 'IPS_2022','IDA_2022', 'IPP_2022', 'IPV_2022', 'IAN_2022'], 
                            text_auto=True, 
                            barmode='group', 
                            orientation='v',
                            title='Pedra-Conceito x Alunos Bolsistas e nãao Bolsistas'  )

    media_disciplinas_2022 = dados_2022.groupby('BOLSISTA_2022')[['NOTA_PORT_2022', 'NOTA_MAT_2022', 'NOTA_ING_2022']].mean().reset_index()
    fig_media_disciplinas_2022 = px.bar(data_frame=media_disciplinas_2022, 
                                        x='BOLSISTA_2022', 
                                        y=['NOTA_PORT_2022', 'NOTA_MAT_2022', 'NOTA_ING_2022'], 
                                        text_auto=True, 
                                        barmode='group', 
                                        orientation='v',
                                        title='Média Nota Disciplinas (Matemática, Português e Inglês) x Alunos Bolsistas e nãao Bolsistas' )


    st.plotly_chart(fig_proporcao_bolsista)
    st.plotly_chart(fig_media_indicadores_bolsistas)

    # st.plotly_chart(fig_histograma)
    st.plotly_chart(fig_bolsista_ponto_virada_2022)
    st.plotly_chart(fig_pedra_2022)
    st.plotly_chart(fig_media_disciplinas_2022)

