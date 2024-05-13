import json
from datetime import datetime
from dbCode.directDBOperation import insertDataIntoDatabase, fetchDataInDatabase, updatetBulkDataInDatabaseByCopyManager, insertBulkDataIntoDatabaseByCopyManager, insertBulkDataIntoDatabase
from psycopg2 import sql

def POST(connection, schema, tableName:str, data:dict, onConflict:bool=False, uniqueColumnNamesForConflict:str='id'):
    # TODO: Check if any column is not nullable that does not appear in data. Return ERROR in this case
    data['created_at'] = int(datetime.now().timestamp())
    data['modified_at'] = int(datetime.now().timestamp())
    columns = data.keys()
    onConflictString = ''
    if onConflict:
        onConflictString = 'ON CONFLICT ({}) DO NOTHING'.format(uniqueColumnNamesForConflict)
    queryString = "INSERT INTO {{}}.{} ({}) VALUES ({}) {};".format(tableName,', '.join(columns),','.join(['%s']*len(columns)),onConflictString)

    params = []
    for key in data:
        if type(data[key]) == dict or type(data[key]) == list:
            params.append(json.dumps(data[key]))
        else:
            params.append(data[key])

    query = sql.SQL(queryString).format(sql.Identifier(schema))
    result = insertDataIntoDatabase(query, params, connection)    
    return result

