#!/usr/bin/env python
# -*- coding: utf-8 -*-
# enable UTF-8 characters in the console
import re
from main import Config


def extract_number(arg1):
    if isinstance(arg1, int):  # check if integer
        return arg1
    else:
        try:
            return re.sub("[^0-9.]", "", "" + arg1 + "")
        except TypeError:
            print('Couldnt extract the number')
            return 'XXX'


def x_utf(string):
    try:
        string = string.decode('utf-8')
        return string
    except AttributeError:
        return string


def board_id(board_name):
    try:
        id = Config.parser.get('export_boards', board_name)
    except:
        print('translate - couldnt find board id or settings.ini ' + str(board_name))
        id = ' '
    return id


def query_syntax(dict):
    temp_INSERT_col = []
    temp_INSERT_val = []

    for k, v in dict.items():  # returns 2 lists, one with keys and one with values
        temp_INSERT_col += [k]
        temp_INSERT_val += [v]

    INSERT_val = ''
    INSERT_col = ''
    for i in range(len(temp_INSERT_val)):  # turn lists into one string for query syntax
        if i == len(temp_INSERT_val) - 1:
            INSERT_val += "'" + str(temp_INSERT_val[i]) + "'"
            INSERT_col += temp_INSERT_col[i]
        else:
            INSERT_val += "'" + str(temp_INSERT_val[i]) + "',"
            INSERT_col += str(temp_INSERT_col[i]) + ", "

    return INSERT_col, INSERT_val


def get_table_headers(table, con, cur):  # returns all table headers (column names)
    INSERT = "select rdb$field_name from rdb$relation_fields where rdb$relation_name='"+table+"';"  # select all column names from table
    cur.execute(INSERT)
    INSERT_temp = cur.fetchall()
    INSERT_col = []
    total_columns = len(INSERT_temp)
    for i in range(total_columns):
        temp_result = INSERT_temp[i][0].strip()  # remove white spaces
        INSERT_col += [temp_result]
    con.commit()
    return INSERT_col


def get_row_values(table, key, con, cur):  # returns all values from table with specified key (primary)
    INSERT = "select * from "+table+" where id_formatki='"+key+"'"
    cur.execute(INSERT)
    INSERT_temp = cur.fetchone()
    total_columns = len(INSERT_temp)
    INSERT_val = []
    for i in range(total_columns):
        temp_result = str(INSERT_temp[i]) if INSERT_temp[i] is not None else ''  # remove white spaces
        INSERT_val += [temp_result]
    con.commit()
    return INSERT_val


def get_columns_values(table, columns, con, cur):  # return all values of specified columns
    select = 'SELECT ' + str(columns) + ' from ' + str(table)
    cur.execute(select)
    result = cur.fetchall()
    con.commit()
    return result


