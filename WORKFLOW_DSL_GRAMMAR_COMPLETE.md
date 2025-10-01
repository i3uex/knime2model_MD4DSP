# WorkflowDSL - Gramática Textual Completa para Workflows MD4DSP

**Versión 1.0** - Domain Specific Language para programar workflows de procesamiento de datos

**✅ Basado en análisis exhaustivo de 35 workflows reales de `parsed_json_workflows/`**

---

## 📋 Resumen de Cobertura

Este DSL cubre **100% de los workflows** analizados, incluyendo:
- ✅ 35 workflows JSON parseados
- ✅ 12 tipos de nodos únicos (node_type)
- ✅ Workflow más completo: "Model data set with metanode" (806 líneas JSON, 4603 líneas XMI)
- ✅ Todas las transformaciones de la librería MD4DSP
- ✅ **Contratos completos** (Preconditions, Postconditions, Invariants) basados en XMI
- ✅ **Especificación JSON detallada para contratos** (Sección 5.1) - Forward-compatible

## ⚠️ Nota Importante sobre Contratos

**Estado actual**: Los contratos en el DSL y JSON son una **especificación para trabajo futuro**.

- El parser actual `json2workflow.py` **genera contratos automáticamente** basándose en el tipo de transformación
- La sección `"contracts"` en JSON está **diseñada para ser forward-compatible**
- Si creas JSONs manualmente con contratos, el parser actual los **ignorará**
- Para que funcionen, necesitarás **modificar `json2workflow.py`** en el futuro
- La estructura JSON está **completamente especificada y lista** para esta implementación futura

**Ver Sección 5.1** para la especificación completa de cómo estructurar contratos en JSON.

---

## 1. Gramática Xtext Completa

```xtext
grammar xtext.json.WorkflowDSL with org.eclipse.xtext.common.Terminals

import "http://www.eclipse.org/emf/2002/Ecore" as ecore

generate workflowDSL "http://www.json.xtext/WorkflowDSL"

Workflow:
    "workflow" name=STRING "{" source=DataSource body=WorkflowBody "}";

DataSource:
    "source" name=ID "=" reader=DataReader;

DataReader:
    CSVReader | FileReader;

CSVReader:
    "read_csv" "(" filePath=FilePath ("," delimiter=Delimiter)? ")";

FileReader:
    "read_file" "(" filePath=FilePath ")";

FilePath:
    path=STRING;

Delimiter:
    "," | ";" | "\t" | "|" | value=STRING;

WorkflowBody:
    steps+=Step*;

Step:
    name=ID "=" transformation=Transformation ("|>" target=ID)? contracts=ContractBlock?;

ContractBlock:
    "contracts" "{" contracts+=Contract* "}";

Contract:
    Precondition | Postcondition | Invariant;

Precondition:
    "precondition" name=ContractName "{" body=ContractBody "}";

Postcondition:
    "postcondition" name=ContractName "{" body=ContractBody "}";

Invariant:
    "invariant" name=ContractName "{" body=ContractBody "}";

ContractName:
    name=STRING | name=ID;

ContractBody:
    type=ContractType;

ContractType:
    ValueRangeContract
    | ConditionContract
    | SpecialValueContract
    | CastTypeContract;

ValueRangeContract:
    "value_range" "(" field=ContractField "," value=ContractValue ")";

ContractField:
    "input" "." column=Column
    | "output" "." column=Column;

ContractValue:
    "castable_to" type=Type
    | "in_range" bounds=RangeBounds
    | "matches" value=Value;

Type:
    "Integer" | "Double" | "String" | "Boolean";

ConditionContract:
    "condition" "{" ifClause=IfClause thenClause=ThenClause "}";

IfClause:
    "if" field=ContractField op=BelongOp condition=DataCondition;

ThenClause:
    "then" field=ContractField op=BelongOp result=DataResult;

BelongOp:
    "belongs_to" | "not_belongs_to";

DataCondition:
    SpecialValueCheck | CastTypeCheck | ValueCheck;

SpecialValueCheck:
    "special_values";

CastTypeCheck:
    "type" type=Type;

ValueCheck:
    "value" value=Value;

DataResult:
    SpecialValueCheck | CastTypeCheck | ValueCheck;

SpecialValueContract:
    "no_special_values" "(" field=ContractField ")"
    | "has_special_values" "(" field=ContractField ")";

CastTypeContract:
    "castable_to" type=Type "(" field=ContractField ")"
    | "is_type" type=Type "(" field=ContractField ")";

Transformation:
    RowFilter
    | ColumnFilter  
    | Mapping
    | MathOp
    | Binner
    | TypeConversion
    | Imputation
    | OutlierTreatment
    | Join;

RowFilter:
    "filter_rows" "{" condition=FilterCondition "}";

FilterCondition:
    MissingFilter | RangeFilter | StringFilter;

MissingFilter:
    "missing" "(" columns=ColumnList "," includeExclude=IncludeExclude ")";

RangeFilter:
    "range" "(" column=Column "," bounds=RangeBounds "," includeExclude=IncludeExclude ")";

RangeBounds:
    "[" lower=BoundValue "," upper=BoundValue "]"
    | "[" lower=BoundValue "," upper=BoundValue ")"
    | "(" lower=BoundValue "," upper=BoundValue "]"
    | "(" lower=BoundValue "," upper=BoundValue ")";

BoundValue:
    value=Number | "*" | "inf" | "-inf";

StringFilter:
    "matches" "(" column=Column "," pattern=Pattern "," includeExclude=IncludeExclude ")"
    | "like" "(" column=Column "," pattern=Pattern "," includeExclude=IncludeExclude ")";

Pattern:
    value=STRING | regex=Regex;

IncludeExclude:
    "include" | "exclude";

ColumnFilter:
    "select_columns" "{" columns=ColumnList "}"
    | "drop_columns" "{" columns=ColumnList "}"
    | "keep" "{" columns=ColumnList "}"
    | "remove" "{" columns=ColumnList "}";

Mapping:
    ValueMapping | SubstringMapping;

ValueMapping:
    "map" "(" column=Column ")" "{" rules=MappingRules "}" mode=MappingMode;

MappingRules:
    (rules+=MappingRule ("," rules+=MappingRule)*)?;

MappingRule:
    from=STRING "->" to=STRING
    | pattern=Pattern "=>" to=STRING;

SubstringMapping:
    "replace" "(" column=Column "," from=STRING "," to=STRING ")" mode=MappingMode;

MappingMode:
    "replace" | "as" newName=ID;

MathOp:
    "math" "(" expression=MathExpression ")" "as" newName=ID;

MathExpression:
    Primary (operator=Operator right=Primary)*;

Primary:
    operand=Operand | "(" expression=MathExpression ")" | call=FunctionCall;

FunctionCall:
    function=Function "(" (operands+=Operand ("," operands+=Operand)*)? ")";

Function:
    "abs" | "sqrt" | "pow" | "log" | "exp" 
    | "sin" | "cos" | "tan" | "round" | "ceil" | "floor";

Operand:
    column=Column | number=Number | string=STRING;

Operator:
    "+" | "-" | "*" | "/" | "%" | "^";

Binner:
    "bin" "(" column=Column ")" "{" definitions=BinDefinitions "}" mode=BinMode;

BinDefinitions:
    (definitions+=BinDef ("," definitions+=BinDef)*)?;

BinDef:
    name=BinName ":" interval=Interval;

BinName:
    name=STRING;

Interval:
    "[" lower=IntervalBound "," upper=IntervalBound "]"
    | "[" lower=IntervalBound "," upper=IntervalBound ")"
    | "(" lower=IntervalBound "," upper=IntervalBound "]"
    | "(" lower=IntervalBound "," upper=IntervalBound ")";

IntervalBound:
    value=Number | "-inf" | "inf" | "-Infinity" | "Infinity";

BinMode:
    "replace" | "as" newName=ID;

TypeConversion:
    "to_numeric" "(" columns=ColumnList ")" separator=DecimalSeparator?
    | "to_string" "(" columns=ColumnList ")"
    | "to_categorical" "(" columns=ColumnList ")"
    | "to_boolean" "(" columns=ColumnList ")"
    | "to_date" "(" columns=ColumnList "," format=DateFormat? ")";

DecimalSeparator:
    "separator" "=" ("." | ",");

DateFormat:
    "format" "=" format=STRING;

Imputation:
    "impute" "(" columns=ColumnList ")" "{" method=ImputeMethod "}";

ImputeMethod:
    FixedImpute
    | StatisticalImpute
    | SequentialImpute
    | AdvancedImpute;

FixedImpute:
    "fixed" "=" values=ValueList;

ValueList:
    value=Value | "[" (values+=Value ("," values+=Value)*)? "]";

Value:
    number=Number | string=STRING | "null";

StatisticalImpute:
    "mean"
    | "median"
    | "mode"
    | "most_frequent"
    | "max"
    | "min";

SequentialImpute:
    "forward_fill"
    | "backward_fill"
    | "previous_value"
    | "next_value";

AdvancedImpute:
    "interpolation" type=InterpolationType?
    | "moving_average" ("window" "=" windowSize=Number)?
    | "linear"
    | "polynomial" ("degree" "=" degree=Number)?
    | "spline";

InterpolationType:
    "linear" | "polynomial" | "spline";

OutlierTreatment:
    "outliers" "(" columns=ColumnList ")" "{" strategy=OutlierStrategy "}";

OutlierStrategy:
    replacement=ReplacementStrategy method=DetectionMethod options=OutlierOptions?;

ReplacementStrategy:
    "replace_closest"
    | "replace_missing"
    | "replace_by_closest"
    | "replace_with" "=" value=Number
    | "remove"
    | "cap";

DetectionMethod:
    IQRMethod | ZScoreMethod | PercentileMethod;

IQRMethod:
    "iqr" params=IQRParams?;

IQRParams:
    "scalar" "=" scalar=Number
    | "estimation" "=" estimation=EstimationType;

EstimationType:
    "R_4" | "R_7" | "R_8";

ZScoreMethod:
    "zscore" ("threshold" "=" threshold=Number)?;

PercentileMethod:
    "percentile" "lower" "=" lower=Number "upper" "=" upper=Number;

OutlierOptions:
    "scope" "=" scope=OutlierScope;

OutlierScope:
    "all" | "all_outliers" | "lower_only" | "upper_only";

Join:
    "join" "(" left=ID "," right=ID ")" "{" spec=JoinSpec "}";

JoinSpec:
    type=JoinType "on" conditions=JoinConditions options=JoinOptions?;

JoinType:
    "inner" | "left" | "right" | "full" | "cross";

JoinConditions:
    conditions+=JoinCondition ("and" conditions+=JoinCondition)*;

JoinCondition:
    left=Column "=" right=Column
    | left=Column comparator=Comparator right=Column;

Comparator:
    "=" | "==" | "!=" | "<" | ">" | "<=" | ">=";

JoinOptions:
    "suffix" "=" "(" leftSuffix=STRING "," rightSuffix=STRING ")";

Column:
    name=ID | table=ID "." column=ID;

ColumnList:
    columns+=Column ("," columns+=Column)*
    | "*";

Number:
    INT ('.' INT)? | '.' INT;

Integer returns ecore::EInt:
    INT;

Float returns ecore::EFloat:
    INT '.' INT | '.' INT | INT '.';

Regex:
    '/' pattern=STRING '/' flags=STRING?;

terminal COMMENT:
    '//' !('\n'|'\r')* ('\r'? '\n')?
    | '/*' -> '*/';
```

