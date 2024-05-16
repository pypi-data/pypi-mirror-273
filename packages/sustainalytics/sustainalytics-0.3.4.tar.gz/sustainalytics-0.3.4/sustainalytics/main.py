from api import API
import pandas as pd

# Access
client_id = 'f3706a19-ef03-4be7-8057-433155522583'
client_secret_key = 'TymCMY8J9Q]P9(-X7kq<s{BNpcdBNcn@'
# client_id = '51b4e3cb-5279-4e18-9109-adb81cff6080'
# client_secret_key = '{IK4q77qM*$c|a+Ae#q+aVYfPdg2T*3I'
con = API(client_id=client_id, client_secretkey=client_secret_key)


identifier_search = ['US914460WL04','US914460WL05',1264207945,'',1264207944]#,'US84055BAA17']
research_data = con.get_data(identifiers=identifier_search, productId=10, fieldIds=['101011112999'], dtype='dataframe', timestamps=False)

print(research_data)
# print(con.get_fieldDefinitions(time_series=True))
# print(con.get_fieldsInfo(dtype="dataframe"))
# print(con.get_fieldClusterInfo(dtype="dataframe"))
# print(con.get_packageInfo(dtype="dataframe"))
# print(con.get_productsInfo(dtype="dataframe"))
#con.get_fullFieldDefinitions(dtype="dataframe").to_csv("test_fullfielddefinitions.csv", index=False)
# print(con.get_fieldDefinitions(time_series=False, dtype="dataframe"))
# print(con.get_fieldDefinitions(time_series=True, dtype="dataframe"))
# print(con.get_fieldDefinitions(time_series=False, dtype="json"))
# print(con.get_fieldDefinitions(time_series=True, dtype="json")
# )
# print(con.get_fieldMappingDefinitions(time_series=False, dtype='dataframe'))
# print(con.get_fieldMappingDefinitions(time_series=True, dtype='dataframe'))
# print(con.get_fieldMappingDefinitions(time_series=False))
# print(con.get_fieldMappingDefinitions(time_series=True))

# print(con.get_fieldMappings(time_series=True, dtype='dataframe'))
# print(con.get_fieldMappings(time_series=False, dtype='dataframe'))
# print(con.get_fieldMappings(time_series=True, dtype='json'))
# print(con.get_fieldMappings(time_series=False, dtype='json'))

#
# full_field_definitions = con.get_fullFieldDefinitions(dtype='dataframe')
# print(full_field_definitions)

# print(con.get_data(identifiers=[1264207944], productId=19, dtype='dataframe'))
# test = con.get_time_series_data(identifiers=[1264207944, 1264207944, 1264207942], productId=70, dtype='dataframe')
# print(con.get_data(identifiers=[1264207944, 1264207944, 1264207942], productId=17, dtype='json', time_series=False))
# print(con.get_data(identifiers=[1264207944, 1264207944, 1264207942], productId=70, dtype='dataframe', time_series=True, timestamps=True))
# con.get_data(identifiers=[1264207944, 1264207944, 1264207942], productId=70, dtype='dataframe', time_series=True, timestamps=False).to_csv("test11.csv")
# con.get_data(identifiers=[1264207944, 1264207944, 1264207942], productId=70, dtype='dataframe', time_series=True, timestamps=True).to_csv("test2.csv")

# print(con.get_fieldDefinitions(dtype='dataframe')[['fieldId', 'fieldName']])
# print(con.get_fieldsInfo(dtype='dataframe', fieldIds=[101010112799, 101011112999]))
# print(con.get_productsInfo())
# print(con.get_universe_access(dtype='dataframe'))
# print(con.get_universe_entityIds())