def POST_BULK(connection, schema, tableName:str, data:list, byCopy = True, onConflict:bool=False, uniqueColumnNamesForConflict:str='id'):
    '''
    data must be list of diictionaries. Key is column name according to database!
    '''
    query = sql.SQL('SELECT column_name,data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
    res = fetchDataInDatabase(query, [schema,tableName], connection)
    columns = []
    template = []
    for row in res:
        if row[0] in data[0]:
            columns.append(row[0])
            if row[1] == 'json':
                template.append('%s::json')
            else:
                template.append('%s')
    template = '(' + ','.join(template) + ')' 

    newData = []
    for item in data:
        item['created_at'] = int(datetime.now().timestamp())
        item['modified_at'] = int(datetime.now().timestamp())
        # TODO: Check if any column is not nullable that does not appear in data. Return ERROR in this case
        newItem = []
        for column in columns:
            if column in item:
                if type(item[column]) == dict or type(item[column]) == list:
                    if byCopy:
                        newItem.append(json.dumps(item[column]).encode('utf8'))
                    else:
                        newItem.append(json.dumps(item[column]))
                elif type(item[column]) == str:
                    if byCopy:
                        newItem.append(str(item[column]).encode('utf8'))
                    else:
                        newItem.append(item[column])
                else:
                    newItem.append(item[column])
            else:
                newItem.append(None)
        newData.append(newItem)

    if byCopy and not onConflict:
        result = insertBulkDataIntoDatabaseByCopyManager('.'.join([schema,tableName]),columns,newData,connection)  
    else:
        onConflictString = ''
        if onConflict:
            onConflictString = 'ON CONFLICT ({}) DO NOTHING'.format(uniqueColumnNamesForConflict)
        queryString = "INSERT INTO {{}}.{} ({}) VALUES %s {};".format(tableName,', '.join(columns),onConflictString)
        query = sql.SQL(queryString).format(sql.Identifier(schema))
        result = insertBulkDataIntoDatabase(query,template,newData,connection)
    return result

def PUT(connection, schema, updates:dict, tableName:str, conditions:dict={}):
    updates['modified_at'] = int(datetime.now().timestamp())
    sqlTemplateEqual = "{} = %s"
    sqlTemplateIn = "{} IN ({})"
    setArray = []
    conditionArray = []
    params = []
    for key in updates.keys():
        setArray.append(sqlTemplateEqual.format(key))
        if type(updates[key]) == dict or type(updates[key]) == list:
            params.append(json.dumps(updates[key]))
            
        else:
            params.append(updates[key])
    
    for key in conditions.keys():
        if type(conditions[key]) == list:
            conditionArray.append(sqlTemplateIn.format(key,','.join(['%s'] * len(conditions[key]))))
            for item in conditions[key]:
                params.append(item) 
        else:
            conditionArray.append(sqlTemplateEqual.format(key))
            params.append(conditions[key]) 
    
    if len(conditionArray) == 0:
        queryString = "UPDATE {{}}.{} SET {}".format(tableName,', '.join(setArray))
    else:
        queryString = "UPDATE {{}}.{} SET {} WHERE 1=1 AND {}".format(tableName,', '.join(setArray),' AND '.join(conditionArray))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    insertDataIntoDatabase(query, params, connection)    
    return None

def PUT_BULK(connection, schema, updates:list, tableName:str, conditionColumns:list=['id']):
    '''
    updates must be list of dictionaries (with equal keys!). Key is column name according to database!
    Every column of the table which is NOT NULL and has no DEFAULT, must occur in updates! Otherwhise an error will occur!
    keys in conditionColumns must also be in updates!
    '''
    query = sql.SQL('SELECT column_name,data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
    res = fetchDataInDatabase(query, [schema,tableName], connection)
    columns = ['modified_at']
    for row in res:
        if row[0] in updates[0]:
            columns.append(row[0])


    newData = []
    for item in updates:
        item['modified_at'] = int(datetime.now().timestamp())
        # TODO: Check if any column is not nullable that does not appear in data. Return ERROR in this case
        newItem = []
        for column in columns:
            if column in item:
                if type(item[column]) == dict or type(item[column]) == list:
                    newItem.append(json.dumps(item[column]).encode('utf8'))
                elif type(item[column]) == str:
                    newItem.append(str(item[column]).encode('utf8'))
                else:
                    newItem.append(item[column])
            else:
                newItem.append(None)
        newData.append(newItem)

    setArray = []
    conditionArray = []

    for col in conditionColumns:
        if col not in columns:
            return {
                'error': 1,
                'msg': 'at least one columnn in conditionColumns is not in updates'
            }
        conditionArray.append("t.{} = tmp.{}".format(col,col))
    for col in columns:
        if col not in conditionColumns:
            setArray.append("{} = tmp.{}".format(col,col))
    
    tmpTableName = schema + '_tmp_' + tableName
    queryString = "UPDATE {{}}.{} AS t SET {} FROM {} tmp WHERE 1=1 AND {}".format(tableName,', '.join(setArray),tmpTableName,' AND '.join(conditionArray))

    query = sql.SQL(queryString).format(sql.Identifier(schema))

    result = updatetBulkDataInDatabaseByCopyManager(schema,tableName,columns,newData,query,connection)   
    return result

def SELECT(connection, schema, columns:list, tableName:str, conditions:dict={}):
    if columns == [] or columns == ['*']:
        query = sql.SQL('SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
        res = fetchDataInDatabase(query, [schema,tableName], connection)
        columns = []
        for row in res:
            columns.append(row[0])
    
    sqlTemplateEqual = "{} = %s"
    sqlTemplateIn = "{} IN ({})"
    sqlTemplateNotIn = "{} NOT IN ({})"
    sqlTemplateIsNull = "{} IS NULL"
    sqlTemplateIsNotNull = "{} IS NOT NULL"

    sqlTemplateLt = "{} < %s"
    sqlTemplateLte = "{} <= %s"
    sqlTemplateGt = "{} > %s"
    sqlTemplateGte = "{} >= %s"
    conditionArray = []
    params = []
    for key in conditions.keys():
        conditionColumnName = key
        if type(conditions[key]) == dict:
            conditionValue = conditions[key]['value']
            if 'alias' in conditions[key]:
                conditionColumnName = conditions[key]['alias']
            sqlTemplate = None
            if conditions[key]['operator'] == 'lt':
                sqlTemplate = sqlTemplateLt
            elif conditions[key]['operator'] == 'lte':
                sqlTemplate = sqlTemplateLte
            elif conditions[key]['operator'] == 'gt':
                sqlTemplate = sqlTemplateGt
            elif conditions[key]['operator'] == 'gte':
                sqlTemplate = sqlTemplateGte
            elif conditions[key]['operator'] == 'not in':
                sqlTemplate = sqlTemplateNotIn
            elif conditions[key]['operator'] == 'in':
                sqlTemplate = sqlTemplateIn
            elif conditions[key]['operator'] == 'is not':
                sqlTemplate = sqlTemplateIsNotNull
        else:
            conditionValue = conditions[key]
            if conditionValue is None:
                sqlTemplate = sqlTemplateIsNull
            else:
                sqlTemplate = sqlTemplateEqual
        
        
        if type(conditionValue) == list:
            if sqlTemplate is None or sqlTemplate not in (sqlTemplateIn,sqlTemplateNotIn):
                conditionArray.append(sqlTemplateIn.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            else:
                conditionArray.append(sqlTemplate.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            for item in conditionValue:
                params.append(item) 
        else:
            conditionArray.append(sqlTemplate.format(conditionColumnName))
            if conditionValue is not None:
                params.append(conditionValue) 
   
    if len(conditionArray) == 0:
        queryString = "SELECT {} FROM {{}}.{}".format(', '.join(columns),tableName)
    else:
        queryString = "SELECT {} FROM {{}}.{} WHERE 1=1 AND {}".format(', '.join(columns),tableName,' AND '.join(conditionArray))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    res = fetchDataInDatabase(query, params, connection)    

    if res == None:
        return []
    
    result = []
    for row in res:
        resultDict = {}
        for idx,item in enumerate(row):
            resultDict[columns[idx]] = item
        result.append(resultDict)
    return result

def SELECT_FUNCTION(connection, schema,functionName,functionParameter:list,columns:list=[]):
    '''
    See PostGreSQL Function get_return_columns_of_function for supported RETURN TYPES
    '''
    if columns == [] or columns == ['*']:
        queryString = 'SELECT column_name, arg_type, col_num FROM {}.get_return_columns_of_function(%s,%s)'
        query = sql.SQL(queryString).format(sql.Identifier(schema))
        # query = sql.SQL('SELECT t.column_name, t.arg_type::regtype::text, t.col_num FROM pg_proc p LEFT JOIN pg_namespace pn ON p.pronamespace = pn.oid \
        #                 CROSS JOIN UNNEST(proargnames, proargmodes, proallargtypes) WITH ORDINALITY AS t(column_name, arg_mode, arg_type, col_num) \
        #                 WHERE p.proname = %s AND pn.nspname = %s AND t.arg_mode = \'t\' ORDER BY t.col_num')
        res = fetchDataInDatabase(query, [functionName,schema], connection)
        if res == None:
            return []
        
        columns = []
        for row in res:
            columns.append(row[0])
    queryString = "SELECT {} FROM {{}}.{}({})".format(', '.join(columns),functionName,','.join(['%s']*len(functionParameter)))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    res = fetchDataInDatabase(query, functionParameter, connection)    

    if res == None:
        return []
    
    result = []
    for row in res:
        resultDict = {}
        for idx,item in enumerate(row):
            resultDict[columns[idx]] = item
        result.append(resultDict)
    return result

def DELETE(connection, schema, tableName:str, conditions:dict={}):

    query = sql.SQL('SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
    res = fetchDataInDatabase(query, [schema,tableName], connection)
    columns = []
    for row in res:
        columns.append(row[0])
    
    sqlTemplateEqual = "{} = %s"
    sqlTemplateIn = "{} IN ({})"
    sqlTemplateNotIn = "{} NOT IN ({})"
    sqlTemplateIsNull = "{} IS NULL"
    sqlTemplateIsNotNull = "{} IS NOT NULL"

    sqlTemplateLt = "{} < %s"
    sqlTemplateLte = "{} <= %s"
    sqlTemplateGt = "{} > %s"
    sqlTemplateGte = "{} >= %s"
    conditionArray = []
    params = []
    for key in conditions.keys():
        conditionColumnName = key
        if type(conditions[key]) == dict:
            conditionValue = conditions[key]['value']
            if 'alias' in conditions[key]:
                conditionColumnName = conditions[key]['alias']
            sqlTemplate = None
            if conditions[key]['operator'] == 'lt':
                sqlTemplate = sqlTemplateLt
            elif conditions[key]['operator'] == 'lte':
                sqlTemplate = sqlTemplateLte
            elif conditions[key]['operator'] == 'gt':
                sqlTemplate = sqlTemplateGt
            elif conditions[key]['operator'] == 'gte':
                sqlTemplate = sqlTemplateGte
            elif conditions[key]['operator'] == 'not in':
                sqlTemplate = sqlTemplateNotIn
            elif conditions[key]['operator'] == 'in':
                sqlTemplate = sqlTemplateIn
            elif conditions[key]['operator'] == 'is not':
                sqlTemplate = sqlTemplateIsNotNull
        else:
            conditionValue = conditions[key]
            if conditionValue is None:
                sqlTemplate = sqlTemplateIsNull
            else:
                sqlTemplate = sqlTemplateEqual
        
        
        if type(conditionValue) == list:
            if sqlTemplate is None or sqlTemplate not in (sqlTemplateIn,sqlTemplateNotIn):
                conditionArray.append(sqlTemplateIn.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            else:
                conditionArray.append(sqlTemplate.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            for item in conditionValue:
                params.append(item) 
        else:
            conditionArray.append(sqlTemplate.format(conditionColumnName))
            if conditionValue is not None:
                params.append(conditionValue) 
   
    queryString = "DELETE FROM {{}}.{} WHERE 1=1 AND {}".format(tableName,' AND '.join(conditionArray))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    res = insertDataIntoDatabase(query, params, connection)    

    return True