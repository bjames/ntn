import requests

from csv import reader
from sqlalchemy.exc import OperationalError, IntegrityError

from config import OUI_FILES
from ntn_models import OUI_MAL, OUI_MAM, OUI_MAS, OUI_CID, OUI_IAB
from ntn_db import db_session, init_db


def clear_tables():

    try:

        Session = db_session()

        Session.query(OUI_MAL).delete()
        Session.query(OUI_MAM).delete()
        Session.query(OUI_MAS).delete()
        Session.query(OUI_CID).delete()
        Session.query(OUI_IAB).delete()


        Session.commit()

    # Tables do not exist, we initiate them
    except OperationalError:

        init_db()


def update_table(oui_csv, table_name):

    Session = db_session()

    next(oui_csv)

    for row in oui_csv:


        if table_name == 'OUI_MAL':

            Session.add(OUI_MAL(row[1], row[2], row[3]))
            Session.commit()

        elif table_name == 'OUI_MAM':

            Session.add(OUI_MAM(row[1], row[2], row[3]))
            Session.commit()

        elif table_name == 'OUI_MAS':

            Session.add(OUI_MAS(row[1], row[2], row[3]))
            Session.commit()

        elif table_name == 'OUI_CID':

            Session.add(OUI_CID(row[1], row[2], row[3]))
            Session.commit()

        elif table_name == 'OUI_IAB':

            Session.add(OUI_IAB(row[1], row[2], row[3]))
            Session.commit()

def download_oui_lists():

    clear_tables()

    for oui_file in OUI_FILES:

        response = requests.get(oui_file['url'])

        if response.status_code == 200:

            oui_csv = reader(response.text.splitlines())

            update_table(oui_csv, oui_file['table_name'])


if __name__ == "__main__":

    download_oui_lists()