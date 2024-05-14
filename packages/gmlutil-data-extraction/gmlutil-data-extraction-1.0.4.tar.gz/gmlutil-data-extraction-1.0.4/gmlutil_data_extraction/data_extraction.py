# from pandas.core.strings import str_count
import boto3
import geopandas as gpd
import hana_ml
import io
import json
import numpy as np
import pandas as pd
import pymssql
import oracledb
import redshift_connector
import sqlalchemy as sa
import sys
import time

from gmlutil_data_extraction import config as conf
from fuzzywuzzy import fuzz
from pytrends.request import TrendReq
from sqlalchemy import create_engine, Table, MetaData
from types import SimpleNamespace

limit = np.int64(10**9 * 2.1)
sys.setrecursionlimit(limit)

run_mode = "cloud"
if run_mode == "local":
    path_to_folder = '../'
    sys.path.append(path_to_folder)
    import credentials as cred
else:
    def credf(keys):
        client = boto3.client('secretsmanager', region_name = conf.secretsm_region)
        if keys == "redshift":
            response = client.get_secret_value(SecretId=conf.secretsm_redshift_keys)
            database_secrets = json.loads(response['SecretString'])
            cred = SimpleNamespace(**database_secrets)
        else:
            response = client.get_secret_value(SecretId=conf.secretsm_master_keys)
            database_secrets = json.loads(response['SecretString'])
            cred = SimpleNamespace(**database_secrets)
        return cred
    cred = credf('master')
    credr = credf('redshift')


