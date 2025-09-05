import pandas as pd
import numpy as np
import functions.data_transformations as data_transformations
import functions.data_smells as data_smells
from helpers.enumerations import Belong, Operator, Operation, SpecialType, DataType, DerivedType, Closure, FilterType, MapOperation, MathOperator
from helpers.logger import set_logger
import pyarrow
from functions.PMML import PMMLModel

def generateWorkflow():
	#-----------------New DataProcessing-----------------
	mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/mathOperation_input_dataDictionary.parquet')

	
	common_invalid_list=['inf', '-inf', 'nan']
	common_missing_list=['', '?', '.','null','none','na']
	
	
	data_smells.check_missing_invalid_value_consistency(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, 
														missing_invalid_list=[], common_missing_invalid_list=common_missing_list, field='Latitude', origin_function="Math Formula")
	
	data_smells.check_missing_invalid_value_consistency(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, 
														missing_invalid_list=[], common_missing_invalid_list=common_missing_list, field='Altitude', origin_function="Math Formula")
	
	data_smells.check_integer_as_floating_point(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Latitude', origin_function="Math Formula")
	data_smells.check_types_as_string(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Latitude', expected_type=DataType.DOUBLE, origin_function="Math Formula")
	data_smells.check_suspect_precision(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Latitude', origin_function="Math Formula")
	data_smells.check_date_as_datetime(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Latitude', origin_function="Math Formula")
	data_smells.check_ambiguous_datetime_format(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Latitude', origin_function="Math Formula")
	data_smells.check_suspect_distribution(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, min_value=440.0, max_value=1600.0, field='Latitude', origin_function="Math Formula")
	data_smells.check_intermingled_data_type(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Latitude', origin_function="Math Formula")
	data_smells.check_separating_consistency(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, decimal_sep='.',  field='Latitude', origin_function="Math Formula")
			
	data_smells.check_integer_as_floating_point(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Altitude', origin_function="Math Formula")
	data_smells.check_types_as_string(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Altitude', expected_type=DataType.DOUBLE, origin_function="Math Formula")
	data_smells.check_suspect_precision(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Altitude', origin_function="Math Formula")
	data_smells.check_date_as_datetime(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Altitude', origin_function="Math Formula")
	data_smells.check_ambiguous_datetime_format(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Altitude', origin_function="Math Formula")
	data_smells.check_suspect_distribution(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, min_value=440.0, max_value=1600.0, field='Altitude', origin_function="Math Formula")
	data_smells.check_intermingled_data_type(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, field='Altitude', origin_function="Math Formula")
	data_smells.check_separating_consistency(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df, decimal_sep='.',  field='Altitude', origin_function="Math Formula")
			
	

	mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_transformed=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_df.copy()
	mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_transformed=data_transformations.transform_derived_field(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_transformed,
																  data_type_output = DataType(5),
																  field_in = 'Latitude', field_out = 'Difference in Latitude/Altitude')
	
	mathOperation_Difference_in_Latitude_Altitude__output_dataDictionary_df=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_transformed
	mathOperation_Difference_in_Latitude_Altitude__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/mathOperation_output_dataDictionary.parquet')
	mathOperation_Difference_in_Latitude_Altitude__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/mathOperation_output_dataDictionary.parquet')
	mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_transformed=data_transformations.transform_math_operation(data_dictionary=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_transformed,
																math_op=MathOperator(1), field_out='Difference in Latitude/Altitude',
																first_operand='Latitude', is_field_first=True,second_operand='Altitude', is_field_second=True)
	
	mathOperation_Difference_in_Latitude_Altitude__output_dataDictionary_df=mathOperation_Difference_in_Latitude_Altitude__input_dataDictionary_transformed
	mathOperation_Difference_in_Latitude_Altitude__output_dataDictionary_df.to_parquet('/wf_validation_python/data/output/mathOperation_output_dataDictionary.parquet')
	mathOperation_Difference_in_Latitude_Altitude__output_dataDictionary_df=pd.read_parquet('/wf_validation_python/data/output/mathOperation_output_dataDictionary.parquet')
	

set_logger("transformations")
generateWorkflow()
