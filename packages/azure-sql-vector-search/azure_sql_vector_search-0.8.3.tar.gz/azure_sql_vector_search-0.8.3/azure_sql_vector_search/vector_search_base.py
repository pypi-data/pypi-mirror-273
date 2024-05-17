import json
import numbers
from abc import abstractmethod
from typing import Any, Optional

import numpy as np
from sqlalchemy import create_engine, Connection, text
from sqlalchemy.engine import URL

from azure_sql_vector_search.models import DistanceMetric, VectorSearchResult


class AzureSQLBaseVectorSearchClient:
    """
    Base class for Azure SQL Vector Search Clients
    """

    def __init__(self, connection_string: str, table_name: str):
        """
        Constructor for Azure SQL Vector Search Client

        :param connection_string: The connection string to connect to Azure SQL Database
        :param table_name: the table prefix
        """
        self.connection_string = connection_string
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        self.engine = create_engine(connection_url)

    @staticmethod
    def validate_vector_magnitude(embeddings: list[float]):
        """
        Validates the vector magnitude

        :param embeddings:
        :exception Throws an exception if the magnitude is zero
        :return:
        """
        if embeddings is None or len(embeddings) == 0:
            raise ValueError("Embeddings cannot be empty")

        v_magnitude = AzureSQLBaseVectorSearchClient.vector_magnitude(embeddings)

        error_message = ("Vectors with Zero magnitude are not valid: {} has a magnitude of zero".format(embeddings))

        if v_magnitude == 0:
            raise ValueError(error_message)

    @staticmethod
    def vector_magnitude(embedding: list[float]) -> float:
        """
        Computes the vector magnitude of the embedding

        :param embedding:
        :return:
        """
        x = np.array(embedding)
        mag_dot: float = np.sqrt(x.dot(x))
        return mag_dot

    @staticmethod
    def convert_embedding_to_json_array(embedding: list[float]):
        return json.dumps(embedding)

    @staticmethod
    def prepare_filter_argument(metadata_field_name: str, field_value: Any):
        if field_value is None or field_value == '':
            return "JSON_VALUE(metadata, '$.{}') = ''".format(metadata_field_name)
        elif isinstance(field_value, bool):
            return "JSON_VALUE(metadata, '$.{}') = '{}'".format(metadata_field_name, str(field_value).lower())
        elif isinstance(field_value, numbers.Number):
            return "JSON_VALUE(metadata, '$.{}') = {}".format(metadata_field_name, field_value)
        else:
            return "JSON_VALUE(metadata, '$.{}') = '{}'".format(metadata_field_name, field_value)

    @staticmethod
    def prepare_filter_query(metadata_filter: dict[str, object], id_field_name: str, subquery_table: str) -> str:
        # stop here if the metadata filter is empty
        if metadata_filter is None:
            return ""

        if isinstance(metadata_filter, dict) is False:
            return ""

        metadata_column_names = list(metadata_filter.keys())

        # the metadata column names are empty, stop here
        if len(metadata_column_names) == 0:
            return ""

        metadata_filters: list[str] = []

        # prepare the sub=-query filters
        for metadata_column_name in metadata_column_names:
            current_value = metadata_filter[metadata_column_name]
            current_filter = AzureSQLBaseVectorSearchClient.prepare_filter_argument(metadata_column_name, current_value)
            metadata_filters.append(current_filter)

        filter_string = " AND ".join(metadata_filters)

        return ("WHERE {} IN (SELECT {} FROM {} WHERE {})".
                format(id_field_name, id_field_name, subquery_table, filter_string))

    @staticmethod
    def execute_distance_computation(connection: Connection,
                                     select_statement: str, metadata_table: str) -> list[VectorSearchResult]:

        sql_statement = text(select_statement)

        select_result = connection.execute(sql_statement)

        result = select_result.fetchall()

        scoring_results: list[dict] = []

        record_identifiers = []

        for row in result:
            record_id = str(row[0])
            record_id_value = int(record_id)
            score: float = float(row[1])
            record_identifiers.append(record_id)
            scoring_results.append({"record_id": record_id_value, "distance_score": score})

        if len(scoring_results) == 0:
            return []

        record_identifiers_filter = ",".join(record_identifiers)

        metadata_select = ("SELECT record_id, content, metadata, vector_content FROM {} WHERE record_id IN ({})"
                           .format(metadata_table, record_identifiers_filter))

        metadata_select_result = connection.execute(text(metadata_select))
        metadata_results = metadata_select_result.fetchall()

        final_results: list[VectorSearchResult] = []

        result_map: dict = {}

        for metadata_row in metadata_results:
            record_id = int(metadata_row[0])
            lookup_key = str(metadata_row[0])
            vector_content = json.loads(metadata_row[3])
            metadata_object = {"id": record_id, "content": metadata_row[1],
                               "metadata": metadata_row[2], "vector_content": vector_content}
            result_map[lookup_key] = metadata_object

        for score_object in scoring_results:
            identifier = str(score_object["record_id"])
            row = result_map[identifier]
            row.update(score_object)
            final_results.append(row)

        return final_results

    @abstractmethod
    def truncate_tables(self):
        """
        Deletes all the records from the vector search tables
        :return:
        """
        pass

    @abstractmethod
    def delete_by_id(self, record_id: int):
        """
        Deletes a specific record from the vector search tables
        :param record_id:
        :return:
        """
        pass

    @abstractmethod
    def insert_row(self, content: str, metadata: dict, embeddings: list[float]):
        """
        Inserts data into the vector store

        :param content: the string content to be inserted
        :param metadata: a dictionary containing the metadata associated with the content
        :param embeddings: a vector representation of the content to be stored in the vector store
        :return:
        """
        pass

    @abstractmethod
    def compute_similarity(self, embedding_vectors: list[float], similarity_operation: DistanceMetric, k: int = 4,
                           filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:
        """
        Computes the Similarity Metric between the query vector and the records in the vector store

        :param embedding_vectors: The query vector
        :param similarity_operation: The similarity operation to be performed on the query vector
        :param k: the number of nearest neighbors to return
        :param filters: the dictionary containing the filters to be matched with the metadata
        :return:
        """
        pass

    @abstractmethod
    def cosine_similarity(self, embedding_vectors: list[float], k: int = 4,
                          filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:
        """
        Computes the Cosine Similarity between the query vector and the records in the vector store

        :param embedding_vectors: The query vector
        :param k: the number of nearest neighbors to return
        :param filters: the dictionary containing the filters to be matched with the metadata
        :return:
        """
        pass

    @abstractmethod
    def inner_product(self, embedding_vectors: list[float], k: int = 4,
                      filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:
        """
        Computes the Inner or Dot Product between the query vector and the records in the vector store

        :param embedding_vectors: The query vector
        :param k: the number of nearest neighbors to return
        :param filters: the dictionary containing the filters to be matched with the metadata
        :return:
        """

    @abstractmethod
    def euclidean_distance(self, embedding_vectors: list[float], k: int = 4,
                           filters: Optional[dict[str, object]] = None) -> list[VectorSearchResult]:
        """
        Computes the Euclidean Distance between the query vector and the records in the vector store

        :param embedding_vectors: The query vector
        :param k: the number of nearest neighbors to return
        :param filters: the dictionary containing the filters to be matched with the metadata
        :return:
        """
        pass