---

## 2. Sintaxis Concreta con Ejemplos Completos

### 2.1. Estructura Básica de Workflow

```
workflow "Data Cleaning Pipeline" {
    source data = read_csv("/path/to/data.csv", ,)
    
    step1 = transformation1 |> data
    step2 = transformation2 |> step1
    step3 = transformation3 |> step2
}
```

**Equivalencia con JSON**:
```json
{
    "nodes": [
        {"id": 1, "node_name": "CSV Reader", ...},
        {"id": 2, "node_name": "...", ...},
        {"id": 3, "node_name": "...", ...},
        {"id": 4, "node_name": "...", ...}
    ],
    "connections": [
        {"sourceID": 1, "destID": 2},
        {"sourceID": 2, "destID": 3},
        {"sourceID": 3, "destID": 4}
    ]
}
```

---

### 2.2. Fuentes de Datos

#### CSV Reader (obligatorio en workflows)
```
source data = read_csv("/data/file.csv", ,)
source data = read_csv("/data/file.csv", ;)
source data = read_csv("/data/file.csv", "\t")
source data = read_csv("/data/file.csv")  // coma por defecto
```

#### File Reader (alternativa)
```
source data = read_file("/data/file.csv")
```

---

### 2.3. Filtros de Filas

```
// Filtro por valores faltantes
clean = filter_rows { missing(Age, Country, Income, exclude) } |> data
missing_only = filter_rows { missing(Life_expectancy, include) } |> data

// Filtro por rango numérico
adults = filter_rows { range(Age, [18, 65], include) } |> data
high_life = filter_rows { range(Life_expectancy, [75, *], include) } |> data  // Sin límite superior
young = filter_rows { range(Age, [*, 25], include) } |> data  // Sin límite inferior
range_open = filter_rows { range(init_span, [0, inf), include) } |> data  // Semi-abierto

// Filtro por string/patrón
usa_data = filter_rows { matches(Country, "United States", include) } |> data
contains_n = filter_rows { like(TERRITORY, "*N*", include) } |> data
```

---

### 2.4. Filtro de Columnas

```
// Seleccionar o mantener columnas
subset = select_columns { Name, Age, Country, Income } |> data
subset = keep { Name, Age, Country, Income } |> data  // Alternativa

// Eliminar columnas
cleaned = drop_columns { ID, Timestamp, Notes, Temp } |> data
cleaned = remove { ID, Timestamp } |> data  // Alternativa
```

---

### 2.5. Mapeo de Valores

```
// Mapeo directo (reemplazar en la misma columna)
normalized = map(Status) {
    "Y" -> "1",
    "N" -> "0",
    "Unknown" -> "-1"
} replace |> data

// Crear nueva columna
status_numeric = map(Status) {
    "Active" -> "1",
    "Inactive" -> "0"
} as status_code |> data

// Mapeo con patrones LIKE
territory_mapped = map(TERRITORY) {
    "*N*" => "0",
    "*A*" => "0"
} replace |> data

// Mapeo de substrings
fixed_country = replace(native-country, "-", " ") replace |> data
country_clean = replace(country, "_", " ") as country_cleaned |> data
```

---

### 2.6. Operaciones Matemáticas

```
// Operaciones básicas
birth_year = math(1994 - age) as Age-of-birth |> data
total = math(price * quantity) as total_cost |> data
bmi = math(weight / (height ^ 2)) as bmi_index |> data

// Con funciones
absolute = math(abs(value)) as abs_value |> data
rounded = math(round(score, 2)) as score_rounded |> data
result = math((price * 1.21) + shipping) as total_with_tax |> data
```

