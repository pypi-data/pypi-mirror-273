import ph_utils.date as date

def date_test():
    print(date.parse())
    print(date.parse('2023-08-14 15:23:23'))
    print(date.parse('20230814 152323'))
    print(date.parse('2023/08/14 15:23:23', '%Y/%m/%d %H:%M:%S'))
    print(date.parse(1691997308))
    print(date.parse(date.parse()))
