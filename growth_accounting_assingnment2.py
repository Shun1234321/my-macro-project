import pandas as pd
import numpy as np

# pwtの読み込み
pwt90 = pd.read_stata('https://www.rug.nl/ggdc/docs/pwt90.dta')


# 国の設定
oecd_countries = [
    "Australia", "Austria", "Belgium", "Canada", "Denmark", "Finland",
    "France", "Germany", "Greece", "Iceland", "Ireland", "Italy", "Japan",
    "Netherlands", "New Zealand", "Norway", "Portugal", "Spain", "Sweden",
    "Switzerland", "United Kingdom", "United States"
]

# 対象の国/期間の絞り込み
data = pwt90[
    pwt90['country'].isin(oecd_countries) &
    pwt90['year'].between(1990, 2019)
]

# 使うデータの取り出し
relevant_cols = ['countrycode', 'country', 'year', 'rgdpna', 'rkna', 'pop', 'emp', 'avh', 'labsh', 'rtfpna']
data = data[relevant_cols].dropna()