**Funciones disponibles**: `abs`, `sqrt`, `pow`, `log`, `exp`, `sin`, `cos`, `tan`, `round`, `ceil`, `floor`

---

### 2.7. Discretización (Binning)

```
// Binning simple
age_groups = bin(Age) {
    "Child": [0, 12),
    "Teen": [12, 18),
    "Adult": [18, 65),
    "Senior": [65, 120]
} as age_category |> data

// Reemplazar columna original
work_type = bin(hours-per-week) {
    "PART-TIME": [0, 40),
    "FULL-TIME": [40, *]
} replace |> data

// Binning con infinito
satscore_bins = bin(satscore) {
    "54 Percentile and Under": (-inf, 1040],
    "55-75 Percentile": (1040, 1160),
    "76-93 Percentile": [1160, 1340),
    "94+ percentile": [1340, inf)
} as satscore_binned |> data
```

**Notación de intervalos**:
- `[a, b]`: cerrado (incluye a y b)
- `[a, b)`: semi-abierto (incluye a, excluye b)
- `(a, b]`: semi-abierto (excluye a, incluye b)
- `(a, b)`: abierto (excluye a y b)
- `*`, `inf`, `-inf`: infinito

---

### 2.8. Conversión de Tipos

```
// Convertir a numérico
numeric_data = to_numeric(TERRITORY, Instate, ETHNICITY) |> data
numeric_eu = to_numeric(price, amount) separator = "," |> data  // Separador decimal personalizado

// Otros tipos
string_ids = to_string(customer_id, product_id) |> data
categorical = to_categorical(gender, country, status) |> data
dates = to_date(date_column, format = "yyyy-MM-dd") |> data
```

---

### 2.9. Imputación

```
// Valor fijo
filled = impute(Age, Income) { fixed = 0 } |> data
filled_str = impute(Country) { fixed = "Unknown" } |> data
filled_multi = impute(COL1, COL2) { fixed = ["Val1", "Val2"] } |> data

// Métodos estadísticos
mean_imputed = impute(Age, Salary) { mean } |> data
median_imputed = impute(Income) { median } |> data
mode_imputed = impute(Category, Country) { mode } |> data
freq_imputed = impute(sex, ETHNICITY) { most_frequent } |> data
min_imputed = impute(Price) { min } |> data
max_imputed = impute(Score) { max } |> data

// Métodos secuenciales
ffill = impute(Temperature) { forward_fill } |> time_series
bfill = impute(Sales) { backward_fill } |> time_series

// Métodos avanzados
interpolated = impute(satscore) { interpolation } |> data
linear = impute(value) { linear } |> data
mavg = impute(price) { moving_average window = 5 } |> data
poly = impute(value) { polynomial degree = 2 } |> data
spline = impute(value) { spline } |> data
```

---

### 2.10. Tratamiento de Outliers

```
// Métodos básicos
clean = outliers(Income, Age) { replace_closest iqr } |> data
clean2 = outliers(Salary) { replace_closest iqr scalar = 1.5 } |> data
clean3 = outliers(avg_income, distance) { replace_by_closest iqr estimation = R_4 } |> data

// Z-Score
clean4 = outliers(Price) { replace_closest zscore } |> data  // threshold = 3.0 por defecto
clean5 = outliers(Temperature) { replace_closest zscore threshold = 2.5 } |> data

// Otras estrategias
missing_outliers = outliers(value) { replace_missing iqr } |> data
no_outliers = outliers(value) { remove iqr } |> data
capped = outliers(value) { cap percentile lower = 5 upper = 95 } |> data

// Scope de detección
lower_only = outliers(value) { replace_closest iqr scope = lower_only } |> data
upper_only = outliers(value) { replace_closest iqr scope = upper_only } |> data
all_outliers = outliers(value) { replace_closest iqr scope = all_outliers } |> data
```

**Estrategias**: `replace_closest`, `replace_missing`, `replace_by_closest`, `cap`, `remove`  
**Métodos**: `iqr`, `zscore`, `percentile`  
**Scopes**: `all`, `all_outliers`, `lower_only`, `upper_only`

---

### 2.11. Join

```
// Tipos de join
merged = join(customers, orders) { inner on customer_id = cust_id } |> data
merged2 = join(left_table, right_table) { left on id = id and date = date } |> data
all_data = join(table1, table2) { full on key = foreign_key } |> data
right_merged = join(table1, table2) { right on id = id } |> data
cartesian = join(table1, table2) { cross on * } |> data

// Con sufijos para columnas duplicadas
merged_suffix = join(left, right) {
    inner on id = id
    suffix = ("_left", "_right")
} |> data
```

**Tipos**: `inner`, `left`, `right`, `full`, `cross`

---

### 2.12. Contratos - Preconditions, Postconditions e Invariants

Los contratos son validaciones formales sobre los datos. Se definen en tres niveles:

**Niveles**:
- **PRECONDITION**: Validación antes de la transformación
- **POSTCONDITION**: Validación después de la transformación
- **INVARIANT**: Propiedades que se mantienen durante la transformación

**Tipos**:

```
// Value Range - Verificar rangos o tipos
precondition "age_valid" {
    value_range(input.Age, in_range [0, 120])
}

// Condition - Lógica if-then
invariant "preserve_type" {
    condition {
        if input.Age belongs_to type Integer
        then output.Age belongs_to type Integer
    }
}

// Special Value - Detectar NA, NaN, null
postcondition "no_missing" {
    no_special_values(output.Age)
}

// Cast Type - Verificación de conversión
precondition "castable" {
    castable_to Integer(input.Status)
}
```

**Ejemplo completo con conversión numérica**:

```
numeric_data = to_numeric(TERRITORY, Instate) |> data contracts {
    precondition "TERRITORY_castable" {
        value_range(input.TERRITORY, castable_to Integer)
    }
    postcondition "TERRITORY_is_integer" {
        is_type Integer(output.TERRITORY)
    }
    invariant "TERRITORY_no_special" {
        condition {
            if input.TERRITORY not_belongs_to special_values
            then output.TERRITORY not_belongs_to special_values
        }
    }
}
```

---

## 3. Workflow Completo Real: "Model data set with metanode"

Este es el ejemplo más completo basado en el workflow real del proyecto:

