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
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_input_dataDictionary.parquet')
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df.to_parquet('/wf_validation_python/data/output/missing_input_dataDictionary.parquet')

	missing_values_imputeByDerivedValue_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df, field='sex', 
									missing_values=missing_values_imputeByDerivedValue_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByMostFrequent(sex)_PRE_value_range VALIDATED')
	else:
		print('PRECONDITION imputeMissingByMostFrequent(sex)_PRE_value_range NOT VALIDATED')
	
	missing_values_imputeByDerivedValue_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df, field='ETHNICITY', 
									missing_values=missing_values_imputeByDerivedValue_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByMostFrequent(ETHNICITY)_PRE_value_range VALIDATED')
	else:
		print('PRECONDITION imputeMissingByMostFrequent(ETHNICITY)_PRE_value_range NOT VALIDATED')
	
	missing_values_imputeByDerivedValue_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df, field='IRSCHOOL', 
									missing_values=missing_values_imputeByDerivedValue_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByMostFrequent(IRSCHOOL)_PRE_value_range VALIDATED')
	else:
		print('PRECONDITION imputeMissingByMostFrequent(IRSCHOOL)_PRE_value_range NOT VALIDATED')
	
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df.copy()
	missing_values_list=[]
	
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed=data_transformations.transform_special_value_derived_value(data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), derived_type_output=DerivedType(0),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'sex', field_out = 'sex')
	
	missing_values_list=[]
	
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed=data_transformations.transform_special_value_derived_value(data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), derived_type_output=DerivedType(0),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'ETHNICITY', field_out = 'ETHNICITY')
	
	missing_values_list=[]
	
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed=data_transformations.transform_special_value_derived_value(data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), derived_type_output=DerivedType(0),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'IRSCHOOL', field_out = 'IRSCHOOL')
	
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_transformed
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	
	missing_values_imputeByDerivedValue_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df, field='sex', 
									missing_values=missing_values_imputeByDerivedValue_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION POST_value_range_impute_sex_columns VALIDATED')
	else:
		print('POSTCONDITION POST_value_range_impute_sex_columns NOT VALIDATED')
	
	missing_values_imputeByDerivedValue_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df, field='ETHNICITY', 
									missing_values=missing_values_imputeByDerivedValue_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION POST_value_range_impute_ETHNICITY_columns VALIDATED')
	else:
		print('POSTCONDITION POST_value_range_impute_ETHNICITY_columns NOT VALIDATED')
	
	missing_values_imputeByDerivedValue_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df, field='IRSCHOOL', 
									missing_values=missing_values_imputeByDerivedValue_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION POST_value_range_impute_IRSCHOOL_columns VALIDATED')
	else:
		print('POSTCONDITION POST_value_range_impute_IRSCHOOL_columns NOT VALIDATED')
	
	missing_values_imputeByDerivedValue_INV_condition=[]
	if contract_invariants.check_inv_special_value_derived_value(data_dictionary_in=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df,
								data_dictionary_out=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df,
								belong_op_in=Belong(0),
								belong_op_out=Belong(0),
								special_type_input=SpecialType(0),
								derived_type_output=DerivedType(0),
								missing_values=missing_values_imputeByDerivedValue_INV_condition, axis_param=0, field_in='sex', field_out='sex'):
		print('INVARIANT INV_condition_impute_sex_columns VALIDATED')
	else:
		print('INVARIANT INV_condition_impute_sex_columns NOT VALIDATED')
	
	
	
	missing_values_imputeByDerivedValue_INV_condition=[]
	if contract_invariants.check_inv_special_value_derived_value(data_dictionary_in=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df,
								data_dictionary_out=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df,
								belong_op_in=Belong(0),
								belong_op_out=Belong(0),
								special_type_input=SpecialType(0),
								derived_type_output=DerivedType(0),
								missing_values=missing_values_imputeByDerivedValue_INV_condition, axis_param=0, field_in='ETHNICITY', field_out='ETHNICITY'):
		print('INVARIANT INV_condition_impute_ETHNICITY_columns VALIDATED')
	else:
		print('INVARIANT INV_condition_impute_ETHNICITY_columns NOT VALIDATED')
	
	
	
	missing_values_imputeByDerivedValue_INV_condition=[]
	if contract_invariants.check_inv_special_value_derived_value(data_dictionary_in=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__input_dataDictionary_df,
								data_dictionary_out=imputeMissingByMostFrequent_sex_ETHNICITY_IRSCHOOL__output_dataDictionary_df,
								belong_op_in=Belong(0),
								belong_op_out=Belong(0),
								special_type_input=SpecialType(0),
								derived_type_output=DerivedType(0),
								missing_values=missing_values_imputeByDerivedValue_INV_condition, axis_param=0, field_in='IRSCHOOL', field_out='IRSCHOOL'):
		print('INVARIANT INV_condition_impute_IRSCHOOL_columns VALIDATED')
	else:
		print('INVARIANT INV_condition_impute_IRSCHOOL_columns NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	imputeMissingByMean_satscore__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')

	missing_values_imputeByNumericOp_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMean_satscore__input_dataDictionary_df, field='satscore', 
									missing_values=missing_values_imputeByNumericOp_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByMean(satscore)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeMissingByMean(satscore)_PRE_valueRange NOT VALIDATED')
	
	imputeMissingByMean_satscore__input_dataDictionary_transformed=imputeMissingByMean_satscore__input_dataDictionary_df.copy()
	missing_values_list=[]
	
	imputeMissingByMean_satscore__input_dataDictionary_transformed=data_transformations.transform_special_value_num_op(data_dictionary=imputeMissingByMean_satscore__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), num_op_output=Operation(1),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'satscore', field_out = 'satscore')
	
	imputeMissingByMean_satscore__output_dataDictionary_df=imputeMissingByMean_satscore__input_dataDictionary_transformed
	imputeMissingByMean_satscore__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	imputeMissingByMean_satscore__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	
	missing_values_imputeByNumericOp_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMean_satscore__output_dataDictionary_df, field='satscore', 
									missing_values=missing_values_imputeByNumericOp_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeMissingByMean(satscore)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeMissingByMean(satscore)_POST_valueRange NOT VALIDATED')
	
	missing_values_imputeByNumericOp_INV_condition=[]
	if contract_invariants.check_inv_special_value_num_op(data_dictionary_in=imputeMissingByMean_satscore__input_dataDictionary_df,
											data_dictionary_out=imputeMissingByMean_satscore__output_dataDictionary_df,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											special_type_input=SpecialType(0),
											num_op_output=Operation(1),
											missing_values=missing_values_imputeByNumericOp_INV_condition, axis_param=0, field_in='satscore', field_out='satscore'):
		print('INVARIANT imputeMissingByMean(satscore)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeMissingByMean(satscore)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	imputeMissingByMean_avg_income_distance__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')

	missing_values_imputeByNumericOp_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMean_avg_income_distance__input_dataDictionary_df, field='avg_income', 
									missing_values=missing_values_imputeByNumericOp_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByMean(avg_income)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeMissingByMean(avg_income)_PRE_valueRange NOT VALIDATED')
	
	missing_values_imputeByNumericOp_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMean_avg_income_distance__input_dataDictionary_df, field='distance', 
									missing_values=missing_values_imputeByNumericOp_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByMean(distance)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeMissingByMean(distance)_PRE_valueRange NOT VALIDATED')
	
	imputeMissingByMean_avg_income_distance__input_dataDictionary_transformed=imputeMissingByMean_avg_income_distance__input_dataDictionary_df.copy()
	missing_values_list=[]
	
	imputeMissingByMean_avg_income_distance__input_dataDictionary_transformed=data_transformations.transform_special_value_num_op(data_dictionary=imputeMissingByMean_avg_income_distance__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), num_op_output=Operation(1),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'avg_income', field_out = 'avg_income')
	
	missing_values_list=[]
	
	imputeMissingByMean_avg_income_distance__input_dataDictionary_transformed=data_transformations.transform_special_value_num_op(data_dictionary=imputeMissingByMean_avg_income_distance__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), num_op_output=Operation(1),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'distance', field_out = 'distance')
	
	imputeMissingByMean_avg_income_distance__output_dataDictionary_df=imputeMissingByMean_avg_income_distance__input_dataDictionary_transformed
	imputeMissingByMean_avg_income_distance__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	imputeMissingByMean_avg_income_distance__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	
	missing_values_imputeByNumericOp_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMean_avg_income_distance__output_dataDictionary_df, field='avg_income', 
									missing_values=missing_values_imputeByNumericOp_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeMissingByMean(avg_income)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeMissingByMean(avg_income)_POST_valueRange NOT VALIDATED')
	
	missing_values_imputeByNumericOp_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByMean_avg_income_distance__output_dataDictionary_df, field='distance', 
									missing_values=missing_values_imputeByNumericOp_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeMissingByMean(distance)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeMissingByMean(distance)_POST_valueRange NOT VALIDATED')
	
	missing_values_imputeByNumericOp_INV_condition=[]
	if contract_invariants.check_inv_special_value_num_op(data_dictionary_in=imputeMissingByMean_avg_income_distance__input_dataDictionary_df,
											data_dictionary_out=imputeMissingByMean_avg_income_distance__output_dataDictionary_df,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											special_type_input=SpecialType(0),
											num_op_output=Operation(1),
											missing_values=missing_values_imputeByNumericOp_INV_condition, axis_param=0, field_in='avg_income', field_out='avg_income'):
		print('INVARIANT imputeMissingByMean(avg_income)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeMissingByMean(avg_income)_INV_condition NOT VALIDATED')
	
	
	
	missing_values_imputeByNumericOp_INV_condition=[]
	if contract_invariants.check_inv_special_value_num_op(data_dictionary_in=imputeMissingByMean_avg_income_distance__input_dataDictionary_df,
											data_dictionary_out=imputeMissingByMean_avg_income_distance__output_dataDictionary_df,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											special_type_input=SpecialType(0),
											num_op_output=Operation(1),
											missing_values=missing_values_imputeByNumericOp_INV_condition, axis_param=0, field_in='distance', field_out='distance'):
		print('INVARIANT imputeMissingByMean(distance)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeMissingByMean(distance)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')

	missing_values_imputeByFixValue_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_df, field='ACADEMIC_INTEREST_1', 
									missing_values=missing_values_imputeByFixValue_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_1)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_1)_PRE_valueRange NOT VALIDATED')
	
	missing_values_imputeByFixValue_PRE_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_df, field='ACADEMIC_INTEREST_2', 
									missing_values=missing_values_imputeByFixValue_PRE_valueRange,
									quant_op=Operator(3), quant_rel=60.0/100):
		print('PRECONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_2)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_2)_PRE_valueRange NOT VALIDATED')
	
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_df.copy()
	missing_values_list=[]
	
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed=data_transformations.transform_special_value_fix_value(data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), fix_value_output='Unknown',
																  missing_values=missing_values_list,		
							                                      data_type_output = DataType(0),
																  axis_param=0, field_in = 'ACADEMIC_INTEREST_1', field_out = 'ACADEMIC_INTEREST_1')
	
	missing_values_list=[]
	
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed=data_transformations.transform_special_value_fix_value(data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), fix_value_output='Unknown',
																  missing_values=missing_values_list,		
							                                      data_type_output = DataType(0),
																  axis_param=0, field_in = 'ACADEMIC_INTEREST_2', field_out = 'ACADEMIC_INTEREST_2')
	
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	missing_values_list=[]
	
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed=data_transformations.transform_special_value_fix_value(data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), fix_value_output='Unknown',
																  missing_values=missing_values_list,		
							                                      data_type_output = DataType(0),
																  axis_param=0, field_in = 'ACADEMIC_INTEREST_1', field_out = 'ACADEMIC_INTEREST_1')
	
	missing_values_list=[]
	
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed=data_transformations.transform_special_value_fix_value(data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed,
																  special_type_input=SpecialType(0), fix_value_output='Unknown',
																  missing_values=missing_values_list,		
							                                      data_type_output = DataType(0),
																  axis_param=0, field_in = 'ACADEMIC_INTEREST_2', field_out = 'ACADEMIC_INTEREST_2')
	
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_transformed
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')
	
	missing_values_imputeByFixValue_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df, field='ACADEMIC_INTEREST_1', 
									missing_values=missing_values_imputeByFixValue_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_1)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_1)_POST_valueRange NOT VALIDATED')
	
	missing_values_imputeByFixValue_POST_valueRange=[]
	if contract_pre_post.check_missing_range(belong_op=Belong(0), data_dictionary=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df, field='ACADEMIC_INTEREST_2', 
									missing_values=missing_values_imputeByFixValue_POST_valueRange,
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_2)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeMissingByFixValue(ACADEMIC_INTEREST_2)_POST_valueRange NOT VALIDATED')
	
	missing_values_imputeByFixValue_INV_condition=[]
	if contract_invariants.check_inv_special_value_fix_value(data_dictionary_in=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_df,
								data_dictionary_out=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df,
								special_type_input=SpecialType(0),
								fix_value_output='',
								belong_op_in=Belong(0),
								belong_op_out=Belong(0),
								data_type_output=DataType(0),
								missing_values=missing_values_imputeByFixValue_INV_condition, 
								axis_param=0, field_in='ACADEMIC_INTEREST_1', field_out='ACADEMIC_INTEREST_1'):
		print('INVARIANT imputeMissingByFixValue(ACADEMIC_INTEREST_1)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeMissingByFixValue(ACADEMIC_INTEREST_1)_INV_condition NOT VALIDATED')
	
	
	
	missing_values_imputeByFixValue_INV_condition=[]
	if contract_invariants.check_inv_special_value_fix_value(data_dictionary_in=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__input_dataDictionary_df,
								data_dictionary_out=imputeMissingByFixValue_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2__output_dataDictionary_df,
								special_type_input=SpecialType(0),
								fix_value_output='',
								belong_op_in=Belong(0),
								belong_op_out=Belong(0),
								data_type_output=DataType(0),
								missing_values=missing_values_imputeByFixValue_INV_condition, 
								axis_param=0, field_in='ACADEMIC_INTEREST_2', field_out='ACADEMIC_INTEREST_2'):
		print('INVARIANT imputeMissingByFixValue(ACADEMIC_INTEREST_2)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeMissingByFixValue(ACADEMIC_INTEREST_2)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	rowFilterRange_init_span__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/missing_output_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=rowFilterRange_init_span__input_dataDictionary_df,
	                                	closure_type=Closure(2), belong_op=Belong(0), field='init_span'):
		print('PRECONDITION rowFilter(init_span)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION rowFilter(init_span)_PRE_valueRange NOT VALIDATED')
	
	rowFilterRange_init_span__input_dataDictionary_transformed=rowFilterRange_init_span__input_dataDictionary_df.copy()
	columns_rowFilterRange_param_filter=['init_span']
	
	filter_range_left_values_list_rowFilterRange_param_filter=[-np.inf]
	filter_range_right_values_list_rowFilterRange_param_filter=[0.0]
	closure_type_list_rowFilterRange_param_filter=[Closure(3)]
	
	rowFilterRange_init_span__input_dataDictionary_transformed=data_transformations.transform_filter_rows_range(data_dictionary=rowFilterRange_init_span__input_dataDictionary_transformed,
																											columns=columns_rowFilterRange_param_filter,
																											left_margin_list=filter_range_left_values_list_rowFilterRange_param_filter,
																											right_margin_list=filter_range_right_values_list_rowFilterRange_param_filter,
																											filter_type=FilterType(1),
																											closure_type_list=closure_type_list_rowFilterRange_param_filter)
	rowFilterRange_init_span__output_dataDictionary_df=rowFilterRange_init_span__input_dataDictionary_transformed
	rowFilterRange_init_span__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/rowFilter_output_dataDictionary.parquet')
	rowFilterRange_init_span__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/rowFilter_output_dataDictionary.parquet')
	
	if contract_pre_post.check_fix_value_range(value='-216', data_dictionary=rowFilterRange_init_span__output_dataDictionary_df, belong_op=Belong(0), field='init_span',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION rowFilter(init_span)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION rowFilter(init_span)_POST_valueRange NOT VALIDATED')
	
	#-----------------New DataProcessing-----------------
	columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/rowFilter_output_dataDictionary.parquet')

	field_list_columnFilter_PRE_field_range=['ETHNICITY', 'TERRITORY', 'ACADEMIC_INTEREST_1', 'ACADEMIC_INTEREST_2', 'Enroll', 'TOTAL_CONTACTS', 'SELF_INIT_CNTCTS', 'SOLICITED_CNTCTS', 'CAMPUS_VISIT', 'IRSCHOOL', 'satscore', 'sex', 'mailq', 'premiere', 'init_span', 'int1rat', 'int2rat', 'hscrat', 'avg_income', 'distance', 'Instate']
	if contract_pre_post.check_field_range(fields=field_list_columnFilter_PRE_field_range,
								data_dictionary=columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__input_dataDictionary_df,
								belong_op=Belong(0)):
		print('PRECONDITION columnFilter(ETHNICITY, TERRITORY, ACADEMIC_INTEREST_1, ACADEMIC_INTEREST_2, Enroll, TOTAL_CONTACTS, SELF_INIT_CNTCTS, SOLICITED_CNTCTS, CAMPUS_VISIT, IRSCHOOL, satscore, sex, mailq, premiere, init_span, int1rat, int2rat, hscrat, avg_income, distance, Instate)_PRE_fieldRange VALIDATED')
	else:
		print('PRECONDITION columnFilter(ETHNICITY, TERRITORY, ACADEMIC_INTEREST_1, ACADEMIC_INTEREST_2, Enroll, TOTAL_CONTACTS, SELF_INIT_CNTCTS, SOLICITED_CNTCTS, CAMPUS_VISIT, IRSCHOOL, satscore, sex, mailq, premiere, init_span, int1rat, int2rat, hscrat, avg_income, distance, Instate)_PRE_fieldRange NOT VALIDATED')
	
	
	columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__input_dataDictionary_transformed=columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__input_dataDictionary_df.copy()
	field_list_columnFilter_param_field=['ETHNICITY', 'TERRITORY', 'ACADEMIC_INTEREST_1', 'ACADEMIC_INTEREST_2', 'Enroll', 'TOTAL_CONTACTS', 'SELF_INIT_CNTCTS', 'SOLICITED_CNTCTS', 'CAMPUS_VISIT', 'IRSCHOOL', 'satscore', 'sex', 'mailq', 'premiere', 'init_span', 'int1rat', 'int2rat', 'hscrat', 'avg_income', 'distance', 'Instate']
	
	columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__input_dataDictionary_transformed=data_transformations.transform_filter_columns(data_dictionary=columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__input_dataDictionary_transformed,
																	columns=field_list_columnFilter_param_field, belong_op=Belong.BELONG)
	
	columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__output_dataDictionary_df=columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__input_dataDictionary_transformed
	columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/columnFilter_output_dataDictionary.parquet')
	columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/columnFilter_output_dataDictionary.parquet')
	
	field_list_columnFilter_POST_field_range=['ETHNICITY', 'TERRITORY', 'ACADEMIC_INTEREST_1', 'ACADEMIC_INTEREST_2', 'Enroll', 'TOTAL_CONTACTS', 'SELF_INIT_CNTCTS', 'SOLICITED_CNTCTS', 'CAMPUS_VISIT', 'IRSCHOOL', 'satscore', 'sex', 'mailq', 'premiere', 'init_span', 'int1rat', 'int2rat', 'hscrat', 'avg_income', 'distance', 'Instate']
	if contract_pre_post.check_field_range(fields=field_list_columnFilter_POST_field_range,
								data_dictionary=columnFilter_ETHNICITY_TERRITORY_ACADEMIC_INTEREST_1_ACADEMIC_INTEREST_2_Enroll_TOTAL_CONTACTS_SELF_INIT_CNTCTS_SOLICITED_CNTCTS_CAMPUS_VISIT_IRSCHOOL_satscore_sex_mailq_premiere_init_span_int1rat_int2rat_hscrat_avg_income_distance_Instate__output_dataDictionary_df,
								belong_op=Belong(0)):
		print('POSTCONDITION columnFilter(ETHNICITY, TERRITORY, ACADEMIC_INTEREST_1, ACADEMIC_INTEREST_2, Enroll, TOTAL_CONTACTS, SELF_INIT_CNTCTS, SOLICITED_CNTCTS, CAMPUS_VISIT, IRSCHOOL, satscore, sex, mailq, premiere, init_span, int1rat, int2rat, hscrat, avg_income, distance, Instate)_POST_fieldRange VALIDATED')
	else:
		print('POSTCONDITION columnFilter(ETHNICITY, TERRITORY, ACADEMIC_INTEREST_1, ACADEMIC_INTEREST_2, Enroll, TOTAL_CONTACTS, SELF_INIT_CNTCTS, SOLICITED_CNTCTS, CAMPUS_VISIT, IRSCHOOL, satscore, sex, mailq, premiere, init_span, int1rat, int2rat, hscrat, avg_income, distance, Instate)_POST_fieldRange NOT VALIDATED')
	
	
	#-----------------New DataProcessing-----------------
	mapping_TERRITORY__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/columnFilter_output_dataDictionary.parquet')

	if contract_pre_post.check_fix_value_range(value='N', data_dictionary=mapping_TERRITORY__input_dataDictionary_df, belong_op=Belong(0), field='TERRITORY',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION mapping(TERRITORY)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION mapping(TERRITORY)_PRE_valueRange NOT VALIDATED')
	if contract_pre_post.check_fix_value_range(value='A', data_dictionary=mapping_TERRITORY__input_dataDictionary_df, belong_op=Belong(0), field='TERRITORY',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION mapping(TERRITORY)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION mapping(TERRITORY)_PRE_valueRange NOT VALIDATED')
	
	input_values_list=['N', 'A']
	output_values_list=['0', '0']
	data_type_input_list=[DataType(0), DataType(0)]
	data_type_output_list=[DataType(0), DataType(0)]
	map_operation_list=[MapOperation(0), MapOperation(0)]
	
	mapping_TERRITORY__output_dataDictionary_df=data_transformations.transform_fix_value_fix_value(data_dictionary=mapping_TERRITORY__input_dataDictionary_df, input_values_list=input_values_list,
																  output_values_list=output_values_list,
							                                      data_type_input_list = data_type_input_list,
							                                      data_type_output_list = data_type_output_list,
																  map_operation_list = map_operation_list,
																  field_in = 'TERRITORY', field_out = 'TERRITORY')
	
	mapping_TERRITORY__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/ruleEngine_territory_output_dataDictionary.parquet')
	mapping_TERRITORY__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/ruleEngine_territory_output_dataDictionary.parquet')
	
	if contract_pre_post.check_fix_value_range(value='N', data_dictionary=mapping_TERRITORY__output_dataDictionary_df, belong_op=Belong(0), field='TERRITORY',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION mapping(TERRITORY)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION mapping(TERRITORY)_POST_valueRange NOT VALIDATED')
	if contract_pre_post.check_fix_value_range(value='A', data_dictionary=mapping_TERRITORY__output_dataDictionary_df, belong_op=Belong(0), field='TERRITORY',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION mapping(TERRITORY)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION mapping(TERRITORY)_POST_valueRange NOT VALIDATED')
	
	
	input_values_list_def_INV_condition=['N', 'A']
	output_values_list_def_INV_condition=['0', '0']
	
	data_type_input_list_def_INV_condition=[DataType(0), DataType(0)]
	data_type_output_list_def_INV_condition=[DataType(0), DataType(0)]
	
	is_substring_list_def_INV_condition=[False, False]
	
	if contract_invariants.check_inv_fix_value_fix_value(data_dictionary_in=mapping_TERRITORY__input_dataDictionary_df,
											data_dictionary_out=mapping_TERRITORY__output_dataDictionary_df,
											input_values_list=input_values_list_def_INV_condition, 
											output_values_list=output_values_list_def_INV_condition,
											is_substring_list=is_substring_list_def_INV_condition,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											data_type_input_list=data_type_input_list_def_INV_condition,
											data_type_output_list=data_type_output_list_def_INV_condition,
											field_in='TERRITORY', field_out='TERRITORY'):
		print('INVARIANT mapping(TERRITORY)_INV_condition VALIDATED')
	else:
		print('INVARIANT mapping(TERRITORY)_INV_condition NOT VALIDATED')
	
	
	
	
	#-----------------New DataProcessing-----------------
	mapping_Instate__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/ruleEngine_territory_output_dataDictionary.parquet')

	if contract_pre_post.check_fix_value_range(value='Y', data_dictionary=mapping_Instate__input_dataDictionary_df, belong_op=Belong(0), field='Instate',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION mapping(Instate)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION mapping(Instate)_PRE_valueRange NOT VALIDATED')
	if contract_pre_post.check_fix_value_range(value='N', data_dictionary=mapping_Instate__input_dataDictionary_df, belong_op=Belong(0), field='Instate',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION mapping(Instate)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION mapping(Instate)_PRE_valueRange NOT VALIDATED')
	
	input_values_list=['Y', 'N']
	output_values_list=['1', '0']
	data_type_input_list=[DataType(0), DataType(0)]
	data_type_output_list=[DataType(0), DataType(0)]
	map_operation_list=[MapOperation(0), MapOperation(0)]
	
	mapping_Instate__output_dataDictionary_df=data_transformations.transform_fix_value_fix_value(data_dictionary=mapping_Instate__input_dataDictionary_df, input_values_list=input_values_list,
																  output_values_list=output_values_list,
							                                      data_type_input_list = data_type_input_list,
							                                      data_type_output_list = data_type_output_list,
																  map_operation_list = map_operation_list,
																  field_in = 'Instate', field_out = 'Instate')
	
	mapping_Instate__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/ruleEngine_instate_output_dataDictionary.parquet')
	mapping_Instate__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/ruleEngine_instate_output_dataDictionary.parquet')
	
	if contract_pre_post.check_fix_value_range(value='Y', data_dictionary=mapping_Instate__output_dataDictionary_df, belong_op=Belong(0), field='Instate',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION mapping(Instate)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION mapping(Instate)_POST_valueRange NOT VALIDATED')
	if contract_pre_post.check_fix_value_range(value='N', data_dictionary=mapping_Instate__output_dataDictionary_df, belong_op=Belong(0), field='Instate',
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION mapping(Instate)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION mapping(Instate)_POST_valueRange NOT VALIDATED')
	
	
	input_values_list_def_INV_condition=['Y', 'N']
	output_values_list_def_INV_condition=['1', '0']
	
	data_type_input_list_def_INV_condition=[DataType(0), DataType(0)]
	data_type_output_list_def_INV_condition=[DataType(0), DataType(0)]
	
	is_substring_list_def_INV_condition=[False, False]
	
	if contract_invariants.check_inv_fix_value_fix_value(data_dictionary_in=mapping_Instate__input_dataDictionary_df,
											data_dictionary_out=mapping_Instate__output_dataDictionary_df,
											input_values_list=input_values_list_def_INV_condition, 
											output_values_list=output_values_list_def_INV_condition,
											is_substring_list=is_substring_list_def_INV_condition,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											data_type_input_list=data_type_input_list_def_INV_condition,
											data_type_output_list=data_type_output_list_def_INV_condition,
											field_in='Instate', field_out='Instate'):
		print('INVARIANT mapping(Instate)_INV_condition VALIDATED')
	else:
		print('INVARIANT mapping(Instate)_INV_condition NOT VALIDATED')
	
	
	
	
	#-----------------New DataProcessing-----------------
	stringToNumber_TERRITORY_Instate__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/ruleEngine_instate_output_dataDictionary.parquet')

	stringToNumber_TERRITORY_Instate__input_dataDictionary_transformed=stringToNumber_TERRITORY_Instate__input_dataDictionary_df.copy()
	stringToNumber_TERRITORY_Instate__input_dataDictionary_transformed=data_transformations.transform_cast_type(data_dictionary=stringToNumber_TERRITORY_Instate__input_dataDictionary_transformed,
																	data_type_output= DataType(2),
																	field='TERRITORY')
	
	stringToNumber_TERRITORY_Instate__input_dataDictionary_transformed=data_transformations.transform_cast_type(data_dictionary=stringToNumber_TERRITORY_Instate__input_dataDictionary_transformed,
																	data_type_output= DataType(2),
																	field='Instate')
	
	stringToNumber_TERRITORY_Instate__output_dataDictionary_df=stringToNumber_TERRITORY_Instate__input_dataDictionary_transformed
	stringToNumber_TERRITORY_Instate__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/stringToNumber_output_dataDictionary.parquet')
	stringToNumber_TERRITORY_Instate__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/stringToNumber_output_dataDictionary.parquet')
	
	if contract_invariants.check_inv_missing_value_missing_value(data_dictionary_in=stringToNumber_TERRITORY_Instate__input_dataDictionary_df,
											data_dictionary_out=stringToNumber_TERRITORY_Instate__output_dataDictionary_df,
											belong_op_out=Belong(1), field_in='TERRITORY', field_out='TERRITORY'):
		print('INVARIANT INV_specialValue_condition_TERRITORY VALIDATED')
	else:
		print('INVARIANT INV_specialValue_condition_TERRITORY NOT VALIDATED')
	
	
	if contract_invariants.check_inv_cast_type(data_dictionary_in=stringToNumber_TERRITORY_Instate__input_dataDictionary_df,
								data_dictionary_out=stringToNumber_TERRITORY_Instate__output_dataDictionary_df,
								cast_type_in=DataType(0),
								cast_type_out=DataType(2),
								belong_op_out=Belong(0),
								field_in='TERRITORY', field_out='TERRITORY'):
		print('INVARIANT INV_castType_condition_TERRITORY VALIDATED')
	else:
		print('INVARIANT INV_castType_condition_TERRITORY NOT VALIDATED')
	
	
	
	if contract_invariants.check_inv_missing_value_missing_value(data_dictionary_in=stringToNumber_TERRITORY_Instate__input_dataDictionary_df,
											data_dictionary_out=stringToNumber_TERRITORY_Instate__output_dataDictionary_df,
											belong_op_out=Belong(1), field_in='Instate', field_out='Instate'):
		print('INVARIANT INV_specialValue_condition_Instate VALIDATED')
	else:
		print('INVARIANT INV_specialValue_condition_Instate NOT VALIDATED')
	
	
	if contract_invariants.check_inv_cast_type(data_dictionary_in=stringToNumber_TERRITORY_Instate__input_dataDictionary_df,
								data_dictionary_out=stringToNumber_TERRITORY_Instate__output_dataDictionary_df,
								cast_type_in=DataType(0),
								cast_type_out=DataType(2),
								belong_op_out=Belong(0),
								field_in='Instate', field_out='Instate'):
		print('INVARIANT INV_castType_condition_Instate VALIDATED')
	else:
		print('INVARIANT INV_castType_condition_Instate NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/stringToNumber_output_dataDictionary.parquet')

	if contract_pre_post.check_outliers(belong_op=Belong(0), data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df, field='avg_income', 
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION imputeOutlierByClosest(avg_income)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeOutlierByClosest(avg_income)_PRE_valueRange NOT VALIDATED')
	
	if contract_pre_post.check_outliers(belong_op=Belong(0), data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df, field='distance', 
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION imputeOutlierByClosest(distance)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeOutlierByClosest(distance)_PRE_valueRange NOT VALIDATED')
	
	if contract_pre_post.check_outliers(belong_op=Belong(0), data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df, field='Instate', 
									quant_abs=None, quant_rel=None, quant_op=None):
		print('PRECONDITION imputeOutlierByClosest(Instate)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION imputeOutlierByClosest(Instate)_PRE_valueRange NOT VALIDATED')
	
	imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df.copy()
	missing_values_list=[]
	
	imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed=data_transformations.transform_special_value_num_op(data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed,
																  special_type_input=SpecialType(2), num_op_output=Operation(3),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'avg_income', field_out = 'avg_income')
	
	missing_values_list=[]
	
	imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed=data_transformations.transform_special_value_num_op(data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed,
																  special_type_input=SpecialType(2), num_op_output=Operation(3),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'distance', field_out = 'distance')
	
	missing_values_list=[]
	
	imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed=data_transformations.transform_special_value_num_op(data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed,
																  special_type_input=SpecialType(2), num_op_output=Operation(3),
																  missing_values=missing_values_list,		
																  axis_param=0, field_in = 'Instate', field_out = 'Instate')
	
	imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_transformed
	imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericOutliers_output_dataDictionary.parquet')
	imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericOutliers_output_dataDictionary.parquet')
	
	if contract_pre_post.check_outliers(belong_op=Belong(0), data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df, field='avg_income', 
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeOutlierByClosest(avg_income)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeOutlierByClosest(avg_income)_POST_valueRange NOT VALIDATED')
	
	if contract_pre_post.check_outliers(belong_op=Belong(0), data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df, field='distance', 
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeOutlierByClosest(distance)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeOutlierByClosest(distance)_POST_valueRange NOT VALIDATED')
	
	if contract_pre_post.check_outliers(belong_op=Belong(0), data_dictionary=imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df, field='Instate', 
									quant_abs=None, quant_rel=None, quant_op=None):
		print('POSTCONDITION imputeOutlierByClosest(Instate)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION imputeOutlierByClosest(Instate)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_special_value_num_op(data_dictionary_in=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df,
											data_dictionary_out=imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											special_type_input=SpecialType(2),
											num_op_output=Operation(3),
											missing_values=None, axis_param=0, field_in='avg_income', field_out='avg_income'):
		print('INVARIANT imputeOutlierByClosest(avg_income)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeOutlierByClosest(avg_income)_INV_condition NOT VALIDATED')
	
	
	
	if contract_invariants.check_inv_special_value_num_op(data_dictionary_in=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df,
											data_dictionary_out=imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											special_type_input=SpecialType(2),
											num_op_output=Operation(3),
											missing_values=None, axis_param=0, field_in='distance', field_out='distance'):
		print('INVARIANT imputeOutlierByClosest(distance)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeOutlierByClosest(distance)_INV_condition NOT VALIDATED')
	
	
	
	if contract_invariants.check_inv_special_value_num_op(data_dictionary_in=imputeOutlierByClosest_avg_income_distance_Instate__input_dataDictionary_df,
											data_dictionary_out=imputeOutlierByClosest_avg_income_distance_Instate__output_dataDictionary_df,
											belong_op_in=Belong(0),
											belong_op_out=Belong(0),
											special_type_input=SpecialType(2),
											num_op_output=Operation(3),
											missing_values=None, axis_param=0, field_in='Instate', field_out='Instate'):
		print('INVARIANT imputeOutlierByClosest(Instate)_INV_condition VALIDATED')
	else:
		print('INVARIANT imputeOutlierByClosest(Instate)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	binner_satscore__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericOutliers_output_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_satscore__input_dataDictionary_df,
	                                	closure_type=Closure(3), belong_op=Belong(0), field='satscore'):
		print('PRECONDITION binner(satscore)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION binner(satscore)_PRE_valueRange NOT VALIDATED')
	
	binner_satscore__input_dataDictionary_transformed=binner_satscore__input_dataDictionary_df.copy()
	binner_satscore__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=binner_satscore__input_dataDictionary_transformed,
																  data_type_output = DataType(0),
																  field_in = 'satscore', field_out = 'satscore_binned')
	
	binner_satscore__output_dataDictionary_df=binner_satscore__input_dataDictionary_transformed
	binner_satscore__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_satscore__input_dataDictionary_transformed,
																  left_margin=-Infinity, right_margin=1040.0,
																  closure_type=Closure(1),
																  fix_value_output='54 Percentile and Under',
							                                      data_type_output = DataType(0),
																  field_in = 'satscore',
																  field_out = 'satscore_binned')
	
	binner_satscore__output_dataDictionary_df=binner_satscore__input_dataDictionary_transformed
	binner_satscore__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_satscore__input_dataDictionary_transformed,
																  left_margin=1040.0, right_margin=1160.0,
																  closure_type=Closure(0),
																  fix_value_output='55-75 Percentile',
							                                      data_type_output = DataType(0),
																  field_in = 'satscore',
																  field_out = 'satscore_binned')
	
	binner_satscore__output_dataDictionary_df=binner_satscore__input_dataDictionary_transformed
	binner_satscore__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_satscore__input_dataDictionary_transformed,
																  left_margin=1160.0, right_margin=1340.0,
																  closure_type=Closure(2),
																  fix_value_output='76-93 Percentile',
							                                      data_type_output = DataType(0),
																  field_in = 'satscore',
																  field_out = 'satscore_binned')
	
	binner_satscore__output_dataDictionary_df=binner_satscore__input_dataDictionary_transformed
	binner_satscore__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_satscore__input_dataDictionary_transformed,
																  left_margin=1340.0, right_margin=Infinity,
																  closure_type=Closure(2),
																  fix_value_output='94+ percentile',
							                                      data_type_output = DataType(0),
																  field_in = 'satscore',
																  field_out = 'satscore_binned')
	
	binner_satscore__output_dataDictionary_df=binner_satscore__input_dataDictionary_transformed
	binner_satscore__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_satscore__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	
	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_satscore__output_dataDictionary_df,
	                                	closure_type=Closure(0), belong_op=Belong(0), field='satscore_binned'):
		print('POSTCONDITION binner(satscore)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION binner(satscore)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_satscore__input_dataDictionary_df,
											data_dictionary_out=binner_satscore__output_dataDictionary_df,
											left_margin=-Infinity, right_margin=1040.0,
											closure_type=Closure(1),
											fix_value_output='54 Percentile and Under',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='satscore', field_out='satscore_binned'):
		print('INVARIANT binner(satscore)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(satscore)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_satscore__input_dataDictionary_df,
											data_dictionary_out=binner_satscore__output_dataDictionary_df,
											left_margin=1040.0, right_margin=1160.0,
											closure_type=Closure(0),
											fix_value_output='55-75 Percentile',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='satscore', field_out='satscore_binned'):
		print('INVARIANT binner(satscore)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(satscore)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_satscore__input_dataDictionary_df,
											data_dictionary_out=binner_satscore__output_dataDictionary_df,
											left_margin=1160.0, right_margin=1340.0,
											closure_type=Closure(2),
											fix_value_output='76-93 Percentile',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='satscore', field_out='satscore_binned'):
		print('INVARIANT binner(satscore)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(satscore)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_satscore__input_dataDictionary_df,
											data_dictionary_out=binner_satscore__output_dataDictionary_df,
											left_margin=1340.0, right_margin=Infinity,
											closure_type=Closure(2),
											fix_value_output='94+ percentile',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='satscore', field_out='satscore_binned'):
		print('INVARIANT binner(satscore)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(satscore)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	binner_TERRITORY__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_TERRITORY__input_dataDictionary_df,
	                                	closure_type=Closure(3), belong_op=Belong(0), field='TERRITORY'):
		print('PRECONDITION binner(TERRITORY)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION binner(TERRITORY)_PRE_valueRange NOT VALIDATED')
	
	binner_TERRITORY__input_dataDictionary_transformed=binner_TERRITORY__input_dataDictionary_df.copy()
	binner_TERRITORY__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=binner_TERRITORY__input_dataDictionary_transformed,
																  data_type_output = DataType(0),
																  field_in = 'TERRITORY', field_out = 'TERRITORY_binned')
	
	binner_TERRITORY__output_dataDictionary_df=binner_TERRITORY__input_dataDictionary_transformed
	binner_TERRITORY__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TERRITORY__input_dataDictionary_transformed,
																  left_margin=-Infinity, right_margin=1.0,
																  closure_type=Closure(0),
																  fix_value_output='Unknown',
							                                      data_type_output = DataType(0),
																  field_in = 'TERRITORY',
																  field_out = 'TERRITORY_binned')
	
	binner_TERRITORY__output_dataDictionary_df=binner_TERRITORY__input_dataDictionary_transformed
	binner_TERRITORY__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TERRITORY__input_dataDictionary_transformed,
																  left_margin=1.0, right_margin=3.0,
																  closure_type=Closure(2),
																  fix_value_output='Zone 1',
							                                      data_type_output = DataType(0),
																  field_in = 'TERRITORY',
																  field_out = 'TERRITORY_binned')
	
	binner_TERRITORY__output_dataDictionary_df=binner_TERRITORY__input_dataDictionary_transformed
	binner_TERRITORY__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TERRITORY__input_dataDictionary_transformed,
																  left_margin=3.0, right_margin=5.0,
																  closure_type=Closure(2),
																  fix_value_output='Zone 2',
							                                      data_type_output = DataType(0),
																  field_in = 'TERRITORY',
																  field_out = 'TERRITORY_binned')
	
	binner_TERRITORY__output_dataDictionary_df=binner_TERRITORY__input_dataDictionary_transformed
	binner_TERRITORY__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TERRITORY__input_dataDictionary_transformed,
																  left_margin=5.0, right_margin=7.0,
																  closure_type=Closure(2),
																  fix_value_output='Zone 3',
							                                      data_type_output = DataType(0),
																  field_in = 'TERRITORY',
																  field_out = 'TERRITORY_binned')
	
	binner_TERRITORY__output_dataDictionary_df=binner_TERRITORY__input_dataDictionary_transformed
	binner_TERRITORY__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TERRITORY__input_dataDictionary_transformed,
																  left_margin=7.0, right_margin=Infinity,
																  closure_type=Closure(2),
																  fix_value_output='Zone 4',
							                                      data_type_output = DataType(0),
																  field_in = 'TERRITORY',
																  field_out = 'TERRITORY_binned')
	
	binner_TERRITORY__output_dataDictionary_df=binner_TERRITORY__input_dataDictionary_transformed
	binner_TERRITORY__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TERRITORY__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	
	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_TERRITORY__output_dataDictionary_df,
	                                	closure_type=Closure(0), belong_op=Belong(0), field='TERRITORY_binned'):
		print('POSTCONDITION binner(TERRITORY)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION binner(TERRITORY)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TERRITORY__input_dataDictionary_df,
											data_dictionary_out=binner_TERRITORY__output_dataDictionary_df,
											left_margin=-Infinity, right_margin=1.0,
											closure_type=Closure(0),
											fix_value_output='Unknown',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TERRITORY', field_out='TERRITORY_binned'):
		print('INVARIANT binner(TERRITORY)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TERRITORY)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TERRITORY__input_dataDictionary_df,
											data_dictionary_out=binner_TERRITORY__output_dataDictionary_df,
											left_margin=1.0, right_margin=3.0,
											closure_type=Closure(2),
											fix_value_output='Zone 1',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TERRITORY', field_out='TERRITORY_binned'):
		print('INVARIANT binner(TERRITORY)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TERRITORY)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TERRITORY__input_dataDictionary_df,
											data_dictionary_out=binner_TERRITORY__output_dataDictionary_df,
											left_margin=3.0, right_margin=5.0,
											closure_type=Closure(2),
											fix_value_output='Zone 2',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TERRITORY', field_out='TERRITORY_binned'):
		print('INVARIANT binner(TERRITORY)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TERRITORY)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TERRITORY__input_dataDictionary_df,
											data_dictionary_out=binner_TERRITORY__output_dataDictionary_df,
											left_margin=5.0, right_margin=7.0,
											closure_type=Closure(2),
											fix_value_output='Zone 3',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TERRITORY', field_out='TERRITORY_binned'):
		print('INVARIANT binner(TERRITORY)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TERRITORY)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TERRITORY__input_dataDictionary_df,
											data_dictionary_out=binner_TERRITORY__output_dataDictionary_df,
											left_margin=7.0, right_margin=Infinity,
											closure_type=Closure(2),
											fix_value_output='Zone 4',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TERRITORY', field_out='TERRITORY_binned'):
		print('INVARIANT binner(TERRITORY)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TERRITORY)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	binner_avg_income__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_avg_income__input_dataDictionary_df,
	                                	closure_type=Closure(3), belong_op=Belong(0), field='avg_income'):
		print('PRECONDITION binner(avg_income)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION binner(avg_income)_PRE_valueRange NOT VALIDATED')
	
	binner_avg_income__input_dataDictionary_transformed=binner_avg_income__input_dataDictionary_df.copy()
	binner_avg_income__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=binner_avg_income__input_dataDictionary_transformed,
																  data_type_output = DataType(0),
																  field_in = 'avg_income', field_out = 'avg_income_binned')
	
	binner_avg_income__output_dataDictionary_df=binner_avg_income__input_dataDictionary_transformed
	binner_avg_income__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_avg_income__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_avg_income__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_avg_income__input_dataDictionary_transformed,
																  left_margin=-Infinity, right_margin=42830.0,
																  closure_type=Closure(0),
																  fix_value_output='low',
							                                      data_type_output = DataType(0),
																  field_in = 'avg_income',
																  field_out = 'avg_income_binned')
	
	binner_avg_income__output_dataDictionary_df=binner_avg_income__input_dataDictionary_transformed
	binner_avg_income__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_avg_income__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_avg_income__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_avg_income__input_dataDictionary_transformed,
																  left_margin=42830.0, right_margin=55559.0,
																  closure_type=Closure(2),
																  fix_value_output='Moderate',
							                                      data_type_output = DataType(0),
																  field_in = 'avg_income',
																  field_out = 'avg_income_binned')
	
	binner_avg_income__output_dataDictionary_df=binner_avg_income__input_dataDictionary_transformed
	binner_avg_income__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_avg_income__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_avg_income__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_avg_income__input_dataDictionary_transformed,
																  left_margin=55559.0, right_margin=Infinity,
																  closure_type=Closure(2),
																  fix_value_output='High',
							                                      data_type_output = DataType(0),
																  field_in = 'avg_income',
																  field_out = 'avg_income_binned')
	
	binner_avg_income__output_dataDictionary_df=binner_avg_income__input_dataDictionary_transformed
	binner_avg_income__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_avg_income__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	
	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_avg_income__output_dataDictionary_df,
	                                	closure_type=Closure(0), belong_op=Belong(0), field='avg_income_binned'):
		print('POSTCONDITION binner(avg_income)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION binner(avg_income)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_avg_income__input_dataDictionary_df,
											data_dictionary_out=binner_avg_income__output_dataDictionary_df,
											left_margin=-Infinity, right_margin=42830.0,
											closure_type=Closure(0),
											fix_value_output='low',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='avg_income', field_out='avg_income_binned'):
		print('INVARIANT binner(avg_income)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(avg_income)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_avg_income__input_dataDictionary_df,
											data_dictionary_out=binner_avg_income__output_dataDictionary_df,
											left_margin=42830.0, right_margin=55559.0,
											closure_type=Closure(2),
											fix_value_output='Moderate',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='avg_income', field_out='avg_income_binned'):
		print('INVARIANT binner(avg_income)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(avg_income)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_avg_income__input_dataDictionary_df,
											data_dictionary_out=binner_avg_income__output_dataDictionary_df,
											left_margin=55559.0, right_margin=Infinity,
											closure_type=Closure(2),
											fix_value_output='High',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='avg_income', field_out='avg_income_binned'):
		print('INVARIANT binner(avg_income)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(avg_income)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	binner_TOTAL_CONTACTS__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_TOTAL_CONTACTS__input_dataDictionary_df,
	                                	closure_type=Closure(3), belong_op=Belong(0), field='TOTAL_CONTACTS'):
		print('PRECONDITION binner(TOTAL_CONTACTS)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION binner(TOTAL_CONTACTS)_PRE_valueRange NOT VALIDATED')
	
	binner_TOTAL_CONTACTS__input_dataDictionary_transformed=binner_TOTAL_CONTACTS__input_dataDictionary_df.copy()
	binner_TOTAL_CONTACTS__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=binner_TOTAL_CONTACTS__input_dataDictionary_transformed,
																  data_type_output = DataType(0),
																  field_in = 'TOTAL_CONTACTS', field_out = 'TOTAL_CONTACTS_binned')
	
	binner_TOTAL_CONTACTS__output_dataDictionary_df=binner_TOTAL_CONTACTS__input_dataDictionary_transformed
	binner_TOTAL_CONTACTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TOTAL_CONTACTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TOTAL_CONTACTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TOTAL_CONTACTS__input_dataDictionary_transformed,
																  left_margin=-Infinity, right_margin=1.0,
																  closure_type=Closure(0),
																  fix_value_output='Low',
							                                      data_type_output = DataType(0),
																  field_in = 'TOTAL_CONTACTS',
																  field_out = 'TOTAL_CONTACTS_binned')
	
	binner_TOTAL_CONTACTS__output_dataDictionary_df=binner_TOTAL_CONTACTS__input_dataDictionary_transformed
	binner_TOTAL_CONTACTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TOTAL_CONTACTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TOTAL_CONTACTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TOTAL_CONTACTS__input_dataDictionary_transformed,
																  left_margin=1.0, right_margin=4.0,
																  closure_type=Closure(2),
																  fix_value_output='Moderate',
							                                      data_type_output = DataType(0),
																  field_in = 'TOTAL_CONTACTS',
																  field_out = 'TOTAL_CONTACTS_binned')
	
	binner_TOTAL_CONTACTS__output_dataDictionary_df=binner_TOTAL_CONTACTS__input_dataDictionary_transformed
	binner_TOTAL_CONTACTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TOTAL_CONTACTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TOTAL_CONTACTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_TOTAL_CONTACTS__input_dataDictionary_transformed,
																  left_margin=4.0, right_margin=Infinity,
																  closure_type=Closure(2),
																  fix_value_output='High',
							                                      data_type_output = DataType(0),
																  field_in = 'TOTAL_CONTACTS',
																  field_out = 'TOTAL_CONTACTS_binned')
	
	binner_TOTAL_CONTACTS__output_dataDictionary_df=binner_TOTAL_CONTACTS__input_dataDictionary_transformed
	binner_TOTAL_CONTACTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_TOTAL_CONTACTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	
	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_TOTAL_CONTACTS__output_dataDictionary_df,
	                                	closure_type=Closure(0), belong_op=Belong(0), field='TOTAL_CONTACTS_binned'):
		print('POSTCONDITION binner(TOTAL_CONTACTS)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION binner(TOTAL_CONTACTS)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TOTAL_CONTACTS__input_dataDictionary_df,
											data_dictionary_out=binner_TOTAL_CONTACTS__output_dataDictionary_df,
											left_margin=-Infinity, right_margin=1.0,
											closure_type=Closure(0),
											fix_value_output='Low',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TOTAL_CONTACTS', field_out='TOTAL_CONTACTS_binned'):
		print('INVARIANT binner(TOTAL_CONTACTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TOTAL_CONTACTS)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TOTAL_CONTACTS__input_dataDictionary_df,
											data_dictionary_out=binner_TOTAL_CONTACTS__output_dataDictionary_df,
											left_margin=1.0, right_margin=4.0,
											closure_type=Closure(2),
											fix_value_output='Moderate',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TOTAL_CONTACTS', field_out='TOTAL_CONTACTS_binned'):
		print('INVARIANT binner(TOTAL_CONTACTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TOTAL_CONTACTS)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_TOTAL_CONTACTS__input_dataDictionary_df,
											data_dictionary_out=binner_TOTAL_CONTACTS__output_dataDictionary_df,
											left_margin=4.0, right_margin=Infinity,
											closure_type=Closure(2),
											fix_value_output='High',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='TOTAL_CONTACTS', field_out='TOTAL_CONTACTS_binned'):
		print('INVARIANT binner(TOTAL_CONTACTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(TOTAL_CONTACTS)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	binner_SOLICITED_CNTCTS__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_SOLICITED_CNTCTS__input_dataDictionary_df,
	                                	closure_type=Closure(3), belong_op=Belong(0), field='SOLICITED_CNTCTS'):
		print('PRECONDITION binner(SOLICITED_CNTCTS)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION binner(SOLICITED_CNTCTS)_PRE_valueRange NOT VALIDATED')
	
	binner_SOLICITED_CNTCTS__input_dataDictionary_transformed=binner_SOLICITED_CNTCTS__input_dataDictionary_df.copy()
	binner_SOLICITED_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed,
																  data_type_output = DataType(0),
																  field_in = 'SOLICITED_CNTCTS', field_out = 'SOLICITED_CNTCTS_binned')
	
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed
	binner_SOLICITED_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SOLICITED_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed,
																  left_margin=-Infinity, right_margin=1.0,
																  closure_type=Closure(0),
																  fix_value_output='Low',
							                                      data_type_output = DataType(0),
																  field_in = 'SOLICITED_CNTCTS',
																  field_out = 'SOLICITED_CNTCTS_binned')
	
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed
	binner_SOLICITED_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SOLICITED_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed,
																  left_margin=1.0, right_margin=4.0,
																  closure_type=Closure(2),
																  fix_value_output='Moderate',
							                                      data_type_output = DataType(0),
																  field_in = 'SOLICITED_CNTCTS',
																  field_out = 'SOLICITED_CNTCTS_binned')
	
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed
	binner_SOLICITED_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SOLICITED_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed,
																  left_margin=4.0, right_margin=Infinity,
																  closure_type=Closure(2),
																  fix_value_output='High',
							                                      data_type_output = DataType(0),
																  field_in = 'SOLICITED_CNTCTS',
																  field_out = 'SOLICITED_CNTCTS_binned')
	
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=binner_SOLICITED_CNTCTS__input_dataDictionary_transformed
	binner_SOLICITED_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SOLICITED_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	
	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_SOLICITED_CNTCTS__output_dataDictionary_df,
	                                	closure_type=Closure(0), belong_op=Belong(0), field='SOLICITED_CNTCTS_binned'):
		print('POSTCONDITION binner(SOLICITED_CNTCTS)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION binner(SOLICITED_CNTCTS)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_SOLICITED_CNTCTS__input_dataDictionary_df,
											data_dictionary_out=binner_SOLICITED_CNTCTS__output_dataDictionary_df,
											left_margin=-Infinity, right_margin=1.0,
											closure_type=Closure(0),
											fix_value_output='Low',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='SOLICITED_CNTCTS', field_out='SOLICITED_CNTCTS_binned'):
		print('INVARIANT binner(SOLICITED_CNTCTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(SOLICITED_CNTCTS)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_SOLICITED_CNTCTS__input_dataDictionary_df,
											data_dictionary_out=binner_SOLICITED_CNTCTS__output_dataDictionary_df,
											left_margin=1.0, right_margin=4.0,
											closure_type=Closure(2),
											fix_value_output='Moderate',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='SOLICITED_CNTCTS', field_out='SOLICITED_CNTCTS_binned'):
		print('INVARIANT binner(SOLICITED_CNTCTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(SOLICITED_CNTCTS)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_SOLICITED_CNTCTS__input_dataDictionary_df,
											data_dictionary_out=binner_SOLICITED_CNTCTS__output_dataDictionary_df,
											left_margin=4.0, right_margin=Infinity,
											closure_type=Closure(2),
											fix_value_output='High',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='SOLICITED_CNTCTS', field_out='SOLICITED_CNTCTS_binned'):
		print('INVARIANT binner(SOLICITED_CNTCTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(SOLICITED_CNTCTS)_INV_condition NOT VALIDATED')
	
	
	
	#-----------------New DataProcessing-----------------
	binner_SELF_INIT_CNTCTS__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')

	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_SELF_INIT_CNTCTS__input_dataDictionary_df,
	                                	closure_type=Closure(3), belong_op=Belong(0), field='SELF_INIT_CNTCTS'):
		print('PRECONDITION binner(SELF_INIT_CNTCTS)_PRE_valueRange VALIDATED')
	else:
		print('PRECONDITION binner(SELF_INIT_CNTCTS)_PRE_valueRange NOT VALIDATED')
	
	binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed=binner_SELF_INIT_CNTCTS__input_dataDictionary_df.copy()
	binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed,
																  data_type_output = DataType(0),
																  field_in = 'SELF_INIT_CNTCTS', field_out = 'SELF_INIT_CNTCTS_binned')
	
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed,
																  left_margin=-Infinity, right_margin=1.0,
																  closure_type=Closure(0),
																  fix_value_output='Low',
							                                      data_type_output = DataType(0),
																  field_in = 'SELF_INIT_CNTCTS',
																  field_out = 'SELF_INIT_CNTCTS_binned')
	
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed,
																  left_margin=1.0, right_margin=4.0,
																  closure_type=Closure(2),
																  fix_value_output='Moderate',
							                                      data_type_output = DataType(0),
																  field_in = 'SELF_INIT_CNTCTS',
																  field_out = 'SELF_INIT_CNTCTS_binned')
	
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed=data_transformations.transform_interval_fix_value(data_dictionary=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed,
																  left_margin=4.0, right_margin=Infinity,
																  closure_type=Closure(2),
																  fix_value_output='High',
							                                      data_type_output = DataType(0),
																  field_in = 'SELF_INIT_CNTCTS',
																  field_out = 'SELF_INIT_CNTCTS_binned')
	
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=binner_SELF_INIT_CNTCTS__input_dataDictionary_transformed
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	binner_SELF_INIT_CNTCTS__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/numericBinner_output_dataDictionary.parquet')
	
	if contract_pre_post.check_interval_range_float(left_margin=0.0, right_margin=1000.0, data_dictionary=binner_SELF_INIT_CNTCTS__output_dataDictionary_df,
	                                	closure_type=Closure(0), belong_op=Belong(0), field='SELF_INIT_CNTCTS_binned'):
		print('POSTCONDITION binner(SELF_INIT_CNTCTS)_POST_valueRange VALIDATED')
	else:
		print('POSTCONDITION binner(SELF_INIT_CNTCTS)_POST_valueRange NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_SELF_INIT_CNTCTS__input_dataDictionary_df,
											data_dictionary_out=binner_SELF_INIT_CNTCTS__output_dataDictionary_df,
											left_margin=-Infinity, right_margin=1.0,
											closure_type=Closure(0),
											fix_value_output='Low',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='SELF_INIT_CNTCTS', field_out='SELF_INIT_CNTCTS_binned'):
		print('INVARIANT binner(SELF_INIT_CNTCTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(SELF_INIT_CNTCTS)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_SELF_INIT_CNTCTS__input_dataDictionary_df,
											data_dictionary_out=binner_SELF_INIT_CNTCTS__output_dataDictionary_df,
											left_margin=1.0, right_margin=4.0,
											closure_type=Closure(2),
											fix_value_output='Moderate',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='SELF_INIT_CNTCTS', field_out='SELF_INIT_CNTCTS_binned'):
		print('INVARIANT binner(SELF_INIT_CNTCTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(SELF_INIT_CNTCTS)_INV_condition NOT VALIDATED')
	
	if contract_invariants.check_inv_interval_fix_value(data_dictionary_in=binner_SELF_INIT_CNTCTS__input_dataDictionary_df,
											data_dictionary_out=binner_SELF_INIT_CNTCTS__output_dataDictionary_df,
											left_margin=4.0, right_margin=Infinity,
											closure_type=Closure(2),
											fix_value_output='High',
											belong_op_in=Belong(0), belong_op_out=Belong(0),
											data_type_output=DataType(0),
											field_in='SELF_INIT_CNTCTS', field_out='SELF_INIT_CNTCTS_binned'):
		print('INVARIANT binner(SELF_INIT_CNTCTS)_INV_condition VALIDATED')
	else:
		print('INVARIANT binner(SELF_INIT_CNTCTS)_INV_condition NOT VALIDATED')
	
	
	
















set_logger("dataProcessing")
generateWorkflow()
