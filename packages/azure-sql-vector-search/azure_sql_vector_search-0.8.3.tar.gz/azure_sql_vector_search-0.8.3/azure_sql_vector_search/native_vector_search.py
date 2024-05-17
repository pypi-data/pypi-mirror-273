import json
from typing import Optional

from sqlalchemy import Table, Column, Integer, VARCHAR, VARBINARY, MetaData
from sqlalchemy import event, DDL, text

from azure_sql_vector_search.models import DistanceMetric, VectorSearchResult
from azure_sql_vector_search.vector_search_base import AzureSQLBaseVectorSearchClient


class AzureSQLNativeVectorSearchClient(AzureSQLBaseVectorSearchClient):
    """
    AzureSQLNativeVectorSearchClient

    Performs native vector search queries on tables containing vectors using built-in native functions and operations

    """

    def __init__(self, connection_string, table_name):
        super().__init__(connection_string, table_name)

        self.vector_embeddings_table_name = "{}_embeddings".format(table_name)
        self.vector_metadata_table_name = "{}_metadata".format(table_name)
        self.vector_index_name = "{}_vector_cc".format(self.vector_embeddings_table_name)

        self.metadata_object = MetaData()

        self.azure_sql_vector_metadata_table = Table(
            self.vector_metadata_table_name,
            self.metadata_object,
            Column("record_id", Integer, primary_key=True, autoincrement=True),
            Column("content", VARCHAR(None)),
            Column("metadata", VARCHAR(None)),
            Column("vector_content", VARCHAR(None))
        )

        self.azure_sql_vector_embeddings_table = Table(
            self.vector_embeddings_table_name,
            self.metadata_object,
            Column("record_id", Integer, nullable=False),
            Column("vector_embeddings", VARBINARY(8000))
        )

        clustered_column_ddl = ("create clustered columnstore index {} ON {}"
                                .format(self.vector_index_name, self.azure_sql_vector_embeddings_table))
        event.listen(
            self.azure_sql_vector_embeddings_table,
            "after_create",
            DDL(clustered_column_ddl)
        )

        # Creates all applicable tables defined in the constructor IF NOT EXISTS
        self.metadata_object.create_all(self.engine)

    def truncate_tables(self):
        truncate_embeddings_query = "TRUNCATE TABLE {}".format(self.vector_embeddings_table_name)
        truncate_metadata_query = "TRUNCATE TABLE {}".format(self.vector_metadata_table_name)
        connection = self.engine.connect()

        connection.execute(text(truncate_embeddings_query))
        connection.execute(text(truncate_metadata_query))

        connection.commit()
        connection.close()

    def delete_by_id(self, record_id: int):
        connection = self.engine.connect()
        record_identifier = int(record_id)

        delete_embeddings_query = ("DELETE FROM {} WHERE record_id = {}"
                                   .format(self.vector_embeddings_table_name, record_identifier))

        delete_metadata_query = ("DELETE FROM {} WHERE record_id = {}"
                                 .format(self.vector_metadata_table_name, record_identifier))

        connection.execute(text(delete_embeddings_query))
        connection.execute(text(delete_metadata_query))

        connection.commit()
        connection.close()

    def insert_row(self, content: str, metadata: dict, embeddings: list[float]):

        metadata_json_string = json.dumps(metadata)

        vector_content: str = json.dumps(embeddings)
        metadata_insert_statement = (self.azure_sql_vector_metadata_table
                                     .insert()
                                     .values(content=content, metadata=metadata_json_string,
                                             vector_content=vector_content))

        connection = self.engine.connect()

        metadata_result = connection.execute(metadata_insert_statement)

        # Retrieves the most recent primary key from the metadata table
        record_id = int(metadata_result.inserted_primary_key[0])
        vector_string = text("JSON_ARRAY_TO_VECTOR('{}')".format(vector_content))
        vectors_insert_statement = (self.azure_sql_vector_embeddings_table
                                    .insert()
                                    .values(record_id=record_id, vector_embeddings=vector_string))

        connection.execute(vectors_insert_statement)

        final_results = {
            "record_id": record_id,
            "embeddings": embeddings
        }

        connection.commit()
        connection.close()

        return final_results

    def compute_similarity(self, embedding_vectors: list[float], similarity_operation: DistanceMetric, k: int = 4,
                           filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:

        if similarity_operation == DistanceMetric.DOT_PRODUCT:
            return self.inner_product(embedding_vectors, k=k, filters=filters)

        elif similarity_operation == DistanceMetric.COSINE_SIMILARITY:
            return self.cosine_similarity(embedding_vectors, k=k, filters=filters)

        elif similarity_operation == DistanceMetric.EUCLIDEAN_DISTANCE:
            return self.euclidean_distance(embedding_vectors, k=k, filters=filters)

        error_message = "Invalid Similarity Operation {}".format(similarity_operation)
        raise ValueError(error_message)

    def cosine_similarity(self, embedding_vectors: list[float], k: int = 4,
                          filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:

        embedding_vectors_string = self.convert_embedding_to_json_array(embedding_vectors)

        subquery = (AzureSQLBaseVectorSearchClient
                    .prepare_filter_query(filters, "record_id",
                                          self.vector_metadata_table_name))

        select_statement = """
                   SELECT TOP({}) record_id, 1-VECTOR_DISTANCE('cosine', JSON_ARRAY_TO_VECTOR('{}'), vector_embeddings) AS cosine_distance
                   FROM {}
                   {}
                   ORDER BY cosine_distance desc
                """.format(k, embedding_vectors_string, self.vector_embeddings_table_name, subquery)

        return self.__compute_similarity(select_statement)

    def inner_product(self, embedding_vectors: list[float], k: int = 4,
                      filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:

        embedding_vectors_string = self.convert_embedding_to_json_array(embedding_vectors)

        subquery = (AzureSQLBaseVectorSearchClient
                    .prepare_filter_query(filters, "record_id",
                                          self.vector_metadata_table_name))

        select_statement = """
                           SELECT TOP ({})record_id, ABS(VECTOR_DISTANCE('dot', JSON_ARRAY_TO_VECTOR('{}'), vector_embeddings)) AS inner_product
                           FROM {}
                           {}
                           ORDER BY inner_product desc
                        """.format(k, embedding_vectors_string, self.vector_embeddings_table_name, subquery)

        return self.__compute_similarity(select_statement)

    def euclidean_distance(self, embedding_vectors: list[float], k: int = 4,
                           filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:

        embedding_vectors_string = self.convert_embedding_to_json_array(embedding_vectors)

        subquery = (AzureSQLBaseVectorSearchClient
                    .prepare_filter_query(filters, "record_id",
                                          self.vector_metadata_table_name))

        select_statement = """
                           SELECT TOP({}) record_id, VECTOR_DISTANCE('euclidean', JSON_ARRAY_TO_VECTOR('{}'), vector_embeddings) AS euclidean_distance
                           FROM {}
                           {}
                           ORDER BY euclidean_distance asc
                                """.format(k, embedding_vectors_string, self.vector_embeddings_table_name, subquery)

        return self.__compute_similarity(select_statement)

    def __compute_similarity(self, select_statement: str) -> list[VectorSearchResult]:
        conn = self.engine.connect()
        metadata_table = self.vector_metadata_table_name
        return AzureSQLBaseVectorSearchClient.execute_distance_computation(conn, select_statement, metadata_table)

    def __str__(self):
        json_object = {
            "embeddings_table": self.vector_embeddings_table_name,
            "metadata_table": self.vector_metadata_table_name,
            "connection_string": self.connection_string
        }
        return json.dumps(json_object, indent=True)

    def __repr__(self):
        return self.__str__()