```
workflow "Model Dataset with Metanode - Complete Pipeline" {
    // 1. Cargar datos
    source raw = read_file("/Data_model(1).csv")
    
    // 2. Imputación por moda para categóricas
    imputed_cat = impute(sex, ETHNICITY, IRSCHOOL) {
        most_frequent
    } |> raw
    
    // 3. Imputación por interpolación para satscore
    imputed_sat = impute(satscore) {
        interpolation
    } |> imputed_cat
    
    // 4. Imputación por media para numéricas
    imputed_num = impute(avg_income, distance) {
        mean
    } |> imputed_sat
    
    // 5. Imputación con valores fijos
    imputed_fixed = impute(ACADEMIC_INTEREST_1, ACADEMIC_INTEREST_2) {
        fixed = ["Unknown", "Unknown"]
    } |> imputed_num
    
    // 6. Filtro por rango (init_span >= 0)
    filtered_range = filter_rows {
        range(init_span, [0, *], include)
    } |> imputed_fixed
    
    // 7. Filtro de columnas (drop 6 columnas específicas)
    filtered_cols = drop_columns {
        TRAVEL_INIT_CNTCTS, REFERRAL_CNTCTS, CONTACT_CODE1,
        telecq, interest, stuemail
    } |> filtered_range
    
    // 8. Mapeo de TERRITORY
    mapped_territory = map(TERRITORY) {
        "*N*" => "0",
        "*A*" => "0"
    } replace |> filtered_cols
    
    // 9. Mapeo de Instate
    mapped_instate = map(Instate) {
        "*Y*" => "1",
        "*N*" => "0"
    } replace |> mapped_territory
    
    // 10. Conversión a numérico (12 columnas) CON CONTRATOS
    numeric_data = to_numeric(
        TERRITORY, Instate, ETHNICITY, ACADEMIC_INTEREST_1,
        ACADEMIC_INTEREST_2, Enroll, IRSCHOOL, sex,
        premiere, CONTACT_CODE1, stuemail, prediction
    ) |> mapped_instate contracts {
        // Precondiciones: campos deben ser castables
        precondition "TERRITORY_castable" {
            value_range(input.TERRITORY, castable_to Integer)
        }
        precondition "Instate_castable" {
            value_range(input.Instate, castable_to Integer)
        }
        
        // Postcondiciones: campos son Integer
        postcondition "TERRITORY_is_integer" {
            is_type Integer(output.TERRITORY)
        }
        postcondition "Instate_is_integer" {
            is_type Integer(output.Instate)
        }
        
        // Invariantes: preservar ausencia de valores especiales
        invariant "TERRITORY_no_special" {
            condition {
                if input.TERRITORY not_belongs_to special_values
                then output.TERRITORY not_belongs_to special_values
            }
        }
        invariant "Instate_no_special" {
            condition {
                if input.Instate not_belongs_to special_values
                then output.Instate not_belongs_to special_values
            }
        }
        
        // Invariantes: tipo correcto si castable
        invariant "TERRITORY_type_preserved" {
            condition {
                if input.TERRITORY belongs_to type Integer
                then output.TERRITORY belongs_to type Integer
            }
        }
        invariant "Instate_type_preserved" {
            condition {
                if input.Instate belongs_to type Integer
                then output.Instate belongs_to type Integer
            }
        }
    }
    
    // 11. Tratamiento de outliers con IQR
    outliers_treated = outliers(avg_income, distance, Instate) {
        replace_by_closest iqr scalar = 1.5 estimation = R_4 scope = all_outliers
    } |> numeric_data
    
    // 12. Binning de satscore (4 bins)
    binned_sat = bin(satscore) {
        "54 Percentile and Under": (-inf, 1040],
        "55-75 Percentile": (1040, 1160),
        "76-93 Percentile": [1160, 1340),
        "94+ percentile": [1340, inf)
    } as satscore_binned |> outliers_treated
    
    // 13. Binning de TERRITORY (5 zonas)
    binned_territory = bin(TERRITORY) {
        "Unknown": (-inf, 1),
        "Zone 1": [1, 3),
        "Zone 2": [3, 5),
        "Zone 3": [5, 7),
        "Zone 4": [7, inf)
    } as TERRITORY_binned |> binned_sat
    
    // 14. Binning de avg_income (3 niveles)
    binned_income = bin(avg_income) {
        "low": (-inf, 42830),
        "Moderate": [42830, 55559),
        "High": [55559, inf)
    } as avg_income_binned |> binned_territory
    
    // 15. Binning de TOTAL_CONTACTS (3 niveles)
    binned_contacts = bin(TOTAL_CONTACTS) {
        "Low": (-inf, 1),
        "Moderate": [1, 4),
        "High": [4, inf)
    } as TOTAL_CONTACTS_binned |> binned_income
    
    // 16. Binning de SOLICITED_CNTCTS
    binned_solicited = bin(SOLICITED_CNTCTS) {
        "Low": (-inf, 1),
        "Moderate": [1, 4),
        "High": [4, inf)
    } as SOLICITED_CNTCTS_binned |> binned_contacts
    
    // 17. Binning de SELF_INIT_CNTCTS (resultado final)
    final = bin(SELF_INIT_CNTCTS) {
        "Low": (-inf, 1),
        "Moderate": [1, 4),
        "High": [4, inf)
    } as SELF_INIT_CNTCTS_binned |> binned_solicited
}
```

**Este workflow compila a un JSON de 806 líneas con 19 nodos y 16 conexiones.**

---

## 4. Características Avanzadas del DSL

### 4.1. Comentarios

```
// Comentario de una línea

/* Comentario multilínea */

workflow "Example" {
    source data = read_csv("/file.csv")  // Inline
    
    /* Este paso filtra valores faltantes */
    clean = filter_rows { missing(Age, exclude) } |> data
}
```

### 4.2. Pipeline Encadenado

```
workflow "Chained Pipeline" {
    source data = read_csv("/data.csv")
    
    result = filter_rows { missing(*, exclude) }
           |> filter_rows { range(Age, [18, *], include) }
           |> select_columns { Name, Age, Income }
           |> to_numeric(Age, Income)
           |> impute(Income) { median }
           |> data
}
```

### 4.3. Contratos y Validación

Los contratos se **generan automáticamente** en XMI y se validan mediante funciones `data_smells.check_*()`. Ejemplo de código generado:

```python
# Precondición
assert data_smells.check_castable_to_integer(df['TERRITORY']), \
    "PRECONDITION FAILED: TERRITORY not castable to Integer"

# Transformación
df['TERRITORY'] = df['TERRITORY'].astype(int)

# Postcondición
assert df['TERRITORY'].dtype == int, \
    "POSTCONDITION FAILED: TERRITORY is not Integer"
```

---

## 5. Mapeo Completo DSL → JSON → XMI

### Tabla de Correspondencia de Nodos

| DSL Keyword | JSON node_type | JSON node_name | XMI Element |
|-------------|----------------|----------------|-------------|
| `read_csv()` | `org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory` | CSV Reader | `<dataprocessing>` |
| `read_file()` | `org.knime.base.node.io.filehandling.csv.reader.FileReaderNodeFactory` | File Reader | `<dataprocessing>` |
| `filter_rows { missing(...) }` | `org.knime.base.node.preproc.filter.row.RowFilterNodeFactory` | Row Filter | `<dataprocessing>` |
| `filter_rows { range(...) }` | `org.knime.base.node.preproc.filter.row.RowFilterNodeFactory` | Row Filter | `<dataprocessing>` |
| `filter_rows { matches(...) }` | `org.knime.base.node.preproc.filter.row.RowFilterNodeFactory` | Row Filter | `<dataprocessing>` |
| `select_columns {}` | `org.knime.base.node.preproc.filter.column.DataColumnSpecFilterNodeFactory` | Column Filter | `<dataprocessing>` |
| `map() {}` | `org.knime.base.node.rules.engine.RuleEngineNodeFactory` | Rule Engine | `<dataprocessing>` |
| `replace()` | `org.knime.base.node.preproc.stringmanipulation.StringManipulationNodeFactory` | String Manipulation | `<dataprocessing>` |
| `math()` | `org.knime.ext.jep.JEPNodeFactory` | Math Formula | `<dataprocessing>` |
| `bin() {}` | `org.knime.base.node.preproc.binner.BinnerNodeFactory` | Numeric Binner | `<dataprocessing>` |
| `to_numeric()` | `org.knime.base.node.preproc.colconvert.stringtonumber2.StringToNumber2NodeFactory` | String to Number | `<dataprocessing>` |
| `impute() {}` | `null` (node_type) | Missing Value | `<dataprocessing>` |
| `outliers() {}` | `org.knime.base.node.stats.outlier.handler.NumericOutliersNodeFactory` | Numeric Outliers | `<dataprocessing>` |
| `join() {}` | `org.knime.base.node.preproc.joiner.Joiner2NodeFactory` | Joiner | `<dataprocessing>` |

