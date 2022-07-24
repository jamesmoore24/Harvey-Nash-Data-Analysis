import pandas as pd

def countSheet(sheet, countVar):
    """
    Parameters:
        sheet: Path to preadsheet with financial information
        countVar: what we want to count ('companies', 'columns', 'rows', 'cells')
            - 

    Returns:
        Amount of anything within the sheet
    """
    data = pd.read_excel(sheet)

    if countVar == 'companies':
        company_set = set()
        for index, row in data.iterrows():
            company_set.add(row['symbol'])
        return len(company_set)
    elif countVar == 'columns':
        return len(data.columns)
    elif countVar == 'cells':
        return len(data.index)
    elif countVar == 'cells':
        return len(data.index)*len(data.columns)

print(countSheet('data_fmp.xlsx', 'companies'))



