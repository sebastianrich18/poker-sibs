from abc import ABC


class TableRepository(ABC):
    @abstractmethod
    def create(self, table_data):
        pass

    @abstractmethod
    def get_by_id(self, table_id):
        pass

    @abstractmethod
    def update(self, table_id, update_data):
        pass

    @abstractmethod
    def delete(self, table_id):
        pass

    @abstractmethod
    def list(self, filters=None):
        pass


class InMemoryTableRepository(TableRepository):
    pass


class PostgresTableRepository(TableRespository):
    pass


class RedisTableRepository(TableRespository):
    pass