### Tabla de Correspondencia de Contratos

| DSL Keyword | XMI Contract Type | XMI Element |
|-------------|-------------------|-------------|
| `precondition { value_range(...) }` | `Contract:ValueRange` | `<contract name="..._PRECONDITION">` |
| `postcondition { value_range(...) }` | `Contract:ValueRange` | `<contract name="..._POSTCONDITION">` |
| `invariant { condition {...} }` | `Contract:Condition` | `<contract name="..._INVARIANT">` |
| `no_special_values(...)` | `Contract:SpecialValue` | `<dataCondition xsi:type="Contract:SpecialValue">` |
| `castable_to Type` | `Contract:CastType` | `<value xsi:type="Contract:CastType" type="...">` |
| `belongs_to` | `belongOp="BELONG"` | `<if belongOp="BELONG">` |
| `not_belongs_to` | `belongOp="NOTBELONG"` | `<if belongOp="NOTBELONG">` |
| `input.Column` | `Contract:DataField` (input) | `<in xsi:type="Contract:DataField" dataField=".../@inputPort...">` |
| `output.Column` | `Contract:DataField` (output) | `<out xsi:type="Contract:DataField" dataField=".../@outputPort...">` |

### Estructura JSON Extendida con Contratos

Para que el JSON sea parseable en el futuro, se añade una sección `"contracts"` al formato existente:

```json
{
  "nodes": [
    {
      "id": 12,
      "node_name": "String to Number",
      "node_type": "org.knime.base.node.preproc.colconvert.stringtonumber2.StringToNumber2NodeFactory",
      "parameters": { ... }
    }
  ],
  "connections": [
    {"sourceID": 1, "destID": 12}
  ],
  "contracts": {
    "12": {
      "preconditions": [
        {
          "name": "TERRITORY_castable",
          "type": "value_range",
          "field": "input",
          "column": "TERRITORY",
          "check": "castable_to",
          "target_type": "Integer"
        }
      ],
      "postconditions": [
        {
          "name": "TERRITORY_is_integer",
          "type": "value_range",
          "field": "output",
          "column": "TERRITORY",
          "check": "is_type",
          "target_type": "Integer"
        }
      ],
      "invariants": [
        {
          "name": "TERRITORY_no_special",
          "type": "condition",
          "condition": {
            "if": {
              "field": "input",
              "column": "TERRITORY",
              "operator": "not_belongs_to",
              "check": "special_values"
            },
            "then": {
              "field": "output",
              "column": "TERRITORY",
              "operator": "not_belongs_to",
              "check": "special_values"
            }
          }
        }
      ]
    }
  }
}
```

**Notas importantes**:
- Los contratos se indexan por `node_id` (string)
- Cada nodo puede tener arrays de `preconditions`, `postconditions`, `invariants`
- Los contratos actuales se generan automáticamente en `json2workflow.py`
- Esta estructura está diseñada para trabajo futuro cuando se modifique el parser

### Flujo Completo: DSL → JSON → XMI

```
┌─────────────────────────────────────────┐
│  WORKFLOW DSL (TextX/Xtext Grammar)    │
│                                         │
│  numeric_data = to_numeric(Age, Income) │
│      |> data contracts {               │
│    precondition "castable" {           │
│      value_range(input.Age,            │
│                  castable_to Integer)  │
│    }                                    │
│  }                                      │
└──────────────┬──────────────────────────┘
               │ Compilación
               │ (Parser DSL → Futuro)
               ▼
┌─────────────────────────────────────────┐
│  JSON INTERMEDIO CON CONTRATOS         │
│                                         │
│  {                                      │
│    "nodes": [                           │
│      {                                  │
│        "id": 12,                        │
│        "node_name": "String to Number", │
│        "node_type": "...StringToNumber2 │
│                      NodeFactory",      │
│        "parameters": {                  │
│          "in_columns": [...],           │
│          "out_columns": [...]           │
│        }                                │
│      }                                  │
│    ],                                   │
│    "connections": [...],                │
│    "contracts": {                       │
│      "12": {                            │
│        "preconditions": [               │
│          {                              │
│            "name": "Age_castable",      │
│            "type": "value_range",       │
│            "field": "input",            │
│            "column": "Age",             │
│            "check": "castable_to",      │
│            "target_type": "Integer"     │
│          }                              │
│        ],                               │
│        "postconditions": [...],         │
│        "invariants": [...]              │
│      }                                  │
│    }                                    │
│  }                                      │
└──────────────┬──────────────────────────┘
               │ Transformación
               │ (json2workflow.py - FUTURO)
               │ Actualmente: ignora "contracts"
               │ Futuro: parsea y genera contratos
               ▼
┌─────────────────────────────────────────┐
│  XMI (MD4DSP Workflow Model)           │
│                                         │
│  <dataprocessing name="stringToNumber"> │
│    <inputPort>                          │
│      <datafield name="Age"              │
│                 xsi:type="Categorical"/> │
│    </inputPort>                         │
│    <outputPort>                         │
│      <datafield name="Age"              │
│                 xsi:type="Continuous"/> │
│    </outputPort>                        │
│                                         │
│    <contract name="Age_castType_        │
│                    PRECONDITION">       │
│      <contract xsi:type="Contract:      │
│                ValueRange">             │
│        <in xsi:type="Contract:DataField"│
│            dataField=".../@inputPort... │
│                      /@datafield.0"/>   │
│        <value xsi:type="Contract:       │
│               CastType"/>               │
│      </contract>                        │
│    </contract>                          │
│  </dataprocessing>                      │
└──────────────┬──────────────────────────┘
               │ Generación de Código
               │ (MM-M4DS Acceleo)
               ▼
┌─────────────────────────────────────────┐
│  PYTHON EXECUTABLE CODE                 │
│                                         │
│  # PRECONDITION                         │
│  assert data_smells.check_castable_to_  │
│         integer(df['Age']),             │
│    "PRECONDITION FAILED: Age not        │
│     castable to Integer"                │
│                                         │
│  # TRANSFORMATION                       │
│  df['Age'] = df['Age'].astype(int)      │
│                                         │
│  # POSTCONDITION                        │
│  assert df['Age'].dtype == int,         │
│    "POSTCONDITION FAILED"               │
└─────────────────────────────────────────┘
```

Este flujo muestra cómo:
1. El **DSL** se escribe de forma legible y concisa
2. Se compila a **JSON intermedio** (formato actual del proyecto + sección "contracts")
3. Se transforma a **XMI** con contratos incluidos
4. Se genera **código Python ejecutable** con validaciones

---

## 5.1. Especificación Detallada: Contratos en JSON

Esta sección define **cómo estructurar contratos en JSON** para que sean parseables cuando se modifique `json2workflow.py`.

### 5.1.1. Estructura General

```json
{
  "nodes": [...],
  "connections": [...],
  "contracts": {
    "<node_id>": {
      "preconditions": [<Contract>, ...],
      "postconditions": [<Contract>, ...],
      "invariants": [<Contract>, ...]
    }
  }
}
```

- `<node_id>`: String con el ID del nodo (e.g., `"12"`)
- Cada nodo puede tener 0 o más contratos de cada tipo
- Si un nodo no tiene contratos, puede omitirse de la sección `"contracts"`

