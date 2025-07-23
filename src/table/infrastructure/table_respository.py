from abc import ABC


class TableRepository(ABC):
    def create(self, table_data):
        pass

    def get_by_id(self, table_id):
        pass

    def update(self, table_id, update_data):
        pass

    def delete(self, table_id):
        pass

    def list(self, filters=None):
        pass


class InMemoryTableRepository(TableRepository):
    pass


class PostgresTableRepository(TableRepository):
    pass


class RedisTableRepository(TableRepository):
    pass
