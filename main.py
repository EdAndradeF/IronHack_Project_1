import numpy as np
import pandas as pd
import re


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
df_notna = df.drop(columns=['Unnamed: 23',
                            'Unnamed: 22',
                            'Case Number',
                            'Case Number.1',
                            'Case Number.2',
                            'href formula',
                            'href',
                            'pdf'])
# limpando linhas nulas
linenan = df_notna.loc[df_notna.isnull().all(axis=1)].index
df_notna = df_notna.drop(index=linenan)

# todo limpando a coluna 'Fatal (Y/N))' e renomeando para 'Fatal'
# todo informacoes ausentes podem estar na coluna 'Injury'

df_notna = df_notna.rename(columns={'Fatal (Y/N)': 'Fatal'})

# dados na coluna Fatal ['N', 'Y', nan, 'M', 'UNKNOWN', '2017', ' N', 'N ', 'y']
# padronizando a coluna Injury para rodar na funcao limp_fatal(), substituindo nulos po string
df_notna.loc[df_notna.loc[:, 'Injury'].isna(), 'Injury'] = 'NaN'
df_notna.loc[:, 'Fatal'] = df_notna.loc[:].apply(limp_fatal, axis=1)
#serie fatal limpa
ind_fatal = df_notna['Fatal']
df.head(10)



print(df_notna)

