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
	join_Name_with_City__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/join_input_dataDictionary.parquet')

	if os.path.exists('/wf_validation_python/data/output/join_output_dataDictionary.parquet'):
		join_Name_with_City__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/join_output_dataDictionary.parquet')

	
	dictionary_join_check_INV_THEN={'Name': True, ' - ': False, 'City': True}
	if contract_invariants.check_inv_join(data_dictionary_in=join_Name_with_City__input_dataDictionary_df,
								data_dictionary_out=join_Name_with_City__output_dataDictionary_df,
								dictionary=dictionary_join_check_INV_THEN,
								field_out='Name with City', origin_function="String Manipulation"):
		print('INVARIANT String Manipulation(Name) JoinInputs:Name VALIDATED')
	else:
		print('INVARIANT String Manipulation(Name) JoinInputs:Name NOT VALIDATED')
	
	dictionary_join_check_INV_THEN={'Name': True, ' - ': False, 'City': True}
	if contract_invariants.check_inv_join(data_dictionary_in=join_Name_with_City__input_dataDictionary_df,
								data_dictionary_out=join_Name_with_City__output_dataDictionary_df,
								dictionary=dictionary_join_check_INV_THEN,
								field_out='Name with City', origin_function="String Manipulation"):
		print('INVARIANT String Manipulation(City) JoinInputs:Name VALIDATED')
	else:
		print('INVARIANT String Manipulation(City) JoinInputs:Name NOT VALIDATED')
	
	
	
set_logger("contracts")
generateWorkflow()
