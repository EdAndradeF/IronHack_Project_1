import numpy as np
import pandas as pd
import re
from pandas_profiling import ProfileReport


def limp_year(row):
    date = row['Date']
    if row['Year'] != row['Year']:
        return date[-4:]
    else:
        return row['Year']


def limp_fatal(row):

    '''recebe as linhas e baseada dos dados da colunas:
                            Fatal e Injury, padroniza os dados com
                                                            0; 1; np.nan
                            se fatal = 0
                            se nao fatal = 1
                            sem o dado = np.nan
    '''

    if isinstance(row['Fatal'], float) or row['Fatal'] == 'UNKNOWN':
        if row['Injury'] == 'NaN':
            return np.nan
        elif bool(re.search('fatal', row['Injury'].lower())):
            return 1
        else:
            return 0
    elif 'n' == row['Fatal'].lower().strip() or row['Fatal'] == '2017' or row['Fatal'] == 'M':
        return 0
    elif 'y' == row['Fatal'].lower().strip():
        return 1



df = pd.read_csv('attacks.csv', sep=',', encoding='ANSI')

pd.set_option('display.max_columns', None)
# limpando colunas inuteis (nulas e com dados repetidos de outras colunas)
df_fatal = df.loc[:, ['Case Number', 'Date', 'Year', 'Type',
                      'Country', 'Activity', 'Injury', 'Fatal (Y/N)']]
# limpando linhas nulas
linenan = df_fatal.loc[df_fatal.isnull().all(axis=1)].index
df_fatal = df_fatal.drop(index=linenan)

# limpando a coluna 'Fatal (Y/N))' e renomeando para 'Fatal'
# informacoes ausentes podem estar na coluna 'Injury'
df_fatal = df_fatal.rename(columns={'Fatal (Y/N)': 'Fatal'})

# dados na coluna Fatal ['N', 'Y', nan, 'M', 'UNKNOWN', '2017', ' N', 'N ', 'y']
# padronizando a coluna Injury para rodar na funcao limp_fatal(), substituindo nulos po string
df_fatal.loc[df_fatal.loc[:, 'Injury'].isna(), 'Injury'] = 'NaN'
df_fatal.loc[:, 'Fatal'] = df_fatal.loc[:].apply(limp_fatal, axis=1)
#serie fatal limpa

# tirando os espacos e caracteres especiais dos nomes de paises
countrys = lambda x : re.sub('[^\w /]', '', x).strip() if isinstance(x, str) else np.nan
df_fatal.loc[:, 'Country'] = df_fatal.loc[:, 'Country'].apply(countrys)


# Faxina nos Anos
ano = df_fatal.loc[:, 'Date'].str.extract('(\d{4})')
df_fatal.loc[:, 'Year' ] = ano[0].astype(float)
dropano = df_fatal['Year'] >= 1950
df_fatal = df_fatal[dropano]
df_fatal.loc[:, 'Year'] = df_fatal.loc[:, 'Year'].astype(int)




print(df_fatal)
# print(df_fatal.loc[df_fatal['Type'] == 'Invalid', :])