########################### Data Extraction ###########################
class data_extraction:
    def __init__(self, dsrc='general', type_=None, dist=None):
        #type_ is if you want it to be at the subcategory level specify 'sub'
        self.type_ = type_
        #dist is if you want it to be 'sgws' you specify sgws
        self.dist = dist
        self.dsrc = dsrc

    
    def aws_connection(self, aws_client='s3'):
        client_conn = boto3.client(aws_client, 
            region_name = cred.AWS_REGION_NAME,
            aws_access_key_id = cred.AWS_ACCESS_KEY,
            aws_secret_access_key = cred.AWS_SECRET_KEY
            )
        return client_conn
    

    def hana_connection(self):
        conn = hana_ml.dataframe.ConnectionContext(
            address= cred.HANA_ADDRESS,
            port=cred.HANA_PORT,
            user=cred.HANA_USER,
            password=cred.HANA_PASSWORD
            )
        return conn


    def irigco_connection(self):
        conn = pymssql.connect(server = cred.GCO_SERVER, # 'lv1sqlprdwdb02', 
                            user=cred.GCO_USERNAME, 
                            password = cred.GCO_PASSWORD, 
                            database = cred.GCO_DATABASE, # 'IRIGCO', 
                            port = cred.GCO_PORT) # 61433)
        return conn


    def rs_connection(self):
        engine_string = 'redshift+psycopg2://{}:{}@{}'.format(credr.username, credr.password, credr.host + ":" + credr.port + "/" + credr.dbName)
        conn = create_engine(engine_string)
        return conn

    
    def get_category(self, sub, cat):
        if self.dsrc == 'sgws':
            if sub in ['SPARKLING WINE']:
                return 'SPARKLING WINE'
            elif cat == 'WINE':
                return "TABLE WINE"
            else:
                return cat
        else:
            if ('SPARKLING' in sub) or ('LAMBRUSCO' in sub):
                return 'SPARKLING WINE'
            elif sub  == 'LIQUOR':
                return cat
            elif sub == 'SELTZER':
                return cat
            else:
                return 'TABLE WINE'


    ### NEED TO READ IN STUFF FROM S3 
    def read_from_s3_acv(self, state='all'):
        if self.dsrc == 'sgws':
            if state == 'all':
                print('Getting all accounts from SGWS, may take longer to pull')
                df = self.read_from_rs(f"select * from prophet.sgws_account_segmentation_raw", conn)
            else:
                df = self.read_from_rs(f"select * from prophet.sgws_account_segmentation_raw where \"Acct_State\" = '{state}'", conn)
            df['sub_category']= df['sub_category'].str.upper()
            df['account_id'] = df['account_id'].astype(str).str.strip('.0')
            df['tier'] = np.where((df['tier'] == 'TIER 7') | (df['category'] == 'TEQUILA'),'TIER 6',df['tier'])
            df['tier'] = np.where((df['tier'] == 'TIER 7') | (df['category'] == 'RUM'),'TIER 6',df['tier'])
            df['category'] = df.apply(lambda x:self.get_category(x.sub_category, x.category), axis=1)
            cols = ['account_id', 'account_name', 'acct_city', 'acct_state', 'category',
           'sub_category', 'sales_type', 'tier', 'key_acct_zone', 'key_acct_group']
            aggs = {i:'sum' for i in ['eq_volume_percent_wine', 'physical_volume_percent_wine',
                   'net_list_dollars_percent_wine', 'eq_volume_percent_spirits',
                   'physical_volume_percent_spirits', 'net_list_dollars_percent_spirits']}
            #need to groupby here because SGWS seperated out two tiers in spirts that should be tier 6
            output_df = df.groupby(cols,as_index=False).agg(aggs)
        else:
            #state all is default for bring in all distributors
            if state == 'all':
                print('Getting all accounts, may take longer to pull')
                conn = self.rs_connection()
                #we are going to query for the all distinct states in the dataframe
                state_df = self.read_from_rs(f"select distinct(acct_state) from prophet.account_segmentation_raw", conn)
                dfs =  []
                #for each state in the data frame loop through these and get the data corresponding to it
                for state in tqdm(state_df['acct_state'].unique()):
                    output_df = self.read_from_rs(f"select * from prophet.account_segmentation_raw where \"Acct_State\" = '{state}'", conn)
                    dfs.append(output_df)
                output_df = pd.concat(dfs)
            else:
                #if you select an individual state we query that individual state
                output_df = self.read_from_rs(f"select * from prophet.account_segmentation_raw where \"Acct_State\" = '{state}'", conn)
            #doing some data cleansing here
            output_df['sub_category']= output_df['sub_category'].str.upper()
            output_df['account_id'] = output_df['account_id'].astype(str).str.strip('.0')
            output_df['net_list_dollars'] = output_df['net_list_dollars'].astype(float)
            #renaming our categorys so sparkling and table wine are seperated...this matches to what we want to merge later down the line 
            output_df['category'] = output_df.apply(lambda x: self.get_category(x.sub_category, x.category), axis=1)
        return output_df


    #nl function norm creates the nl running percent functions(the acv curve creations)
    def nl_function(self, output_df, df, cols, cat):
        if self.dsrc == 'sgws':
            if (cat == 'spirits') or (self.type_ == 'sub'):
                cols = ['acct_state','category','sub_category','sales_type','tier']
            if cat == 'wine':
                df = df.groupby(['account_id', 'account_name', 'acct_city']+cols+['key_acct_zone', 'key_acct_group'],as_index=False).agg({f'net_list_dollars_percent_{cat}':'sum'})
            df['sum_cat'] = df.groupby(cols,as_index=False)[f'net_list_dollars_percent_{cat}'].transform('sum')
            df = df[df['sum_cat'] != 0]
            df['nl_percent'] = df[f'net_list_dollars_percent_{cat}']/df['sum_cat']
            df['nl_percent'] = pd.to_numeric(df['nl_percent'])
            df = df.sort_values(cols+['nl_percent'],ascending=False)
            df['nl_running_percent'] = df.groupby(cols)['nl_percent'].transform('cumsum')
            curves = df[['account_id','account_name','acct_city','key_acct_zone','key_acct_group']+cols+['nl_percent','nl_running_percent']]
        else:
            if self.type_ == 'sub':
                #if you select 'sub' in creating the object we are going to run the acv curves based off of that sub category selection
                cols =['acct_state','category','sub_category','sales_type','tier']
            print('running curves function...')
            #sum for the aggregation of columns
            df['sum_cat'] = df.groupby(cols)[f'net_list_dollars'].transform('sum')
            #percent of total you are worth for the column level
            df['nl_percent'] = df[f'net_list_dollars']/df['sum_cat']
            df['nl_percent'] = pd.to_numeric(df['nl_percent'])
            df = df.sort_values(cols+['nl_percent'],ascending=False)
            #nl running percent which creates our acv curves here...
            df['nl_running_percent'] = df.groupby(cols)['nl_percent'].transform('cumsum')
            # df = df[['account_id','account_name','acct_city','key_acct_zone','key_acct_group']+cols+['nl_percent','nl_running_percent','net_list_dollars']]
            merger = output_df[['account_id','account_name','acct_state','acct_city','acct_zip','key_acct_zone','key_acct_group']].drop_duplicates(subset = ['account_id','acct_state','acct_city'])
            merged = df.merge(merger, on = ['account_id','acct_state','acct_city'],how='left')
            curves = merged[['account_id','account_name','acct_city','key_acct_zone','key_acct_group']+cols+['nl_percent','nl_running_percent','net_list_dollars']]
        return curves


    def acv_curves_calc(self, output_df):
        if self.dsrc == 'sgws':
            spirits = output_df[output_df['category'] == 'SPIRITS']
            wine = output_df[output_df['category'].isin(['TABLE WINE','SPARKLING WINE'])]
            df_dict = {'wine':wine,'spirits':spirits}
            cols = ['acct_state','category','sales_type','tier']
            output =[]
            for k, v in tqdm(df_dict.items()):
                output.append(self.nl_function(output_df, v, cols, k))
            all_curves = pd.concat(output)
            all_curves['category'] = np.where(all_curves['category'] == 'SPIRITS',all_curves['sub_category'],all_curves['category'])
            if self.type_ != 'sub':
                all_curves.drop('sub_category',axis=1,inplace=True)
            all_curves = all_curves.drop_duplicates()
            all_curves_final = all_curves
        else:
            cols =['acct_state', 'category', 'sales_type', 'tier']
            #we are going to group this data together because it is easier 
            if self.type_ == 'sub':
                grouped =  output_df.groupby(['account_id','acct_state','acct_city','category','sub_category','sales_type','tier'],as_index=False).agg({'net_list_dollars':'sum'})
            else:
                grouped =  output_df.groupby(['account_id','acct_state','acct_city','category','sales_type','tier'],as_index=False).agg({'net_list_dollars':'sum'})
            wine = grouped[grouped['category'] == 'TABLE AND SPARKLING WINE']
            spirits =  grouped[grouped['category'] != 'TABLE AND SPARKLING WINE']
            run_dict = {'wine':wine,'spirits':spirits}
            output = []
            for k, v in run_dict.items():
                print(k)
                all_curves = self.nl_function(output_df, v, cols, k)
                all_curves = all_curves.drop_duplicates()
                output.append(all_curves)
            all_curves = pd.concat(output)
            all_curves_final = all_curves[all_curves['account_id']!='']
        return all_curves_final


    # # READING IN ACV DATA
    # def read_from_acv_s3(self, bucket_name=cred.S3_BUCKET, file_name=cred.benchmark_acv_str, geofile_name=cred.benchmark_geo_str, fuzz_ratio=90, state_choice1=['New Mexico','New_Mexico'], state_choice2=['DC','District of Columbia']):
    #     """gets our acv curves from s3 in order to run the distributor path option for upcs
    #     Returns:
    #          df: acv_df is the accounts with the respective net list running percent for each category and tier 
    #     """ 
    #     acv_df = self.read_from_s3(bucket_name, file_name)
    #     columns = ['9L VOLUME','PHYS VOLUME','NET LIST DOLLARS']
    #     for column in columns:
    #         acv_df[column] = round(acv_df[column],2)
    #     columns = ['nl_percent','nl_running_percent']
    #     for column in columns:
    #         acv_df[column] = round(acv_df[column],4)
    #     acv_df['Rtl_Acct_ID'] = acv_df['Rtl_Acct_ID'].astype(int)
    #     acv_df['geoCode'] = acv_df['geoCode'].astype(str)
    #     acv_df['concat'] = acv_df['Mkt_Grp_State'] + ' ' + acv_df['Acct_City']
    #     acv_df['concat'] = acv_df['concat'].astype(str)
    #     unique_citystates = acv_df[['Mkt_Grp_State','Acct_City','concat']].drop_duplicates()
    #     # Read in geocodes and fuzzy match them--> need to do ts cause some cities have different spellings from the hana side
    #     geo_codes = self.read_from_s3(bucket_name, geofile_name)
    #     geo_codes['concat'] =geo_codes['Mkt_Grp_State'] + ' ' + geo_codes['City']
    #     matchers = {}
    #     for j in unique_citystates['concat']:
    #         for i in geo_codes['concat']:
    #             if (j[:2] == i[:2]):
    #                 if fuzz.ratio(i,j) > fuzz_ratio:
    #                     matchers[j] = i
    #     acv_df['new_concat'] = acv_df['concat'].map(matchers)
    #     acv_df_new = acv_df.merge(geo_codes[['geoCode','concat']],left_on = 'new_concat',right_on = 'concat',how='left')
    #     acv_df_new['new_concat'] = acv_df_new['new_concat'].astype(str)
    #     acv_df_new = acv_df_new.drop(['geoCode_x','concat_x','concat_y','new_concat','geoCode_x'],axis = 1)
    #     acv_df_new = acv_df_new.rename(columns = {'geoCode_y':'geoCode'})
    #     acv_df_new['geoCode'] =acv_df_new['geoCode'].astype(str)
    #     acv_df_new['State'] = np.where(acv_df_new['State'] in state_choice1, acv_df_new['State'])
    #     acv_df_new['State'] = np.where(acv_df_new['State'] in state_choice2, acv_df_new['State'])
        # return acv_df_new


    def read_from_ocdb(self, sql, host='oradb07.est1933.com', port=2001, service_name='db07.est1933.com'):
        dsn_conn = oracledb.makedsn(host, port, service_name=service_name)
        conn = oracledb.connect(user=cred.ORACLE_USERID, password=cred.ORACLE_PASSWORD, dsn=dsn_conn, encoding='ISO-8859-1')
        df_ora = pd.read_sql(sql, con=conn)
        conn.close()
        return df_ora


    # PYTRENDS FUNCTION THAT GETS TRENDING CITIES BASED ON KEYWORD(BRAND)
    def read_from_gcity(self, keyword, hl='en-US', cat='71', geo='US', gprop='', timeframe='today 3-m', resolution='DMA', inc_low_vol=True, inc_geo_code=True, num_keywords=30):
        """generates the google trends piece from a keyword that is entered(benchmark)
        Args:
            keyword (str): planning brand that is entered in order to generate city list
        Returns:
            df: cities that are trending for the keyword
        """
        print('gathering google trends data')
        pytrends = TrendReq(hl=hl)
        # Building our payload for the trends query
        keywords = [keyword]
        # Pytrends function to get google data
        pytrends.build_payload(keywords, cat, timeframe, geo,gprop)
        try:
            output= pytrends.interest_by_region(resolution=resolution, inc_low_vol=inc_low_vol, inc_geo_code=inc_geo_code)
            city_queries = output[output[keywords[0]] > num_keywords]
            city_queries['Google'] = 'Y'
            city_queries = city_queries[['geoCode','Google']]
        except:
            city_queries = pd.DataFrame([], columns=['geoCode','Google'])
        time.sleep(1)
        return city_queries

    
    def read_from_geo_s3(self, bucket_name, file_name=cred.geospatial_str): 
        nav_county_polys = self.read_from_s3(bucket_name, file_name)
        nav_county_polys['geometry'] = gpd.GeoSeries.from_wkt(nav_county_polys['geometry'])
        nav_county_polys = gpd.GeoDataFrame(nav_county_polys, geometry = 'geometry',crs='EPSG:4326')
        return nav_county_polys
    

    def read_from_mssql(self, sql):
        conn = self.mssql_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        return df

    
    def read_from_rs(self, sql, conn):
        rs_connect = self.rs_connection()
        query = sa.text(sql)
        rs = rs_connect.execute(query)
        df = pd.DataFrame(rs.fetchall())
        df.columns = rs.keys()
        rs_connect.dispose()
        return df

    # def read_from_rs(self, table_name, schema_name=credr.dbName):
    #     metadata = MetaData()
    #     conn = self.rs_connection()
    #     dt = Table(table_name, metadata, autoload=True, autoload_with=conn, schema=schema_name)
    #     df_columns = dt.columns.keys()
    #     return dt, conn, df_columns

    
    def read_from_s3(self, bucket_name, file_name, encoding='utf8', low_memory=False, dtypes = None, file_type='csv'):
        s3c = self.aws_connection()
        KEY = '{}'.format(file_name)
        obj = s3c.get_object(Bucket=bucket_name, Key = KEY)
        data = obj['Body'].read()
        if file_type == 'csv':                         
            df = pd.read_csv(io.BytesIO(data) , encoding=encoding, low_memory=low_memory, dtype = dtypes) # , on_bad_lines='skip')
        elif file_type == 'xlsx':
            df = pd.read_excel(io.BytesIO(data), engine='openpyxl')
        return df
    
    
    # GETTING OUR UPCS DF WCH CONTAINS CATEGORY AND PRICE TIER FOR INDIVIDUAL ITEMS
    def read_from_upc_s3(self, bucket_name=cred.S3_BUCKET, file_name=cred.upc_tier_str):
        """gets our upc df: a dataframe with all upcs and thier corresponding price tier and category
        Returns:
            [df]: [upc_df is all upcs and their corresponding price tier and category: to be merged onto acv df]
        """
        upc_df = self.read_from_s3(bucket_name, file_name)
        # Add leading zeros to UPC to match Gallo data
        upc_df['UPC'] = upc_df['UPC'].astype(int).astype(str).str.rjust(12, "0")
        return upc_df


    def upload_to_rs(self, bucket_name, file_name, table_name=credr.winegrowing_table, host = credr.winegrowing_host, database = credr.winegrowing_database, user = credr.winegrowing_user, password = credr.winegrowing_password): # prophet/Deployment/DS_Collab/winegrowing_research/GQI/model_outputs/gqi_calc.csv
        rs_push_query = """call """ + table_name + """.copy_gqi_calc('s3://"""+ bucket_name + """/""" + file_name + """')"""
        conn_redshift = redshift_connector.connect(
            host = host,
            database = database,
            user = user,
            password = password
        )
        cursor = conn_redshift.cursor()
        cursor.execute(rs_push_query)
        conn_redshift.commit()
        conn_redshift.close()
        cursor.close()
        print("Successfully pushed to Redshift.")    
    

    def upload_to_s3(self, df, bucket_name, file_name, index=False, file_type='csv'):
        s3c = self.aws_connection()
        KEY = '{}'.format(file_name)
        if file_type == 'csv':
            df.to_csv('buffer', index=index)
            s3c.upload_file(Bucket = bucket_name, Filename = 'buffer', Key = KEY)
        elif file_type == 'xlsx':
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer)
            data = buffer.getvalue()
            s3c.put_object(Bucket=bucket_name, Key=KEY, Body=data)
            writer.close()
        print("Uploading is successful...")



