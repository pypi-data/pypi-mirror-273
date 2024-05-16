import datetime
import requests
import re
import pandas as pd
import numpy as np
import itertools
from dateutil.relativedelta import relativedelta
from typing import Any, Union
from tqdm import tqdm


# pd.set_option('display.max_columns', None)
class API(object):
    """
    API manages connection and collection of Sustainalytics.

    Public Attributes
    -----------------
    client_id : str
        a special ID provided by sustainalytics to client for authentication and authorization
    client_secretkey : str
        a special key provided by sustainalytics to client for authentication and authorization
    access_headers : dict
        a dictionary managing the api tokens
    fieldIds : list
        a list of identifiers i.e. ISINs, CUSIPs, SEDOLs, Entity Ids(Sustainalytics).
    universe_of_access : dataframe/json
        a collection of EntityIds and universe the client can access.
    productIDs : list
        a list of productIds the client can access

    full_definition : dataframe/json
        a collection of the field definitions and more so product, package and cluster information

    Private Attributes
    ------------------
    __universe_entity_ids : list
        a list of entityIds the client can access

    Public Methods
    -----------------
    get_access_headers()
        returns the access and authorization token to the api.

    get_fieldIDs()
        :returns a list of fieldIds

    get_fieldsInfo(dtype=json)
        :returns a collection containing the fields information accessible to clients
    get_fieldDefinitions(dtype=json)
        :returns a collection of field definitions
    get_productIDs()
        :returns a list of product IDs
    get_productsInfo(dtype=json)
        :returns a collection of products information
    get_packageIDs()
        :returns a list of package IDs
    get_packageInfo(dtype=json)
        :returns a collection of package information
    get_fieldClusterIDs()
        :returns a list of field cluster IDs
    get_fieldClusterInfo(dtype=json)
        :returns a collection of field cluster information

    get_fieldMappings(dtype=json)
        :returns a collections of fieldId mappings to their descriptive information

    get_fieldMappingDefinitions(dtype=json)
        :returns a collection of the field mappings definitions.
    get_universe_access(dtype=json)
        :returns a collection of entity ids and universe access of an account
    get_universe_entityIDs(dtype=json)
        :returns a list of entityIds the client can access
    get_fullFieldDefinitions(dtype=json)
        :returns a collection of fieldDefinitions
    get_pdfReportService(dtype=json):
        :returns manages the pdf report generation.
    get_pdfReportInfo(dtype=json)
        :returns a collection of pdf information
    get_pdfReportUrl(identifier=None,reportId=None,dtype=json)
        :returns URL pdf link for an entityId and a reportId

    get_data(dtype=json)
        :returns a collections of sustainalytics data to the client.
    
    Private Methods
    --------------
    __process_fieldsdata(field):
        :returns a processed list of fieldIds
    --
    """

    def __init__(self, client_id: str, client_secretkey: str):
        """Initialize connection with the API with client id and client_secretkey.

        Args:
            client_id: The client id received from the Sustainalytics team.
            client_secretkey: The secret key for the id.
        """
        self.client_id = client_id
        self.client_secretkey = client_secretkey
        self.access_headers = self.get_access_headers()
        self.fieldIds = None
        self.universe_of_access = None
        self.__universe_entity_ids = None

    def get_access_headers(self) -> dict:
        """Get access token data.

        Returns:
            Access headers data.
        """
        try:
            access_token_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            }

            access_token_data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secretkey
            }

            access_token = requests.post('https://api.sustainalytics.com/auth/token', headers=access_token_headers,
                                         data=access_token_data,
                                         ).json()['access_token']

            access_headers = {
                'Accept': 'text/json',
                'Authorization': str('Bearer ' + access_token)}
            return access_headers
        except:
            raise ConnectionError('API Access Error: Please ensure the client_id and secret_key are valid else '
                                  'reach-out to your account manager for support')

    def get_fieldIds(self) -> list:
        """Gets the list of field ids that are activated for the client.

        Returns:
            List of field ids.
        """
        temp_data = self.get_fieldDefinitions(dtype='dataframe')

        if len(temp_data) > 0:
            return temp_data['fieldId'].tolist()
        else:
            return []

    def get_fieldsInfo(self, fieldIds: list = None, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Gets the description for the field ids activated for the client.

        Args:
            fieldIds: The list of fieldids to search.
            dtype: json or dataframe.

        Returns:
            The description of the field ids.
        """
        temp_data_general = self.get_fieldDefinitions(dtype='dataframe')
        temp_data_time_series = self.get_fieldDefinitions(time_series=True, dtype='dataframe')
        temp_data = pd.concat([temp_data_general, temp_data_time_series])
        temp_data = temp_data.reset_index(drop=True)

        if fieldIds is not None:
            temp_data = temp_data[temp_data['fieldId'].isin(fieldIds)].copy()
            temp_data = temp_data.reset_index(drop=True)

        if len(temp_data) > 0:
            if dtype == 'json':
                return pd.Series(temp_data['fieldName'].values, index=temp_data['fieldId']).to_dict()
            else:
                return temp_data[['fieldId', 'fieldName']]
        else:
            return {}

    def __get_request_data(self, endpoint_url: str, normalize: bool = False, dtype: str = 'json') -> Union[
        dict, pd.DataFrame]:
        """Gets the data from the specified endpoint url.

        Args:
            endpoint_url: Url to the API endpoint.
            normalize: A boolean value on whether to normalize the response or not.
            dtype: json or dataframe.

        Returns:
            The response in json or dataframe format.
        """
        if dtype == 'json':
            return requests.get(endpoint_url, headers=self.access_headers, timeout=60).json()
        if normalize:
            return pd.json_normalize(requests.get(endpoint_url, headers=self.access_headers, timeout=60).json())
        return pd.DataFrame(requests.get(endpoint_url, headers=self.access_headers, timeout=60).json())

    def get_request_with_authentication(self, endpoint_url: str, normalize: bool = False, dtype: str = 'json') -> Union[
        dict, pd.DataFrame]:
        """Makes a get request to the endpoint url. If authentication is expired, it authenticates again.

        Args:
            endpoint_url: Url to the API endpoint.
            normalize: A boolean value on whether to normalize the response or not.
            dtype: json or dataframe.

        Returns:
            The response in json or dataframe format.
        """
        try:
            result = self.__get_request_data(endpoint_url, normalize, dtype)
        except:
            self.access_headers = self.get_access_headers()
            result = self.__get_request_data(endpoint_url, normalize, dtype)
        return result

    def get_fieldDefinitions(self, time_series: bool = False, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Returns the field definitions either as a dataframe or json

        Args:
            time_series: A boolean value indicating whether to return time series data or not.
            dtype: json or dataframe

        Returns:
            Requested data in json or dataframe format.
        """
        if time_series:
            return self.get_request_with_authentication('https://api.sustainalytics.com/v2/TimeSeriesFieldDefinitions',
                                                        dtype=dtype)
        return self.get_request_with_authentication('https://api.sustainalytics.com/v2/FieldDefinitions', dtype=dtype)

    def get_productIds(self) -> list:
        """Gets the list of product ids activated for the client.

        Returns:
            The list of product ids.
        """
        temp_data = self.get_fieldMappings(dtype='dataframe')

        if len(temp_data) > 0:
            return temp_data['productId'].tolist()
        else:
            return []

    def get_productsInfo(self, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Gets info for the products.

        Args:
            dtype: json or dataframe

        Returns:
            Requested data in json or dataframe format.
        """
        temp_data_general = self.get_fieldMappings(dtype='dataframe')
        temp_data_general_time_series = self.get_fieldMappings(time_series=True, dtype='dataframe')
        temp_data = pd.concat([temp_data_general, temp_data_general_time_series]).reset_index(drop=True)

        if len(temp_data) > 0:
            if dtype == 'json':
                return pd.Series(temp_data['productName'].values, index=temp_data['productId']).to_dict()
            else:
                return temp_data[['productId', 'productName']]
        else:
            return {}

    def get_packageIds(self) -> list:
        """Gets a list of the package ids activated for the client id.

        Returns:
            List of package ids.
        """
        temp_data = self.get_fieldMappings(dtype='dataframe')
        temp_data = pd.DataFrame(list(itertools.chain.from_iterable(temp_data['packages'].tolist())))

        if len(temp_data) > 0:
            return temp_data['packageId'].tolist()
        else:
            return []

    def get_packageInfo(self, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Gets package info.

        Args:
            dtype: json or dataframe.

        Returns:
            Information about the packages in json or dataframe format.
        """
        temp_data_general = self.get_fieldMappings(dtype='dataframe')
        temp_data_general_time_series = self.get_fieldMappings(time_series=True, dtype='dataframe')
        temp_data = pd.concat([temp_data_general, temp_data_general_time_series]).reset_index(drop=True)
        temp_data = pd.DataFrame(list(itertools.chain.from_iterable(temp_data['packages'].tolist())))

        if len(temp_data) > 0:
            if dtype == 'json':
                return pd.Series(temp_data['packageName'].values, index=temp_data['packageId']).to_dict()
            else:
                return temp_data[['packageId', 'packageName']]
        else:
            return {}

    def get_fieldClusterIds(self) -> list:
        """Gets of list of the field cluster ids activated for the client.

        Returns:
            List of the field cluster ids.
        """
        temp_data = self.get_fieldMappings(dtype='dataframe')
        temp_data = pd.DataFrame(list(itertools.chain.from_iterable(temp_data['packages'].tolist())))
        temp_data = pd.DataFrame(list(itertools.chain.from_iterable(temp_data['clusters'].tolist())))

        if len(temp_data) > 0:
            return temp_data['fieldClusterId'].tolist()
        else:
            return []

    def get_fieldClusterInfo(self, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Gets information about the field clusters available for the client id.

        Args:
            dtype: json or dataframe.

        Returns:
            Information about the field clusters.
        """
        temp_data_general = self.get_fieldMappings(dtype='dataframe')
        temp_data_general_time_series = self.get_fieldMappings(time_series=True, dtype='dataframe')
        temp_data = pd.concat([temp_data_general, temp_data_general_time_series]).reset_index(drop=True)
        temp_data = pd.DataFrame(list(itertools.chain.from_iterable(temp_data['packages'].tolist())))
        temp_data = pd.DataFrame(list(itertools.chain.from_iterable(temp_data['clusters'].tolist())))

        if len(temp_data) > 0:
            if dtype == 'json':
                return pd.Series(temp_data['fieldClusterName'].values, index=temp_data['fieldClusterId']).to_dict()
            else:
                return temp_data[['fieldClusterId', 'fieldClusterName']]
        else:
            return {}

    def get_fieldMappings(self, time_series: bool = False, dtype='json') -> Union[dict, pd.DataFrame]:
        """Gets the field definitions (time series or not) either as a dataframe or json.

        Args:
            time_series: A boolean value indicating whether to return time series field mappings or not.
            dtype: json or dataframe

        Returns:
            The field definitions.
        """
        if time_series:
            return self.get_request_with_authentication('https://api.sustainalytics.com/v2/TimeSeriesFieldMappings',
                                                        normalize=True, dtype=dtype)
        return self.get_request_with_authentication('https://api.sustainalytics.com/v2/FieldMappings',
                                                    normalize=True, dtype=dtype)

    def get_fieldMappingDefinitions(self, time_series: bool = False, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Gets the field definitions.

        Args:
            time_series: A boolean value indicating whether to return time series field definitions or not.
            dtype: json or dataframe

        Returns:
            Field definitions.
        """
        if time_series:
            return self.get_request_with_authentication(
                'https://api.sustainalytics.com/v2/TimeSeriesFieldMappingDefinitions', dtype=dtype)
        return self.get_request_with_authentication(
            'https://api.sustainalytics.com/v2/FieldMappingDefinitions', dtype=dtype)

    def get_universe_access(self, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Get all the id of the companies in a universe.

        Args:
            dtype: json or dataframe.

        Returns:
            json or dataframe with all the identifiers in the universes.
        """
        try:
            if dtype == 'json':
                temp_data = requests.get('https://api.sustainalytics.com/v2/UniverseOfAccess',
                                         headers=self.access_headers, timeout=60).json()
            else:
                temp_data = pd.DataFrame(requests.get('https://api.sustainalytics.com/v2/UniverseOfAccess',
                                                      headers=self.access_headers, timeout=60).json())
        except:
            self.access_headers = self.get_access_headers()
            if dtype == 'json':

                temp_data = requests.get('https://api.sustainalytics.com/v2/UniverseOfAccess',
                                         headers=self.access_headers, timeout=60).json()
            else:
                temp_data = pd.DataFrame(requests.get('https://api.sustainalytics.com/v2/UniverseOfAccess',
                                                      headers=self.access_headers, timeout=60).json())
        return temp_data

    def get_universe_entityIds(self, keep_duplicates: bool = False) -> list:
        """Gets a list of company ids

        Args:
            keep_duplicates: A boolean value on whether to remove duplicates or not.

        Returns:
            A list with the entities.
        """
        self.universe_of_access = self.get_universe_access(dtype='dataframe')
        self.__universe_entity_ids = list(itertools.chain.from_iterable(self.universe_of_access['entityIds'].tolist()))
        if keep_duplicates is True:
            return self.__universe_entity_ids
        else:
            return list(set(self.__universe_entity_ids))

    # TODO: remove this
    def __process_fieldsdata(self, field) -> pd.DataFrame:
        """Does the processing on the fields data.

        Args:
            field:

        Returns:
            A new dataframe.
        """
        if not bool(field) or field is np.nan:
            self.fieldIds = self.get_fieldIds()
            fieldstr = [str(i) for i in self.fieldIds]
            self.fieldIds_default = dict.fromkeys(fieldstr, np.nan)
            return self.fieldIds_default
        else:
            return field

    @staticmethod
    def __process_definitions(value: int, src_df: pd.DataFrame, match_length: int, src_id_name: str):
        """Process the definition file.

        Args:
            value: The definition id.
            src_df: The dataframe file to lookup.
            match_length: The match length (e.g. 2, 4, 6)
            src_id_name: The id name.

        Returns:
            The id and the idname.
        """
        value_str = str(value)[:match_length]
        temp_df = src_df[src_df[src_id_name] == int(value_str)].copy()
        if len(temp_df) >= 1:
            return temp_df.iat[0, 0], temp_df.iat[0, 1]
        else:
            return None, None

    def get_fullFieldDefinitions(self, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Gets the complete field definitions.

        Args:
            dtype: json or dataframe.

        Returns:
            json or dataframe of the definition mapping for the fields.
        """
        field_info = self.get_fieldsInfo(dtype='dataframe')
        field_cluster = self.get_fieldClusterInfo(dtype='dataframe')
        packages = self.get_packageInfo(dtype='dataframe')
        products = self.get_productsInfo(dtype='dataframe')

        field_info['productId'], field_info['productName'] = zip(
            *field_info.apply(lambda x: self.__process_definitions(x['fieldId'], products, 2, 'productId'), axis=1))
        field_info['packageId'], field_info['packageName'] = zip(
            *field_info.apply(lambda x: self.__process_definitions(x['fieldId'], packages, 4, 'packageId'), axis=1))
        field_info['fieldClusterId'], field_info['fieldClusterName'] = zip(
            *field_info.apply(lambda x: self.__process_definitions(x['fieldId'], field_cluster, 6, 'fieldClusterId'),
                              axis=1))
        if dtype == 'json':
            return field_info.to_json(orient='records')
        else:
            return field_info

    def get_pdfReportService(self, productId: int = None, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Get the PDF reports accessible.

        Args:
            productId: The id of the product that you search for.
            dtype: json or dataframe.

        Returns:
            json or dataframe of the pdf reports.
        """
        if productId is None:
            raise ValueError('Please specify productId')
        if not isinstance(productId, int):
            raise ValueError('productId must be integer and have only one value per call')

        try:

            if dtype == 'json':
                temp_data = requests.get('https://api.sustainalytics.com/v2/ReportService',
                                         headers=self.access_headers, params=(('ProductId', productId),),
                                         timeout=60).json()
            else:
                temp_data = pd.DataFrame(requests.get('https://api.sustainalytics.com/v2/ReportService',
                                                      headers=self.access_headers, params=(('ProductId', productId),),
                                                      timeout=60).json())
                if temp_data.shape[0] == 0:
                    return {'Message': 'No available reports to show'}

        except:
            self.access_headers = self.get_access_headers()
            if dtype == 'json':

                temp_data = requests.get('https://api.sustainalytics.com/v2/ReportService',
                                         headers=self.access_headers, params=(('ProductId', productId),),
                                         timeout=60).json()
            else:
                temp_data = pd.DataFrame(requests.get('https://api.sustainalytics.com/v2/ReportService',
                                                      headers=self.access_headers, params=(('ProductId', productId),),
                                                      timeout=60).json())
                if temp_data.shape[0] == 0:
                    return {'Message': 'No available reports to show'}
        return temp_data

    def get_pdfReportUrl(self, identifier: int = None, reportId: int = None, dtype: str = 'json') -> Union[
        dict, pd.DataFrame]:
        """Returns the URL of a PDF report.

        Args:
            identifier: The company identifier.
            reportId: The id of the report.
            dtype: json or dataframe.

        Returns:
            json or dataframe of the PDF URL.
        """
        temp_data = pd.DataFrame()
        request_url = 'https://api.sustainalytics.com/v2/ReportService/url/'
        if identifier is not None and reportId is not None:
            request_url = request_url + str(identifier).strip(' \t\n') + "/" + str(reportId).strip(' \t\n')
            try:

                if dtype == 'json':
                    temp_data = requests.get(request_url,
                                             headers=self.access_headers, timeout=60).json()
                else:
                    temp_data = pd.DataFrame(requests.get(request_url,
                                                          headers=self.access_headers, timeout=60).json())

            except:
                self.access_headers = self.get_access_headers()
                if dtype == 'json':

                    temp_data = requests.get(request_url,
                                             headers=self.access_headers, timeout=60).json()
                else:
                    temp_data = pd.DataFrame(requests.get(request_url,
                                                          headers=self.access_headers, timeout=60).json())

            return temp_data
        else:
            return temp_data

    def get_pdfReportInfo(self, productId: int = None, dtype: str = 'json') -> Union[dict, pd.DataFrame]:
        """Returns the report IDs granted to the client id .

        Args:
            productId: The id of the product that you want to search.
            dtype: json or dataframe.

        Returns:
            json or dataframe with the reports and their type.
        """
        temp_data = self.get_pdfReportService(productId=productId, dtype='dataframe')
        if isinstance(temp_data, pd.DataFrame) and len(temp_data) > 0:
            temp_data = pd.DataFrame(list(itertools.chain.from_iterable(temp_data['reports'].tolist())))
            if dtype == 'json':
                return pd.Series(temp_data['reportType'].values, index=temp_data['reportId']).to_dict()
            else:
                return temp_data[['reportId', 'reportType']].drop_duplicates()
        else:
            return {'Message': 'Client has no pdf report access'}

    @staticmethod
    def __process_parameter_for_request(parameter_name: str, parameter_values: list = None,
                                        all_parameters_values: tuple = None) -> tuple:
        """Prepares a parameter to be added to the tuple with all the parameter values for the endpoint request.

        Args:
            parameter_name: Name of the parameter.
            parameter_values: Values given to the parameter.
            all_parameters_values: Tuple containing all the parameter data.

        Returns:
            The tuple with all parameter values with new parameter added to it.
        """
        if (parameter_values is not None) and (isinstance(parameter_values, list)) and (len(parameter_values) > 0):
            parameter_str = ','.join([str(elem) for elem in parameter_values])
            all_parameters_values = all_parameters_values + ((str(parameter_name), parameter_str),)
            return all_parameters_values
        elif (parameter_values is not None) and (
                isinstance(parameter_values, str) or isinstance(parameter_values, int)):
            all_parameters_values = all_parameters_values + ((str(parameter_name), parameter_values),)
            return all_parameters_values
        else:
            return all_parameters_values

    def __get_endpoint_data(self, params: tuple, extracted_data: Union[list, pd.DataFrame], dtype: str,
                            endpoint: str) -> Union[list, pd.DataFrame]:
        """Makes a GET request to the specified endpoint and returns it in the specified format.

        Args:
            params: Parameters for the request.
            extracted_data: Place where to store the data.
            dtype: json or dataframe.
            endpoint: endpoint to call.

        Returns:
            A json or a dataframe with the extracted data.
        """
        requests_url = requests.get(f"https://api.sustainalytics.com/v2/{endpoint}",
                                    headers=self.access_headers, params=params, timeout=180).json()
        if dtype == 'json':
            temp_data = requests_url
            extracted_data = extracted_data + temp_data
            return extracted_data
        else:
            if 'message' in requests_url:
                identifiers = re.findall(r"'(.*?)'", requests_url['message'])
                identifiers = identifiers[0].split(',')
                # Initialize list to store dictionaries
                identifiers_list = list()

                # Construct dictionary for each identifier
                for identifier in identifiers:
                    identifier_dict = {'identifier': identifier, 'status': {'matched': 'No', 'hasPermissions': False}}
                    identifiers_list.append(identifier_dict)
                temp_data = pd.DataFrame(identifiers_list)
                extracted_data = pd.concat([extracted_data, temp_data], ignore_index=True)
                return extracted_data

            temp_data = pd.DataFrame(requests_url)
            extracted_data = pd.concat([extracted_data, temp_data], ignore_index=True)
            return extracted_data

    def __make_request_to_endpoint(self, all_parameter_values: tuple, extracted_data: Union[list, pd.DataFrame],
                                   endpoint: str, dtype: str) -> Union[list, pd.DataFrame]:
        """Makes a request to a given V2 endpoint.

        Args:
            all_parameter_values: tuple containing all parameter data.
            extracted_data: place where to store the data from the request.
            endpoint: endpoint to make request to.
            dtype: json or dataframe.

        Returns:
            A json or a dataframe with the extracted data.
        """
        try:
            extracted_data = self.__get_endpoint_data(all_parameter_values, extracted_data, dtype, endpoint)
            return extracted_data
        except:
            self.access_headers = self.get_access_headers()
            extracted_data = self.__get_endpoint_data(all_parameter_values, extracted_data, dtype, endpoint)
            return extracted_data

    def __set_parameters(self, startdate: str = None, productId: int = None, packageIds: list = None,
                         fieldClusterIds: list = None, fieldIds: list = None, identifiers: list = None) -> tuple:
        """Gathers all the data from the parameters in order to combine them into a tuple.

        Args:
            startdate: Date filter for last changes query.
            productId: The product ID.
            packageIds: A list of package ids.
            fieldClusterIds: A list of field cluster ids.
            fieldIds: A list of field ids.
            identifiers: A list of security or company identifiers.

        Returns:
            A tuple with all the params ready to be passed for a request.
        """
        params = ()
        params = self.__process_parameter_for_request("StartDate", startdate, params)
        params = self.__process_parameter_for_request("productId", productId, params)
        params = self.__process_parameter_for_request("PackageIds", packageIds, params)
        params = self.__process_parameter_for_request("fieldClusterIds", fieldClusterIds, params)
        params = self.__process_parameter_for_request("fieldIds", fieldIds, params)
        params = self.__process_parameter_for_request("identifiers", identifiers, params)
        return params

    @staticmethod
    def __json_or_dataframe(dtype: str) -> Union[list, pd.DataFrame]:
        """Creates a list or a dataframe based on the input.

        Args:
            dtype: json or dataframe.

        Returns:
            A empty list or an empty dataframe.
        """
        if dtype == 'json':
            return []
        else:
            return pd.DataFrame()

    @staticmethod
    def __create_identifier_groups(identifiers: list, chunk_size: int) -> list:
        """Creates identifier groups of 10 when the number of elements in the identifiers list is >10.

        Args:
            identifiers: A list of security or company identifiers.
            chunk_size: The chunk size. 10 is the maximum value.

        Returns:
            A list of lists with the identifiers.
        """
        return [identifiers[i:i + chunk_size] for i in range(0, len(identifiers), chunk_size)]

    @staticmethod
    def __process_identifier_groups(identifiers: list) -> str:
        """Transforms the lists of identifiers into str values, strips them and puts a comma after each of them.

        Args:
            identifiers: The list of identifiers.

        Returns:
            The values from the list of identifiers as a string.
        """
        return ','.join([str(elem).strip() for elem in identifiers])

    @staticmethod
    def __check_date_format(self, date: str) -> None:
        """Checks whether the given date is in 'yyyy-mm-dd' format.

        Args:
            date: The date to check the format of.

        Raises:
            ValueError: if the date is in any other format.
        """
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except:
            raise ValueError(f"Incorrect date format, should be 'yyyy-mm-dd': {date}.")

    @staticmethod
    def __check_less_than_3_months_ago(date: str) -> None:
        """Checks whether the given date is more than 3 months ago, and raises an error if it is.

        Args:
            date: The date to check, in 'yyyy-mm-dd' format.

        Raises:
            ValueError: if the date is more than 3 months ago from current date.
        """
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        today = datetime.date.today()
        three_months_ago = today + relativedelta(months=-3)
        if date < three_months_ago:
            raise ValueError('The date entered is more than 3 months ago.')

    @staticmethod
    def __check_type(arg_name: str, actual_values, expected_type) -> None:
        """Checks values to see if their actual type matches the expected one.

        Args:
            actual_values: The values to check the type of.
            expected_type: Expected type of the values.

        Raises:
            TypeError: if the expected type is different from the current type.
        """
        if not isinstance(actual_values, expected_type):
            raise TypeError(
                f"Expected {expected_type.__name__} for {arg_name}, but got {type(actual_values).__name__} instead.")

    @staticmethod
    def __check_possible_existence_type(arg_name: str, actual_values: Any, expected_type: Any) -> None:
        """Checks whether there are any actual values. If there are their actual type will be compared to the expected
        type.

        Args:
            actual_values: The values to check the type of.
            expected_type: Expected type of the values.

        Raises:
            TypeError: if the expected type is different from the current type.
        """
        if actual_values is not None:
            if not isinstance(actual_values, expected_type):
                raise TypeError(
                    f"Expected {expected_type.__name__} for {arg_name}, but got {type(actual_values).__name__} instead.")

    @staticmethod
    def __check_greater_than(arg_name: str, actual_value: int, comparison_value: int) -> None:
        """Checks whether the values of an argument are bigger than a provided value.

        Args:
            actual_value: The value given in the function call.
            comparison_value: The value to compare with.

        Raises:
            ValueError: if the actual value is smaller than the expected one.
        """
        if not actual_value > comparison_value:
            raise ValueError(f"{actual_value} must be bigger than {comparison_value} for {arg_name}.")

    @staticmethod
    def __check_less_than(arg_name: str, actual_value: int, comparison_value: int) -> None:
        """Checks whether the values of an argument are smaller than a provided value.

        Args:
            actual_value: The value given in the function call.
            comparison_value: The value to compare with.

        Raises:
            ValueError: if the actual value is bigger than the expected one.
        """
        if not actual_value < comparison_value:
            raise ValueError(f"{actual_value} must be smaller than {comparison_value} for {arg_name}.")

    @staticmethod
    def __check_is_value_valid(arg_name: str, actual_value: str, valid_values: list) -> None:
        """Checks whether the actual value is in the list of valid values.

        Args:
            actual_value: The value given in the function call.
            valid_values: The possible values.

        Raises:
            ValueError: If the actual value is not present in the valid values list.
        """
        if actual_value not in valid_values:
            raise ValueError(
                f"{actual_value} is not a valid value for {arg_name}. Valid values are: {', '.join(valid_values)}.")

    @staticmethod
    def __check_list_not_empty(arg_name: str, actual_values: list) -> None:
        """Checks whether a list is empty. Throws a ValueError if it is.

        Args:
            arg_name: Name of the argument.
            actual_values: The list to check if it's empty or not.

        Raises:
            ValueError: if list is empty.
        """
        if not actual_values:
            raise ValueError(f"The list of {arg_name} must contain at least 1 value.")

    def __get_LastChangesSince_validations(self, startdate: str, productId: int, identifiers: list, packageIds: list,
                                           fieldClusterIds: list, fieldIds: list, dtype: str) -> None:
        """Validation checks for the get_LastChangesSince function.

        Args:
            startdate: Date filter for last changes query. Can retrieve data only for last 3 months from current date.
            productId: The product ID. Only one value allowed.
            identifiers: A list of security or company identifiers.
            packageIds: A list of package ids.
            fieldClusterIds: A list of field cluster ids.
            fieldIds: A list of field ids.
            dtype: json or dataframe.
        """
        self.__check_type("startdate", startdate, str)
        self.__check_date_format(startdate)
        self.__check_less_than_3_months_ago(startdate)
        self.__check_type("productId", productId, int)
        self.__check_possible_existence_type("identifiers", identifiers, list)
        self.__check_possible_existence_type("packageIds", packageIds, list)
        self.__check_possible_existence_type("fieldClusterIds", fieldClusterIds, list)
        self.__check_possible_existence_type("fieldIds", fieldIds, list)
        self.__check_is_value_valid("dtype", dtype, ['json', 'dataframe'])

    def get_LastChangesSince(self, startdate: str, productId: int, identifiers: list = None, packageIds: list = None,
                             fieldClusterIds: list = None, fieldIds: list = None, dtype: str = 'json') -> Union[
        list, pd.DataFrame]:
        """Make an API request to the LastChangesSince endpoint with the given parameters and return the response.

        Args:
            startdate: Date filter for last changes query. Can retrieve data only for last 3 months from current date.
            productId: The product ID. Only one value allowed.
            identifiers: A list of security or company identifiers.
            packageIds: A list of package ids.
            fieldClusterIds: A list of field cluster ids.
            fieldIds: A list of field ids.
            dtype: json or dataframe.
            bigger than the chunk size, then the number of API calls to the endpoint would be equal to the number of
            identifiers/chunk size.

        Returns:
            A json or a dataframe representing the response from the v2 endpoint LastChangesSince of the API.
        """

        self.__get_LastChangesSince_validations(startdate, productId, identifiers, packageIds, fieldClusterIds,
                                                fieldIds, dtype)

        extracted_data = self.__json_or_dataframe(dtype)

        if (identifiers is not None) and len(identifiers) > 10:
            identifier_groups = self.__create_identifier_groups(identifiers, chunk_size=10)
            for i, id_group_list in enumerate(identifier_groups):
                params = self.__set_parameters(startdate, productId, packageIds, fieldClusterIds, fieldIds,
                                               id_group_list)

                extracted_data = self.__make_request_to_endpoint(params, extracted_data, "LastChangesSince", dtype)
        else:
            params = self.__set_parameters(startdate, productId, packageIds, fieldClusterIds, fieldIds, identifiers)
            extracted_data = self.__make_request_to_endpoint(params, extracted_data, "LastChangesSince", dtype)
        return extracted_data

    def __get_data_validations(self, identifiers: list, productId: int, packageIds: list, fieldClusterIds: list,
                               fieldIds: list, dtype: str, time_series: bool, timestamps: bool,
                               use_progressbar: bool) -> None:
        """ Validation checks for the get_data function.

        Args:
            identifiers: A list of security or company identifiers separated by comma.
            productId: The product ID.
            packageIds: A list of package ids separated by comma.
            fieldClusterIds: A list of field cluster ids separated by comma.
            fieldIds: A list of field ids separated by comma.
            dtype: json or dataframe.
            time_series: A boolean value indicating whether to return time series data or not.
            timestamps: A boolean value indicating whether to return data with timestamps or not.
            use_progressbar: A boolean value indicating whether to show a progress bar or not during the function call.
        """
        self.__check_type("productId", productId, int)
        self.__check_type("identifiers", identifiers, list)
        self.__check_list_not_empty("identifiers", identifiers)
        self.__check_type("timestamps", timestamps, bool)
        self.__check_type("use_progressbar", use_progressbar, bool)
        self.__check_type("time_series", time_series, bool)
        self.__check_is_value_valid("dtype", dtype, ['json', 'dataframe'])
        self.__check_possible_existence_type("packageIds", packageIds, list)
        self.__check_possible_existence_type("fieldClusterIds", fieldClusterIds, list)
        self.__check_possible_existence_type("fieldIds", fieldIds, list)

    def get_data(self, identifiers: list, productId: int, packageIds: list = None, fieldClusterIds: list = None,
                 fieldIds: list = None, dtype: str = 'json', time_series: bool = False,
                 timestamps: bool = False, use_progressbar: bool = True) -> Union[list, pd.DataFrame]:
        """Get normal data or time series data with or without timestamps via sustainalytics API.

        Args:
            identifiers: A list of security or company identifiers separated by comma.
            productId: The product ID.
            packageIds: A list of package ids separated by comma.
            fieldClusterIds: A list of field cluster ids separated by comma.
            fieldIds: A list of field ids separated by comma.
            dtype: json or dataframe.
            time_series: A boolean value indicating whether to return time series data or not.
            timestamps: A boolean value indicating whether to return data with timestamps or not.
            use_progressbar: A boolean value indicating whether to show a progress bar or not during the function call.

        Returns:
            The data in json or dataframe format.
        """
        self.__get_data_validations(identifiers, productId, packageIds, fieldClusterIds, fieldIds, dtype, time_series, timestamps, use_progressbar)

        data_pull = self.__json_or_dataframe(dtype)

        if len(identifiers) > 10:
            identifiers = self.__create_identifier_groups(identifiers, chunk_size=10)
        else:
            identifiers = [identifiers]

        with tqdm(total=len(identifiers), disable=not use_progressbar) as pbar:
            for i, id_group_list in enumerate(identifiers):
                params = self.__set_parameters(productId=productId, packageIds=packageIds,
                                               fieldClusterIds=fieldClusterIds,
                                               fieldIds=fieldIds, identifiers=id_group_list)
                if time_series & timestamps:
                    data_pull = self.__make_request_to_endpoint(params, data_pull, "TimeSeriesDataWTimestamps", dtype)
                elif time_series & (~timestamps):
                    data_pull = self.__make_request_to_endpoint(params, data_pull, "TimeSeriesData", dtype)
                elif (~time_series) & timestamps:
                    data_pull = self.__make_request_to_endpoint(params, data_pull, "DataServiceWTimestamps", dtype)
                else:
                    data_pull = self.__make_request_to_endpoint(params, data_pull, "DataService", dtype)
                pbar.update(1)
        return data_pull
