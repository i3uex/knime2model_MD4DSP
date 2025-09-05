import os

import pandas as pd
import numpy as np
import functions.contract_invariants as contract_invariants
import functions.contract_pre_post as contract_pre_post
import functions.data_smells as data_smells
from helpers.enumerations import Belong, Operator, Operation, SpecialType, DataType, DerivedType, Closure, FilterType, MapOperation, MathOperator
from helpers.logger import set_logger
import pyarrow
from functions.PMML import PMMLModel

def generateWorkflow():
	#-----------------New DataProcessing-----------------
	join_Name_with_City__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/join_input_dataDictionary.parquet')

	if os.path.exists('/wf_validation_python/data/output/join_output_dataDictionary.parquet'):
		join_Name_with_City__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/join_output_dataDictionary.parquet')

	
	common_invalid_list=['inf', '-inf', 'nan']
	common_missing_list=['', '?', '.','null','none','na']
	
	
	data_smells.check_missing_invalid_value_consistency(data_dictionary=join_Name_with_City__input_dataDictionary_df, 
														missing_invalid_list=[], common_missing_invalid_list=common_missing_list, field='Name', origin_function="String Manipulation")
	
	data_smells.check_missing_invalid_value_consistency(data_dictionary=join_Name_with_City__input_dataDictionary_df, 
														missing_invalid_list=[], common_missing_invalid_list=common_missing_list, field='City', origin_function="String Manipulation")
	
	data_smells.check_integer_as_floating_point(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_types_as_string(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', expected_type=DataType.STRING, origin_function="String Manipulation")
	data_smells.check_suspect_precision(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_date_as_datetime(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_ambiguous_datetime_format(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_number_string_size(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_special_character_spacing(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_string_casing(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_intermingled_data_type(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_contracted_text(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_abbreviation_consistency(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_syntactic_synonym(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_ambiguous_value(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='Name', origin_function="String Manipulation")
	data_smells.check_separating_consistency(data_dictionary=join_Name_with_City__input_dataDictionary_df, decimal_sep='.',  field='Name', origin_function="String Manipulation")
			
	data_smells.check_integer_as_floating_point(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_types_as_string(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', expected_type=DataType.STRING, origin_function="String Manipulation")
	data_smells.check_suspect_precision(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_date_as_datetime(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_ambiguous_datetime_format(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_number_string_size(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_special_character_spacing(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_string_casing(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_intermingled_data_type(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_contracted_text(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_abbreviation_consistency(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_syntactic_synonym(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_ambiguous_value(data_dictionary=join_Name_with_City__input_dataDictionary_df, field='City', origin_function="String Manipulation")
	data_smells.check_separating_consistency(data_dictionary=join_Name_with_City__input_dataDictionary_df, decimal_sep='.',  field='City', origin_function="String Manipulation")
			
	
	
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
