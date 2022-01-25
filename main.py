import numpy as np
import pandas as pd
import re
from pandas_profiling import ProfileReport


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
df_fatal = df.loc[:, ['Date', 'Year', 'Type',
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



# ['Boating', 'Unprovoked', 'Invalid', 'Provoked',
# 'Questionable', 'Sea Disaster', nan, 'Boat', 'Boatomg']
df_fatal.loc[(df_fatal['Type'] == 'Boat') | (df_fatal['Type'] == 'Boatomg'), 'Type'] = 'Boating'
df_fatal.loc[df_fatal.loc[:, 'Type'].isna(), 'Type'] = 'Questionable'

# excluindo mais algumas linhas sem dados relevantes
df_fatal.loc[df_fatal.loc[:, 'Injury'] == 'NaN', 'Injury'] = np.nan
df_fatal = df_fatal.loc[df_fatal['Injury'] == df_fatal['Injury'], :]


ataques = (df_fatal['Type'] == 'Provoked') | (df_fatal['Type'] == 'Unprovoked')
df_fatal.loc[(df_fatal['Fatal'] == 0) & ataques, 'NOT Fatal'] = 1
df_fatal.loc[df_fatal['NOT Fatal'].isna(), 'NOT Fatal'] = 0
df_fatal['NOT Fatal'] = df_fatal['NOT Fatal'].astype(int)

mortsematk = (df_fatal['Fatal'] == 1) & (df_fatal['Type'] == 'Invalid')
df_fatal.loc[mortsematk, 'Fatal'] = 0
df_fatal.loc[:,'Fatal'] = df_fatal['Fatal'].astype(int)

inva_boat = pd.get_dummies(df_fatal['Type']).iloc[:, :2]

df_fatal = pd.concat([df_fatal, inva_boat], axis=1, )
df_fatal = df_fatal.drop(columns='Date').reset_index()
df_fatal = df_fatal.drop(index=4063)

perlocal = df_fatal.groupby('Country')[['Fatal', 'NOT Fatal', 'Boating', 'Invalid']].sum()
perano = df_fatal.groupby('Year')[['Fatal', 'NOT Fatal', 'Boating', 'Invalid']].sum()

print(perano)

# df_fatal.info()



# print(df_fatal.loc[df_fatal['Type'] == 'Invalid', :])