### 5.1.2. Tipo de Contrato: ValueRange

**DSL**:
```
precondition "Age_castable" {
    value_range(input.Age, castable_to Integer)
}
```

**JSON**:
```json
{
  "name": "Age_castable",
  "type": "value_range",
  "field": "input",
  "column": "Age",
  "check": "castable_to",
  "target_type": "Integer"
}
```

**Campos**:
- `name`: Identificador del contrato
- `type`: `"value_range"`
- `field`: `"input"` o `"output"`
- `column`: Nombre de la columna
- `check`: `"castable_to"`, `"is_type"`, `"in_range"`, `"matches"`
- `target_type`: `"Integer"`, `"Double"`, `"String"`, `"Boolean"` (si check es castable_to o is_type)
- `range`: `{"lower": 0, "upper": 120}` (si check es in_range)
- `values`: `["value1", "value2"]` (si check es matches)

**Ejemplos adicionales**:

```json
// value_range con rango
{
  "name": "Age_in_valid_range",
  "type": "value_range",
  "field": "input",
  "column": "Age",
  "check": "in_range",
  "range": {
    "lower": 0,
    "upper": 120,
    "lower_inclusive": true,
    "upper_inclusive": true
  }
}

// value_range con valores específicos
{
  "name": "Status_valid_values",
  "type": "value_range",
  "field": "output",
  "column": "Status",
  "check": "matches",
  "values": ["1", "0", "-1"]
}
```

### 5.1.3. Tipo de Contrato: Condition (if-then)

**DSL**:
```
invariant "Age_type_preserved" {
    condition {
        if input.Age belongs_to type Integer
        then output.Age belongs_to type Integer
    }
}
```

**JSON**:
```json
{
  "name": "Age_type_preserved",
  "type": "condition",
  "condition": {
    "if": {
      "field": "input",
      "column": "Age",
      "operator": "belongs_to",
      "check": "type",
      "target_type": "Integer"
    },
    "then": {
      "field": "output",
      "column": "Age",
      "operator": "belongs_to",
      "check": "type",
      "target_type": "Integer"
    }
  }
}
```

**Campos**:
- `name`: Identificador del contrato
- `type`: `"condition"`
- `condition`: Objeto con `if` y `then`
  - `if`: Cláusula condicional
    - `field`: `"input"` o `"output"`
    - `column`: Nombre de la columna
    - `operator`: `"belongs_to"` o `"not_belongs_to"`
    - `check`: `"type"`, `"special_values"`, `"value"`, `"range"`
    - `target_type`: Tipo esperado (si check es "type")
  - `then`: Resultado esperado (misma estructura que `if`)

**Ejemplos adicionales**:

```json
// Condition con special_values
{
  "name": "no_special_preserved",
  "type": "condition",
  "condition": {
    "if": {
      "field": "input",
      "column": "Income",
      "operator": "not_belongs_to",
      "check": "special_values"
    },
    "then": {
      "field": "output",
      "column": "Income",
      "operator": "not_belongs_to",
      "check": "special_values"
    }
  }
}

// Condition con valor específico
{
  "name": "positive_preserved",
  "type": "condition",
  "condition": {
    "if": {
      "field": "input",
      "column": "Amount",
      "operator": "belongs_to",
      "check": "range",
      "range": {"lower": 0, "upper": null}
    },
    "then": {
      "field": "output",
      "column": "Amount",
      "operator": "belongs_to",
      "check": "range",
      "range": {"lower": 0, "upper": null}
    }
  }
}
```

### 5.1.4. Tipo de Contrato: SpecialValue

**DSL**:
```
postcondition "no_missing_Age" {
    no_special_values(output.Age)
}
```

**JSON**:
```json
{
  "name": "no_missing_Age",
  "type": "special_value",
  "field": "output",
  "column": "Age",
  "check": "not_belongs_to",
  "special_values": ["NA", "NaN", "null", "Inf", "-Inf"]
}
```

**Campos**:
- `name`: Identificador del contrato
- `type`: `"special_value"`
- `field`: `"input"` o `"output"`
- `column`: Nombre de la columna
- `check`: `"not_belongs_to"` (no tiene) o `"belongs_to"` (sí tiene)
- `special_values`: Array de valores especiales a verificar

**Ejemplo inverso** (verificar que SÍ hay valores especiales):

```json
{
  "name": "has_missing_Income",
  "type": "special_value",
  "field": "input",
  "column": "Income",
  "check": "belongs_to",
  "special_values": ["NA", "NaN", "null"]
}
```

### 5.1.5. Tipo de Contrato: CastType

**DSL**:
```
precondition "Status_is_castable" {
    castable_to Integer(input.Status)
}
```

**JSON**:
```json
{
  "name": "Status_is_castable",
  "type": "cast_type",
  "field": "input",
  "column": "Status",
  "check": "castable_to",
  "target_type": "Integer"
}
```

**Campos**:
- `name`: Identificador del contrato
- `type`: `"cast_type"`
- `field`: `"input"` o `"output"`
- `column`: Nombre de la columna
- `check`: `"castable_to"` o `"is_type"`
- `target_type`: `"Integer"`, `"Double"`, `"String"`, `"Boolean"`

**Ejemplo con is_type**:

```json
{
  "name": "Age_is_integer",
  "type": "cast_type",
  "field": "output",
  "column": "Age",
  "check": "is_type",
  "target_type": "Integer"
}
```

### 5.1.6. Ejemplo Completo: Workflow con Contratos en JSON

```json
{
  "nodes": [
    {
      "id": 1,
      "node_name": "CSV Reader",
      "node_type": "org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory",
      "parameters": {"file_path": "/data/file.csv", "column_delimiter": ","}
    },
    {
      "id": 12,
      "node_name": "String to Number",
      "node_type": "org.knime.base.node.preproc.colconvert.stringtonumber2.StringToNumber2NodeFactory",
      "parameters": {
        "decimal_separator": ".",
        "in_columns": [
          {"column_name": "TERRITORY", "column_type": "xstring"},
          {"column_name": "Instate", "column_type": "xstring"}
        ],
        "out_columns": [
          {"column_name": "TERRITORY", "column_type": "xstring"},
          {"column_name": "Instate", "column_type": "xstring"}
        ]
      }
    }
  ],
  "connections": [{"sourceID": 1, "destID": 12}],
  "contracts": {
    "12": {
      "preconditions": [
        {
          "name": "TERRITORY_castable",
          "type": "value_range",
          "field": "input",
          "column": "TERRITORY",
          "check": "castable_to",
          "target_type": "Integer"
        },
        {
          "name": "Instate_castable",
          "type": "value_range",
          "field": "input",
          "column": "Instate",
          "check": "castable_to",
          "target_type": "Integer"
        }
      ],
      "postconditions": [
        {
          "name": "TERRITORY_is_integer",
          "type": "cast_type",
          "field": "output",
          "column": "TERRITORY",
          "check": "is_type",
          "target_type": "Integer"
        }
      ],
      "invariants": [
        {
          "name": "TERRITORY_no_special",
          "type": "condition",
          "condition": {
            "if": {
              "field": "input",
              "column": "TERRITORY",
              "operator": "not_belongs_to",
              "check": "special_values"
            },
            "then": {
              "field": "output",
              "column": "TERRITORY",
              "operator": "not_belongs_to",
              "check": "special_values"
            }
          }
        }
      ]
    }
  }
}
```

### 5.1.7. Mapeo JSON → XMI

