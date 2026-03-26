import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig


if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("Initiate the data transforamtio")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation Completed")
        print(data_transformation_artifact)




        
        

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
