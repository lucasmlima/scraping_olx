import pandas as pd

dicionario = {
    'text':['teste'],
    'price':['1.100.000']
}

df = pd.DataFrame(dicionario)

df['price'] = df['price'].str.replace('.','').astype(int)

print(df)

# valor = '1.100.000'

# print(int(valor))