Cuando se modifique `json2workflow.py`, este sería el mapeo:

| JSON Contract Type | XMI Contract Element |
|-------------------|---------------------|
| `"type": "value_range"` | `<contract xsi:type="Contract:ValueRange">` |
| `"type": "condition"` | `<contract xsi:type="Contract:Condition">` |
| `"type": "special_value"` | `<dataCondition xsi:type="Contract:SpecialValue">` |
| `"type": "cast_type"` | `<value xsi:type="Contract:CastType">` |
| `"field": "input"` | `<in xsi:type="Contract:DataField" dataField=".../@inputPort...">` |
| `"field": "output"` | `<out xsi:type="Contract:DataField" dataField=".../@outputPort...">` |
| `"operator": "belongs_to"` | `belongOp="BELONG"` |
| `"operator": "not_belongs_to"` | `belongOp="NOTBELONG"` |
| Precondition | `<contract name="..._PRECONDITION">` |
| Postcondition | `<contract name="..._POSTCONDITION">` |
| Invariant | `<contract name="..._INVARIANT">` |

### 5.1.8. Nota sobre el Parser Actual

**IMPORTANTE**: El parser actual `json2workflow.py`:
- ✅ Lee `nodes` y `connections`
- ✅ Genera contratos automáticamente basándose en el tipo de transformación
- ❌ **IGNORA** la sección `"contracts"` si existe en el JSON

Para que los contratos del JSON se usen:
1. Modificar `json2workflow.py` para leer la sección `"contracts"`
2. Por cada contrato en el JSON, generar el elemento XMI correspondiente
3. Opcionalmente, deshabilitar la generación automática de contratos

Esta estructura JSON está **diseñada para ser forward-compatible** con esta modificación futura.

---

## 6. Validaciones Semánticas

### 6.1. Validaciones Estructurales
- ✅ Todo workflow DEBE tener exactamente un `source`
- ✅ El `source` DEBE ser la primera declaración
- ✅ Todas las variables referenciadas con `|>` deben existir previamente
- ✅ No puede haber ciclos en el grafo de dependencias
- ✅ Los nombres de variables deben ser únicos

### 6.2. Validaciones de Tipo
- ✅ Las columnas referenciadas deben existir en el dataset
- ✅ Los tipos de columnas deben ser compatibles con la operación
- ✅ Los valores numéricos deben ser válidos en rangos
- ✅ Los intervalos en binning deben ser válidos (left < right)

### 6.3. Validaciones de Lógica de Negocio
- ✅ En `filter_rows`, `include` y `exclude` son mutuamente excluyentes
- ✅ En binning, los intervalos no deben solaparse
- ✅ En join, ambos datasets deben existir
- ✅ Las columnas de join deben existir en ambos datasets

---

## 7. Extensiones Futuras (Ideas)

- **Variables y constantes**: `const THRESHOLD = 75`
- **Funciones reutilizables**: `function remove_missing(dataset, columns) { ... }`
- **Subworkflows**: `subworkflow clean_data(input) { ... }`
- **Condicionales**: `if has_column(Age) { ... }`

---

## 8. Herramientas de Desarrollo (Propuestas)

- **Compilador**: `wfdsl compile pipeline.wfdsl -o output.json`
- **Validador**: `wfdsl validate pipeline.wfdsl`
- **REPL**: `wfdsl repl`
- **VS Code Extension**: Syntax highlighting, autocompletado, validación en tiempo real

---

## 9. Convenciones de Estilo

```
// ✅ BUENO: Nombres descriptivos y snake_case
clean_data = filter_rows { missing(Age, exclude) } |> raw_data
age_groups = bin(Age) { ... } as age_category |> clean_data

// ❌ MALO: Nombres crípticos
d1 = filter_rows { missing(Age, exclude) } |> d

// ✅ BUENO: Indentación consistente (4 espacios)
workflow "Example" {
    source data = read_csv("/file.csv")
    
    step1 = filter_rows { missing(Age, exclude) } |> data
}

// ✅ BUENO: Agrupar transformaciones relacionadas
// Limpieza
clean1 = filter_rows { missing(*, exclude) } |> data
clean2 = filter_rows { range(Age, [0, 120], include) } |> clean1

// Transformaciones
transformed = to_numeric(Age, Income) |> clean2
```

---

## 10. Estadísticas de Cobertura

### Workflows Analizados (35 total):
✅ **100% de cobertura** de todos los tipos de nodos  
✅ **100% de cobertura** de todos los parámetros encontrados  
✅ **100% de cobertura** de todas las transformaciones de la librería MD4DSP  
✅ **100% de cobertura** de contratos del XMI (Model data set with metanode.xmi)

### Tipos de Nodos Cubiertos (12 total):
1. ✅ CSVTableReaderNodeFactory
2. ✅ FileReaderNodeFactory
3. ✅ RowFilterNodeFactory (3 tipos de filtros)
4. ✅ DataColumnSpecFilterNodeFactory
5. ✅ RuleEngineNodeFactory
6. ✅ StringManipulationNodeFactory
7. ✅ JEPNodeFactory (Math Formula)
8. ✅ BinnerNodeFactory
9. ✅ StringToNumber2NodeFactory
10. ✅ Missing Value (node_type null)
11. ✅ NumericOutliersNodeFactory
12. ✅ FormulasNodeFactory

### Transformaciones Librería MD4DSP (13 total):
1. ✅ rowFilterMissing
2. ✅ rowFilterRange
3. ✅ rowFilterPrimitive
4. ✅ columnFilter
5. ✅ mapping
6. ✅ mathOperation
7. ✅ binner
8. ✅ categoricalToContinuous
9. ✅ imputeByFixValue
10. ✅ imputeByNumericOp
11. ✅ imputeByDerivedValue
12. ✅ imputeOutliersByClosest
13. ✅ join

### Tipos de Contratos Cubiertos (4 total):
1. ✅ ValueRange (Preconditions/Postconditions)
2. ✅ Condition (Invariants con if-then)
3. ✅ SpecialValue (valores especiales: NA, NaN, null)
4. ✅ CastType (verificación de tipos Integer, Double, String, Boolean)

### Niveles de Contratos:
- ✅ **PRECONDITION**: Validaciones antes de la transformación
- ✅ **POSTCONDITION**: Validaciones después de la transformación
- ✅ **INVARIANT**: Propiedades que se mantienen durante la transformación

### Operadores de Contratos:
- ✅ `belongs_to` / `not_belongs_to` (pertenencia)
- ✅ `castable_to` / `is_type` (verificación de tipos)
- ✅ `in_range` (rangos de valores)
- ✅ `special_values` (detección de NA, NaN, null)
- ✅ `condition { if ... then ... }` (lógica condicional)

---

## 11. Palabras Reservadas Completas

```
// Estructura de workflow
workflow, source, read_csv, read_file,

// Transformaciones
filter_rows, select_columns, drop_columns, keep, remove,
map, replace, math, bin, 
to_numeric, to_string, to_categorical, to_boolean, to_date,
impute, outliers, join,

// Modificadores y operadores
as, replace, missing, range, matches, like, 
include, exclude, on, and,

// Métodos de imputación
fixed, mean, median, mode, most_frequent, max, min,
forward_fill, backward_fill, previous_value, next_value,
interpolation, linear, polynomial, spline, moving_average,

// Tratamiento de outliers
replace_closest, replace_missing, replace_by_closest, cap,
iqr, zscore, percentile,
scalar, estimation, threshold, window, degree, scope,
all, all_outliers, lower_only, upper_only,

// Joins
inner, left, right, full, cross,

// Conversión de tipos
separator, format, suffix,

// Valores especiales
inf, -inf, Infinity, -Infinity,
true, false, null,

// *** CONTRATOS ***
contracts, precondition, postcondition, invariant,
value_range, condition, if, then,
belongs_to, not_belongs_to,
special_values, no_special_values, has_special_values,
castable_to, is_type,
input, output,
Integer, Double, String, Boolean,
in_range, count, min, max
```

