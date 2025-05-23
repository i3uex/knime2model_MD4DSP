import pandas as pd
import numpy as np
import functions.contract_invariants as contract_invariants
import functions.contract_pre_post as contract_pre_post
import functions.data_transformations as data_transformations
from helpers.enumerations import Belong, Operator, Operation, SpecialType, DataType, DerivedType, Closure, FilterType, MapOperation, MathOperator
from helpers.logger import set_logger
import pyarrow
from functions.PMML import PMMLModel

def generateWorkflow():

	#-----------------New DataProcessing-----------------
	binner_native_country__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/binner_input_dataDictionary.parquet')
	binner_native_country__input_dataDictionary_df.to_parquet('/wf_validation_python/data/output/binner_input_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_native_country__input_dataDictionary_df,
	                                	closure_type=Closure(3), belong_op=Belong(0), field='native-country'):
		print('PRECONDITION binner(native-country)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION binner(native-country)_PRE_valueRange NOT VALIDATED')
	
	binner_native_country__input_dataDictionary_transformed=binner_native_country__input_dataDictionary_df.copy()
	binner_native_country__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=binner_native_country__input_dataDictionary_transformed,
																  data_type_output = DataType(0),
																  field_in = 'native-country', field_out = 'prediction')
	
	binner_native_country__output_dataDictionary_df=binner_native_country__input_dataDictionary_transformed
	binner_native_country__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	binner_native_country__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	binner_native_country__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_native_country__input_dataDictionary_transformed,
																  left_margin=40.0, right_margin=40.0,
																  closure_type=Closure(2),
																  fix_value_output='FULL-TIME',
							                                      data_type_output = DataType(0),
																  field_in = 'native-country',
																  field_out = 'prediction')
	
	binner_native_country__output_dataDictionary_df=binner_native_country__input_dataDictionary_transformed
	binner_native_country__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	binner_native_country__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	binner_native_country__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_native_country__input_dataDictionary_transformed,
																  left_margin=-1.0E9, right_margin=40.0,
																  closure_type=Closure(0),
																  fix_value_output='PART-TIME',
							                                      data_type_output = DataType(0),
																  field_in = 'native-country',
																  field_out = 'prediction')
	
	binner_native_country__output_dataDictionary_df=binner_native_country__input_dataDictionary_transformed
	binner_native_country__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	binner_native_country__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	binner_native_country__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_native_country__input_dataDictionary_transformed,
																  left_margin=40.0, right_margin=1.0E9,
																  closure_type=Closure(0),
																  fix_value_output='PART-TIME',
							                                      data_type_output = DataType(0),
																  field_in = 'native-country',
																  field_out = 'prediction')
	
	binner_native_country__output_dataDictionary_df=binner_native_country__input_dataDictionary_transformed
	binner_native_country__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	binner_native_country__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')
	
	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_native_country__output_dataDictionary_df,
	                                	closure_type=Closure(0), belong_op=Belong(0), field='prediction'):
		print('POSTCONDITION binner(native-country)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION binner(native-country)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_native_country__input_dataDictionary_df,
											data_dictionary_out=binner_native_country__output_dataDictionary_df,
											left_margin=40.0, right_margin=40.0,
											closure_type=Closure(2),
											fix_value_output='FULL-TIME',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='native-country', field_out='prediction'):
		print('INVARIANT binner(native-country)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(native-country)_INV_condition NOT VALIDATED')
	
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_native_country__input_dataDictionary_df,
											data_dictionary_out=binner_native_country__output_dataDictionary_df,
											left_margin=-1.0E9, right_margin=40.0,
											closure_type=Closure(0),
											fix_value_output='PART-TIME',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='native-country', field_out='prediction'):
		print('INVARIANT binner(native-country)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(native-country)_INV_condition NOT VALIDATED')
	
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_native_country__input_dataDictionary_df,
											data_dictionary_out=binner_native_country__output_dataDictionary_df,
											left_margin=40.0, right_margin=1.0E9,
											closure_type=Closure(0),
											fix_value_output='PART-TIME',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='native-country', field_out='prediction'):
		print('INVARIANT binner(native-country)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(native-country)_INV_condition NOT VALIDATED')
	
	
	
	
	
	#-----------------New DataProcessing-----------------
	mapping_native_country__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/binner_output_dataDictionary.parquet')

	if contract_pre_post.check_fix_value_range(value='-', data_dictionary=mapping_native_country__input_dataDictionary_df, belong_op=Belong(0), field='native-country',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION mapping(native-country)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION mapping(native-country)_PRE_valueRange NOT VALIDATED')
	
	input_values_list=['-']
	output_values_list=[' ']
	data_type_input_list=[DataType(0)]
	data_type_output_list=[DataType(0)]
	map_operation_list=[MapOperation(0)]
	
	mapping_native_country__output_dataDictionary_df=data_transformations.transform_fix_value_fix_value(data_dictionary=mapping_native_country__input_dataDictionary_df, input_values_list=input_values_list,
																  output_values_list=output_values_list,
							                                      data_type_input_list = data_type_input_list,
							                                      data_type_output_list = data_type_output_list,
																  map_operation_list = map_operation_list,
																  field_in = 'native-country', field_out = 'native-country')
	
	mapping_native_country__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/columnExpressions_output_dataDictionary.parquet')
	mapping_native_country__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/columnExpressions_output_dataDictionary.parquet')
	
	if contract_pre_post.check_fix_value_range(value='-', data_dictionary=mapping_native_country__output_dataDictionary_df, belong_op=Belong(0), field='native-country',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION mapping(native-country)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION mapping(native-country)_POST_valueRange NOT VALIDATED')
	
	
	input_values_list_mapping_INV_condition=['-']
	output_values_list_mapping_INV_condition=[' ']
	
	data_type_input_list_mapping_INV_condition=[DataType(0)]
	data_type_output_list_mapping_INV_condition=[DataType(0)]
	
	is_substring_list_mapping_INV_condition=[False]
	
	if contract_invariants.check_inv_fix_value_fix_value(data_dictionary_in=mapping_native_country__input_dataDictionary_df,
											data_dictionary_out=mapping_native_country__output_dataDictionary_df,
											input_values_list=input_values_list_mapping_INV_condition, 
											output_values_list=output_values_list_mapping_INV_condition,
											is_substring_list=is_substring_list_mapping_INV_condition,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											data_type_input_list=data_type_input_list_mapping_INV_condition,
											data_type_output_list=data_type_output_list_mapping_INV_condition,
											field_in='native-country', field_out='native-country'):
		print('INVARIANT mapping(native-country)_INV_condition VALIDATED')
	else:
		print('INVARIANT mapping(native-country)_INV_condition NOT VALIDATED')
	
	
	
	
	#-----------------New DataProcessing-----------------
	mathOperation_year_of_birth__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/columnExpressions_output_dataDictionary.parquet')

	missing_values_mathOperation_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=mathOperation_year_of_birth__input_dataDictionary_df, field='age', 
									missing_values=missing_values_mathOperation_PRE_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION mathOperation(year-of-birth)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION mathOperation(year-of-birth)_PRE_valueRange NOT VALIDATED')
	
	mathOperation_year_of_birth__input_dataDictionary_transformed=mathOperation_year_of_birth__input_dataDictionary_df.copy()
	mathOperation_year_of_birth__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=mathOperation_year_of_birth__input_dataDictionary_transformed,
																  data_type_output = DataType(5),
																  field_in = 'age', field_out = 'year-of-birth')
	
	mathOperation_year_of_birth__output_dataDictionary_df=mathOperation_year_of_birth__input_dataDictionary_transformed
	mathOperation_year_of_birth__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/columnExpressions_output_dataDictionary.parquet')
	mathOperation_year_of_birth__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/columnExpressions_output_dataDictionary.parquet')
	mathOperation_year_of_birth__input_dataDictionary_transformed=data_transformations.transform_math_operation(data_dictionary=mathOperation_year_of_birth__input_dataDictionary_transformed,
																math_op=MathOperator(1), field_out='year-of-birth',
																firstOperand='1994', isFieldFirst=False,secondOperand='age', isFieldSecond=True)
	
	mathOperation_year_of_birth__output_dataDictionary_df=mathOperation_year_of_birth__input_dataDictionary_transformed
	mathOperation_year_of_birth__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/columnExpressions_output_dataDictionary.parquet')
	mathOperation_year_of_birth__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/columnExpressions_output_dataDictionary.parquet')
	
	missing_values_mathOperation_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=mathOperation_year_of_birth__output_dataDictionary_df, field='year-of-birth', 
									missing_values=missing_values_mathOperation_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION mathOperation(year-of-birth)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION mathOperation(year-of-birth)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_math_operation(data_dictionary_in=mathOperation_year_of_birth__input_dataDictionary_df,
											data_dictionary_out=mathOperation_year_of_birth__output_dataDictionary_df,
											math_op=MathOperator(1),
											firstOperand='', isFieldFirst=False,secondOperand='age', isFieldSecond=True, 
											belong_op_out=Belong(0), field_in='year-of-birth', field_out='year-of-birth'):
		print('INVARIANT mathOperation(year-of-birth)_INV_condition VALIDATED')
	else:
		print('INVARIANT mathOperation(year-of-birth)_INV_condition NOT VALIDATED')
	
	
	
	
	
	



set_logger("dataProcessing")
generateWorkflow()