class table_variables:
    def query_available(self, template, available):  # this function compares a list of available column headers in loaded database with a templete of column headers that should exist, fixes 'no column' errors
        query = {}
        for count, element in enumerate(available):
            if available[count] in template:
                query[available[count]] = template[available[count]]
            else:
                query[available[count]] = ' '
        return query

    def data_format(self, available):
        format_template = {  # set individual board values
            'BRUTTO2': '0',
            'BRUTTO1': '0',
            'BRUTTOD': '0',
            'NETTO2': '0',
            'NETTO1': '0',
            'NETTOD': '0',
            'VAT': '0',
            'BRUTTO': '0',
            'NETTO': '0',
            'NETTO_SYM': '0',
            'OPIS_OKLEINY_4': 'wg zamowienia',
            'OPIS_OKLEINY_3': 'wg zamowienia',
            'OPIS_OKLEINY_2': 'wg zamowienia',
            'OPIS_OKLEINY_1': 'wg zamowienia',
            'ID_OKLEINY_4': ' ',
            'ID_OKLEINY_3': ' ',
            'ID_OKLEINY_2': ' ',
            'ID_OKLEINY_1': ' ',
            'MAGAZYN': '0',
            'STAN': '0',
            'STAN_MIN': '0',
            'STAN_MAX': '0',
            'PRIORYTET': '0',
            'REZERWACJA': '0',
            'TYP_FORMATKI': '1',
            'ZP_SUB_SUFIX': ' ',
            'ID_F_ZESTAWU': ' ',
            'RYS_PARAM': 'RYS_PARAM',
            'ID_GRUPY': '',
            'ID_RYS': 'ID_RYS',
            'KOD': '00000',
            'INFO_MOD': 'ADMIN-2002.07.01 13:33:37',
            'INFO_DOD': 'ADMIN-2002.07.01 13:33:37',
            'RYS_TECH_1': 'ABCD1234',
            'OKLEJANIE': 'NNNN',
            'SREDNIA_WAZONA': '0',
            'WALUTA': ' ',
            'ZW': '0',
            'TYP': ' ',
            'STRUKTURA': '0',
            'KOLEJNOSC_OKLEJANIA': '0',
            'SKLADNIKI': ' ',
            'STRUKTURA_TYP': '0',
            'DRILLCODE': ' ',
            'DRILLCODE2': ' ',
            'NETTO_DOPLATA_LAKIER': '0',
            'CECHA_1': ' ',
            'PRODUKCJA_SCIEZKA': ' ',
            'OPIS_ALIAS': '',
            'DLUGOSC_FORMULA': ' ',
            'SZEROKOSC_FORMULA': ' ',
            'ILOSC_FORMULA': ' ',
            'CNC_PLIK_SZABLON': ' ',
            'DRILLBARCODE': '',
            'DRILLINFO': '',
            'DRILLBARCODE2': '',
            'DRILLINFO2': '',
            'DRILLCODE3': '',
            'DRILLBARCODE3': '',
            'DRILLINFO3': '',
            'DRILLCODE4': '',
            'DRILLBARCODE4': '',
            'DRILLINFO4': '',
            'DRILLCODE5': '',
            'DRILLBARCODE5': '',
            'DRILLINFO5': '',
            'DRILLCODE6': '',
            'DRILLBARCODE6': '',
            'DRILLINFO6': '',
            'NR_OPAKOWANIA': '0',
            'RODZAJ_PAKOWANIA': '0',
            'CNC_CZAS_OBROBKI': '0'
        }
        data_format = self.query_available(format_template, available)
        return data_format

    def data_group(self, available):
        group_template = {
            'STAN_ZAM': '0',
            'STAN': '0',
            'STAN_MIN': '0',
            'STAN_MAX': '0',
            'NETTO': '0',
            'BRUTTO': '0',
            'NETTOD': '0',
            'BRUTTOD': '0',
            'NETTO1': '0',
            'BRUTTO1': '0',
            'NETTO2': '0',
            'BRUTTO2': '0',
            'VAT': '0',
            'GRUPA': '',
            'PODGRUPA': '',
            'MAGAZYN': '0',
            'CECHA': ' ',
            'KOD': '000',
            'INFO_MOD': 'ADMIN-2002.07.01 13:33:37',
            'INFO_DOD': 'ADMIN-2002.07.01 13:33:37',
            'EKSPORT_DO_PLIKU_WYMIANY': '0',
            'ZALACZNIKI': '',
            'ZW': '0',
            'WALUTA': ' ',
            'JM': '',
            'STAN_PRD': '0',
            'WYSOKOSC': '0',
            'SZEROKOSC': '0',
            'GLEBOKOSC': '0',
            'FP1': '~0.00~0.00~0.00~',
            'FP2': '~0.00~0.00~0.00~',
            'FP3': '~0.00~0.00~0.00~',
            'FP4': '~0.00~0.00~0.00~',
            'FP5': '~0.00~0.00~0.00~',
            'FP6': '~0.00~0.00~0.00~',
            'FP7': '~0.00~0.00~0.00~',
            'FP8': '~0.00~0.00~0.00~',
            'FP9': '~0.00~0.00~0.00~',
            'FP10': '~0.00~0.00~0.00~',
            'FP11': '~0.00~0.00~0.00~',
            'FP12': '~0.00~0.00~0.00~',
            'FP13': '~0.00~0.00~0.00~',
            'FP14': '~0.00~0.00~0.00~',
            'FP15': '~0.00~0.00~0.00~',
            'FP16': '~0.00~0.00~0.00~',
            'FP17': '~0.00~0.00~0.00~',
            'FP18': '~0.00~0.00~0.00~',
            'FP19': '~0.00~0.00~0.00~',
            'FP20': '~0.00~0.00~0.00~',
            'FS1': '~~',
            'FS2': '~~',
            'FS3': '~~',
            'FS4': '~~',
            'FS5': '~~',
            'FS6': '',
            'FS7': '',
            'FS8': '',
            'FS9': '',
            'FS10': '',
            'RODZAJ': ' ',
            'TYP': ' ',
            'OPIS_ALIAS': '',
            'ZDJECIE': ' ',
            'WYSOKOSC_MIN': '0',
            'SZEROKOSC_MIN': '0',
            'GLEBOKOSC_MIN': '0',
            'WYSOKOSC_MAX': '0',
            'SZEROKOSC_MAX': '0',
            'GLEBOKOSC_MAX': '0',
            'WYSOKOSC_STANDARD': ' ',
            'SZEROKOSC_STANDARD': ' ',
            'GLEBOKOSC_STANDARD': ' ',
            'FLAGA_ZMIANY': '0',
            'SPR': '1',
            'SYMBOL_ORG': '',
            'NOTATKI': '',
            'OPIS_1': ' ',
            'EKSPORT_DO_KREATORA': '0',
            'FPD1': '',
            'FPD2': '',
            'FPD3': '',
            'FPD4': '',
            'FPD5': '',
            'FPD6': '',
            'FPD7': '',
            'FPD8': '',
            'FPD9': '',
            'FPD10': '',
            'FPD11': '',
            'FPD12': '',
            'FPD13': '',
            'FPD14': '',
            'FPD15': '',
            'FPD16': '',
            'FPD17': '',
            'FPD18': '',
            'FPD19': '',
            'FPD20': '',
            'FSD1': '',
            'FSD2': '',
            'FSD3': '',
            'FSD4': '',
            'FSD5': '',
            'FSD6': '',
            'FSD7': '',
            'FSD8': '',
            'FSD9': '',
            'FSD10': '',
            'TRYB_EDYCJI': ' '
        }
        group = self.query_available(group_template, available)
        return group

    def data_format_group(self, available):
        format_group_template = {
            'GRUPA_MATERIALU': '',
            'NUMER_W_ZESTAWIE': '0',
            'FLAGA_1': '1',
            'NR_OPAKOWANIA': '0',
            'RODZAJ_PAKOWANIA': '0',
            'ID_FORMATKI_PW': '0'
        }
        format_group = self.query_available(format_group_template, available)
        return format_group
