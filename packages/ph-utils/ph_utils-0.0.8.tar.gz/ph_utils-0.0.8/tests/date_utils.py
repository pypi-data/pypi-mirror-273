import ph_utils.date as date

def date_parse():
    print(date.parse())
    print(date.parse('2023-08-14 15:23:23'))
    print(date.parse('20230814 152323'))
    print(date.parse('2023/08/14 15:23:23', '%Y/%m/%d %H:%M:%S'))
    print(date.parse(1691997308))
    print(date.parse(date.parse()))

def date_set():
    date.set(None, '20230815')

def date_diff():
    print(date.diff(date.subtract(delta={'days':1}), date.parse()))

if __name__ == "__main__":
    print(date.set(values='20230814121212'))
