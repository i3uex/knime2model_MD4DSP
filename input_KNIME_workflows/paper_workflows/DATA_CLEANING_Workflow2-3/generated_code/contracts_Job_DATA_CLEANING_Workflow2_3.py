import os

import pandas as pd
import numpy as np
import functions.contract_invariants as contract_invariants
import functions.contract_pre_post as contract_pre_post
from helpers.enumerations import Belong, Operator, Operation, SpecialType, DataType, DerivedType, Closure, FilterType, MapOperation, MathOperator
from helpers.logger import set_logger
import pyarrow
from functions.PMML import PMMLModel

def generateWorkflow():
	#-----------------New DataProcessing-----------------
	rowFilterMissing_marital_status__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/rowFilterMissing_input_dataDictionary.parquet')
	rowFilterMissing_marital_status__input_dataDictionary_df.to_parquet('/wf_validation_python/data/output/rowFilterMissing_input_dataDictionary.parquet')
	if os.path.exists('/wf_validation_python/data/output/rowFilterMissing_output_dataDictionary.parquet'):
		rowFilterMissing_marital_status__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/rowFilterMissing_output_dataDictionary.parquet')

	missing_values_rowFilterMissing_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=rowFilterMissing_marital_status__input_dataDictionary_df, field='marital-status', 
									missing_values=missing_values_rowFilterMissing_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION rowFilterMissing(marital-status)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION rowFilterMissing(marital-status)_PRE_valueRange NOT VALIDATED')
	
	missing_values_rowFilterMissing_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=rowFilterMissing_marital_status__output_dataDictionary_df, field='marital-status', 
									missing_values=missing_values_rowFilterMissing_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION rowFilterMissing(marital-status)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION rowFilterMissing(marital-status)_POST_valueRange NOT VALIDATED')
	
	#-----------------New DataProcessing-----------------
	rowFilterPrimitive_workclass__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/rowFilterMissing_output_dataDictionary.parquet')

	if os.path.exists('/wf_validation_python/data/output/rowFilterPrimitive_output_dataDictionary.parquet'):
		rowFilterPrimitive_workclass__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/rowFilterPrimitive_output_dataDictionary.parquet')

	if contract_pre_post.check_fix_value_range(value='s*', data_dictionary=rowFilterPrimitive_workclass__input_dataDictionary_df, belong_op=Belong(0), field='workclass',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION rowFilterPrimitive(workclass)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION rowFilterPrimitive(workclass)_PRE_valueRange NOT VALIDATED')
	
	if contract_pre_post.check_fix_value_range(value='s*', data_dictionary=rowFilterPrimitive_workclass__output_dataDictionary_df, belong_op=Belong(0), field='workclass',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION rowFilterPrimitive(workclass)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION rowFilterPrimitive(workclass)_POST_valueRange NOT VALIDATED')
	


set_logger("contracts")
generateWorkflow()
