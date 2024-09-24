import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importar os dados (Certifique-se de que a coluna 'date' seja interpretada como data e usada como índice)
df = pd.read_csv('boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Limpar os dados (Remover os 2.5% maiores e menores de visualizações para remover outliers)
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Desenhar o gráfico de linhas
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['value'], color='red')

    # Adicionar título e rótulos de eixos
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salvar a imagem e retornar a figura (não modificar esta parte)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copiar e modificar os dados para o gráfico de barras mensal
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year  # Adicionar uma coluna com o ano
    df_bar['month'] = df_bar.index.strftime('%B')  # Adicionar uma coluna com o nome completo do mês

    # Definir a ordem correta dos meses para garantir que estejam na ordem de janeiro a dezembro
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Agrupar os dados por ano e mês e calcular a média de visualizações por mês
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Reordenar os meses para seguir a ordem correta no gráfico
    df_bar = df_bar[month_order]

    # Desenhar o gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(10, 6)).figure

    # Adicionar rótulos e legenda
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Salvar a imagem e retornar a figura (não modificar esta parte)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar os dados para os gráficos de caixa (box plots)
    df_box = df.copy()
    df_box.reset_index(inplace=True)  # Resetar o índice para manipular as colunas
    df_box['year'] = [d.year for d in df_box.date]  # Criar uma coluna para o ano
    df_box['month'] = [d.strftime('%b') for d in df_box.date]  # Criar uma coluna para o mês (abreviado)

    # Desenhar os gráficos de caixa (usando Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))  # Criar dois subgráficos lado a lado

    # Gráfico de caixa por ano (trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')  # Adicionar título
    axes[0].set_xlabel('Year')  # Rótulo do eixo X
    axes[0].set_ylabel('Page Views')  # Rótulo do eixo Y

    # Gráfico de caixa por mês (seasonality)
    order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']  # Ordem dos meses
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')  # Adicionar título
    axes[1].set_xlabel('Month')  # Rótulo do eixo X
    axes[1].set_ylabel('Page Views')  # Rótulo do eixo Y

    # Salvar a imagem e retornar a figura (não modificar esta parte)
    fig.savefig('box_plot.png')
    return fig
