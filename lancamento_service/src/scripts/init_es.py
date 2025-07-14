#!/usr/bin/env python3
import logging
from datetime import datetime
from src.core.config import settings
from src.core.es_client import es_client
#from core.logging_config import configure_logging

#configure_logging()
logger = logging.getLogger(__name__)

def init_elasticsearch():
    """Inicializa índices e mapeamentos no Elasticsearch"""
    try:
        # Verifica se o Elasticsearch está disponível
        if not es_client.ping():
            raise ConnectionError("Não foi possível conectar ao Elasticsearch")
        
        # Configuração do índice de consolidados
        index_name = "consolidados-diarios"
        
        # Cria o índice se não existir
        if not es_client.indices.exists(index=index_name):
            logger.info(f"Criando índice {index_name}...")
            
            mapping = {
                "settings": {
                    "number_of_shards": 2,
                    "number_of_replicas": 1,
                    "analysis": {
                        "normalizer": {
                            "lowercase_normalizer": {
                                "type": "custom",
                                "filter": ["lowercase"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "data": {
                            "type": "date",
                            "format": "strict_date||epoch_millis"
                        },
                        "total_creditos": {
                            "type": "double"
                        },
                        "total_debitos": {
                            "type": "double"
                        },
                        "saldo_final": {
                            "type": "double"
                        },
                        "lancamentos": {
                            "type": "nested",
                            "properties": {
                                "id": {"type": "keyword"},
                                "valor": {"type": "double"},
                                "tipo": {
                                    "type": "keyword",
                                    "normalizer": "lowercase_normalizer"
                                },
                                "descricao": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                },
                                "categoria": {"type": "keyword"}
                            }
                        },
                        "timestamp": {
                            "type": "date",
                            "format": "strict_date_optional_time||epoch_millis"
                        }
                    }
                }
            }
            
            es_client.indices.create(
                index=index_name,
                body=mapping,
                ignore=400  # Ignora se o índice já existir
            )
            logger.info(f"Índice {index_name} criado com sucesso")
        
        # Cria template para índices futuros (opcional)
        template_name = "fluxo_caixa_template"
        template_body = {
            "index_patterns": ["fluxo_caixa_*"],
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "timestamp": {
                        "type": "date",
                        "format": "strict_date_optional_time||epoch_millis"
                    }
                }
            }
        }
        
        es_client.indices.put_template(
            name=template_name,
            body=template_body
        )
        logger.info(f"Template {template_name} criado com sucesso")
        
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar Elasticsearch: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Iniciando inicialização do Elasticsearch...")
    if init_elasticsearch():
        logger.info("Elasticsearch inicializado com sucesso")
    else:
        logger.error("Falha na inicialização do Elasticsearch")
        exit(1)