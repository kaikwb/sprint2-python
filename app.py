import datetime
import os
from enum import Enum

import pandas as pd
from flask import Flask
from prettytable.prettytable import PrettyTable

from models import Asset, AssetPrice, db


class MainMenuOption(Enum):
    EXIT = 0
    CREATE_ASSET = 1
    LIST_ASSETS = 2
    IMPORT_PRICE = 3
    CALC_CORRELATION = 4


main_menu = """
Digite a opção desejada:
0 - Sair
1 - Cadastrar Ativo
2 - Listar Ativos 
3 - Importar Preços
4 - Calcular correlação
"""

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def wait_key_to_continue():
    input("Pressione Enter para continuar")


def get_input(msg, cast=None, default=None):
    while True:
        try:
            inputed_text = input(msg)
            if inputed_text == "" and default is not None:
                return default
            return cast(inputed_text) if cast is not None else inputed_text
        except (ValueError, KeyboardInterrupt):
            continue


def create_asset():
    clear_console()
    asset_name = input("Digite o nome do ativo: ")
    ticker = input("Digite o ticker do ativo: ").upper()

    if Asset.query.filter_by(ticker=ticker).first() is None:
        asset = Asset(name=asset_name, ticker=ticker)
        db.session.add(asset)
        db.session.commit()

        print("Ativo cadastrado com sucesso!")
    else:
        print(f"Ativo com o ticker {ticker} já cadastrado.")

    wait_key_to_continue()


def list_assets():
    assets = Asset.query.all()

    asset_table = PrettyTable(("ID", "Ticker", "Nome"))

    for asset in assets:
        asset_table.add_row((asset.id, asset.ticker, asset.name))

    return asset_table.get_string(sortby="ID"), assets


def list_all_assets():
    clear_console()

    assets_table, _ = list_assets()

    print("Listando todos os ativos cadastrados")
    print(assets_table)

    wait_key_to_continue()


def get_asset_by_id(asset_id, assets):
    filtred_assets = tuple(
        filter(lambda x: True if x.id == asset_id else False, assets)
    )

    if not filtred_assets:
        raise ValueError(f"ID not found in asset list")

    return filtred_assets[0]


def import_prices():
    clear_console()

    asset_table, assets = list_assets()

    print("Listando ativos")
    print(asset_table)

    while True:
        asset_id = get_input("Selecione o ID do Ativo para importar os preços: ", int)
        try:
            asset = get_asset_by_id(asset_id, assets)
            break
        except ValueError:
            continue

    start_date = get_input(
        "Selecione a data de inicio da importação (dd/mm/aaaa): ",
        lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"),
    )

    end_date = get_input(
        "Selecione a data final da importação ou nada para a data atual "
        "(dd/mm/aaaa): ",
        lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"),
        datetime.date.today(),
    )

    print("Importando preços, por favor aguarde...")
    asset.fetch_prices(start_date, end_date, save_to_db=True)
    print("Preços importados com sucesso!")
    wait_key_to_continue()


def calc_correlation():
    clear_console()

    asset_table, assets = list_assets()

    print("Listando ativos")
    print(asset_table)

    while True:
        asset_id = get_input("Selecione o ID do primeiro ativo para calcular: ", int)
        try:
            asset1 = get_asset_by_id(asset_id, assets)
            break
        except ValueError:
            continue

    while True:
        asset_id = get_input("Selecione o ID do segundo ativo para calcular: ", int)
        try:
            asset2 = get_asset_by_id(asset_id, assets)
            break
        except ValueError:
            continue

    asset1_df = pd.DataFrame.from_records(
        tuple(asset1.price_history.values()),
        index="date",
        columns=AssetPrice.attributes,
    )

    asset2_df = pd.DataFrame.from_records(
        tuple(asset2.price_history.values()),
        index="date",
        columns=AssetPrice.attributes,
    )

    correlation = asset1_df.close.corr(asset2_df.close)

    print(
        f"A correlação entre {asset1.name}({asset1.ticker}) e "
        f"{asset2.name}({asset2.ticker}) é {correlation}"
    )
    wait_key_to_continue()


def menu_loop():
    while True:
        clear_console()
        op = MainMenuOption(get_input(main_menu, int))

        match op:
            case MainMenuOption.EXIT:
                break
            case MainMenuOption.CREATE_ASSET:
                create_asset()
            case MainMenuOption.LIST_ASSETS:
                list_all_assets()
            case MainMenuOption.IMPORT_PRICE:
                import_prices()
            case MainMenuOption.CALC_CORRELATION:
                calc_correlation()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        menu_loop()