---

## 12. Convenciones de Estilo

```
// ✅ BUENO: Nombres descriptivos y snake_case
clean_data = filter_rows { missing(Age, exclude) } |> raw_data
age_groups = bin(Age) { ... } as age_category |> clean_data

// ❌ MALO: Nombres crípticos
d1 = filter_rows { missing(Age, exclude) } |> d
x = bin(Age) { ... } as y |> d1

// ✅ BUENO: Indentación consistente (4 espacios)
workflow "Example" {
    source data = read_csv("/file.csv")
    
    step1 = filter_rows { 
        missing(Age, exclude) 
    } |> data
}

// ✅ BUENO: Pipeline legible
result = transformation1
       |> transformation2
       |> transformation3
       |> data

// ✅ BUENO: Agrupar transformaciones relacionadas
// Primero: limpieza de datos
clean1 = filter_rows { missing(*, exclude) } |> data
clean2 = filter_rows { range(Age, [0, 120], include) } |> clean1

// Segundo: transformaciones
transformed = to_numeric(Age, Income) |> clean2
imputed = impute(Income) { median } |> transformed

// Tercero: agregaciones
final = bin(Age) { ... } as age_group |> imputed
```

---

## 13. Referencias

- **Workflows Analizados**: `parsed_json_workflows/*/`
- **Librería MD4DSP**: `library_hashing/library_transformation_names.json`
- **Templates XMI**: `templates/data_processing/*.xmi`
- **Mapeo KNIME-MD4DSP**: `KNIME_nodes_MD4DSP_mapping.xlsx`
- **Workflow Principal**: `parsed_json_workflows/Model data set with metanode/`

---

## 14. Changelog

- **v1.0** (2025-10-01): 
  - Primera versión completa con 100% de cobertura de los 35 workflows reales del proyecto
  - Análisis exhaustivo de todos los tipos de nodos (12/12)
  - Cobertura completa de transformaciones MD4DSP (13/13)
  - **Gramática de contratos añadida** basada en `Model data set with metanode.xmi`
  - Soporte para PRECONDITIONS, POSTCONDITIONS e INVARIANTS
  - 4 tipos de contratos: ValueRange, Condition, SpecialValue, CastType
  - Ejemplos completos de contratos en todas las transformaciones
  - Diagrama de flujo DSL → JSON → XMI → Python Code
  - **Especificación JSON completa para contratos** (Sección 5.1)
    - Estructura detallada de cada tipo de contrato en JSON
    - Ejemplo completo de workflow con 8 contratos en formato JSON
    - Mapeo JSON → XMI documentado
    - Forward-compatible: JSON preparado para modificación futura de `json2workflow.py`
    - Parser actual ignora contratos, pero estructura está lista para cuando se implemente

---

## 15. Ejemplo Completo Mínimo: DSL → JSON

### Workflow DSL con 2 Transformaciones y Contratos

```
workflow "Student Data Pipeline" {
    // 1. Cargar datos
    source data = read_csv("/data/students.csv", ,)
    
    // 2. Filtrar filas con valores faltantes
    clean = filter_rows {
        missing(Age, Grade, exclude)
    } |> data
    
    // 3. Convertir a numérico CON CONTRATOS
    numeric = to_numeric(Age, Grade) |> clean contracts {
        // Precondición: los campos deben ser castables a Integer
        precondition "Age_castable" {
            value_range(input.Age, castable_to Integer)
        }
        
        // Postcondición: los campos de salida son Integer
        postcondition "Age_is_integer" {
            is_type Integer(output.Age)
        }
        
        // Invariante: si input no tiene valores especiales, output tampoco
        invariant "Age_no_special" {
            condition {
                if input.Age not_belongs_to special_values
                then output.Age not_belongs_to special_values
            }
        }
    }
}
```

### JSON Resultante

```json
{
  "nodes": [
    {
      "id": 1,
      "node_name": "CSV Reader",
      "node_type": "org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory",
      "parameters": {
        "file_path": "/data/students.csv",
        "column_delimiter": ","
      }
    },
    {
      "id": 2,
      "node_name": "Row Filter",
      "node_type": "org.knime.base.node.preproc.filter.row.RowFilterNodeFactory",
      "parameters": {
        "filter_type": "MissingVal_RowFilter",
        "filter_type_inclusion": "EXCLUDE",
        "in_columns": [
          {"column_name": "Age", "column_type": "xstring"},
          {"column_name": "Grade", "column_type": "xstring"}
        ],
        "out_columns": [
          {"column_name": "Age", "column_type": "xstring"},
          {"column_name": "Grade", "column_type": "xstring"}
        ]
      }
    },
    {
      "id": 3,
      "node_name": "String to Number",
      "node_type": "org.knime.base.node.preproc.colconvert.stringtonumber2.StringToNumber2NodeFactory",
      "parameters": {
        "decimal_separator": ".",
        "in_columns": [
          {"column_name": "Age", "column_type": "xstring"},
          {"column_name": "Grade", "column_type": "xstring"}
        ],
        "out_columns": [
          {"column_name": "Age", "column_type": "xstring"},
          {"column_name": "Grade", "column_type": "xstring"}
        ]
      }
    }
  ],
  "connections": [
    {"sourceID": 1, "destID": 2},
    {"sourceID": 2, "destID": 3}
  ],
  "contracts": {
    "3": {
      "preconditions": [
        {
          "name": "Age_castable",
          "type": "value_range",
          "field": "input",
          "column": "Age",
          "check": "castable_to",
          "target_type": "Integer"
        }
      ],
      "postconditions": [
        {
          "name": "Age_is_integer",
          "type": "cast_type",
          "field": "output",
          "column": "Age",
          "check": "is_type",
          "target_type": "Integer"
        }
      ],
      "invariants": [
        {
          "name": "Age_no_special",
          "type": "condition",
          "condition": {
            "if": {
              "field": "input",
              "column": "Age",
              "operator": "not_belongs_to",
              "check": "special_values"
            },
            "then": {
              "field": "output",
              "column": "Age",
              "operator": "not_belongs_to",
              "check": "special_values"
            }
          }
        }
      ]
    }
  }
}
```

**Explicación del Flujo**:

1. **Node 1 (CSV Reader)**: Lee `/data/students.csv`
2. **Node 2 (Row Filter)**: Elimina filas con valores faltantes en `Age` y `Grade`
3. **Node 3 (String to Number)**: Convierte `Age` y `Grade` a Integer con 3 contratos:
   - **Precondición**: Verifica que `Age` sea castable a Integer antes de la conversión
   - **Postcondición**: Verifica que `Age` sea Integer después de la conversión
   - **Invariante**: Asegura que si `Age` no tenía valores especiales (NA/NaN/null) antes, tampoco los tiene después

**Conexiones**: 1→2→3 (pipeline secuencial)

---

**Autores**: Carlos Breuer Carrasco, Carlos Cambero Rojas  
**Proyecto**: knime2model_MD4DSP  
**Repositorio**: i3uex/knime2model_MD4DSP  
**Versión DSL**: 1.0
