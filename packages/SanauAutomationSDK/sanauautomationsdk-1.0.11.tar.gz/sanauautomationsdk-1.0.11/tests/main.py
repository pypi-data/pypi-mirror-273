# from src.SanauAutomationSDK.Worker import Worker
# from src.SanauAutomationSDK.classes.DatabaseCredentials import DatabaseCredentials
# from src.SanauAutomationSDK.classes.ArmApiCredentials import ArmApiCredentials
# from src.SanauAutomationSDK.classes.OneSApiCredentials import OneSApiCredentials
# from src.SanauAutomationSDK.database.DB import DB
# # from src.SanauAutomationSDK.database.DB import db
# from src.SanauAutomationSDK.database.models.Job import Job
#
#
# db_creds = DatabaseCredentials(name='one_s', user='pbo_client', password='0efedb9xz', host='94.247.128.101', port='5432')
# arm_api_creds = ArmApiCredentials(country='KZ', domain='pbo.kz', access_key='7nuLUYDYeQLyd3Rn')
# ones_api_creds = OneSApiCredentials(login='Проверки', password='E123456k')
#
# db = DB('one_s', user='pbo_client', password='0efedb9xz', host='94.247.128.101', port='5432').db
# job_model = Job(db=db)
# job_class = job_model.__class__
#
# worker = Worker(job_class=job_class, arm_api_credentials=arm_api_creds)
# worker.run()

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from SanauAutomationSDK.api.Wrapper import Wrapper

api_wrapper = Wrapper('KZ', 'pbo.kz', '7nuLUYDYeQLyd3Rn')
data = {
    'file_vault_uuid': "34B62952-7898-408E-BC9A-08D10FD08B6F",
    'folder_name': "Оборотно-сальдовая ведомость/05.05.2024/",
    'file_name': "8f363db8-dea4-4fbd-8026-66d6ed05e53a_osv_current_year.xlsx",
}
print(api_wrapper.get_filevault_file(params=data))

# pbo_wrapper = Wrapper('KZ', 'pbo.kz', '7nuLUYDYeQLyd3Rn')
# print(pbo_wrapper.get_database(name='bagat'))
