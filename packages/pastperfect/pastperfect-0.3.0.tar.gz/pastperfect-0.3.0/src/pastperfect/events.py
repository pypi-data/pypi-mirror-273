from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterator, Optional

from turbofan.database import text  # type: ignore


@dataclass(frozen=True)
class Event:
    name: str
    data: dict
    id: Optional[int] = None
    created_at: Optional[datetime] = field(default_factory=datetime.utcnow)


class Events:
    """
    A list of events.
    """

    def __init__(self, db_session: Any):
        super().__init__()
        self._session = db_session

    def __len__(self) -> int:
        sql_stmt = """SELECT COUNT(*) FROM event"""
        prepared_statement = text(sql_stmt)
        row = self._session.execute(prepared_statement).first()
        return row[0]

    def append(self, event: Event) -> Events:
        """
        Appends an event to the list of events.
        """
        sql_stmt = """INSERT INTO event (name, data, created_at) VALUES (:name, :data, :created_at)"""
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(
            name=event.name,
            data=json.dumps(event.data),
            created_at=event.created_at,
        )
        self._session.execute(prepared_statement)

        return self

    def replay(self, handlers, name: Optional[str] = None):
        """
        Replays events with the option of filtering by the event name.
        """
        if not name:
            sql_stmt = (
                """SELECT id, name, data, created_at FROM event ORDER BY id ASC"""
            )
            prepared_statement = text(sql_stmt)
        else:
            sql_stmt = """SELECT id, name, data, created_at FROM event WHERE name=:name ORDER BY id ASC"""
            prepared_statement = text(sql_stmt)
            prepared_statement = prepared_statement.bindparams(name=name)

        results = self._session.execute(prepared_statement)
        for row in results:
            e = Event(
                id=row[0],
                name=row[1],
                data=json.loads(row[2]),
                created_at=row[3],
            )
            for handler in handlers:
                handler(e)

    def __getitem__(self, idx: int) -> Event:
        if idx < 0:
            offset = idx * -1 - 1
            sql_stmt = """SELECT id, name, data, created_at FROM event ORDER BY id DESC LIMIT 1 OFFSET :offset"""
            prepared_statement = text(sql_stmt)
            prepared_statement = prepared_statement.bindparams(offset=offset)
        else:
            sql_stmt = """SELECT id, name, data, created_at FROM event ORDER BY id ASC LIMIT 1 OFFSET :offset"""
            prepared_statement = text(sql_stmt)
            prepared_statement = prepared_statement.bindparams(offset=idx)

        row = self._session.execute(prepared_statement).first()
        if not row:
            raise IndexError

        return Event(id=row[0], name=row[1], data=json.loads(row[2]), created_at=row[3])

    def __iter__(self) -> Iterator[Event]:
        sql_stmt = """SELECT id, name, data, created_at FROM event ORDER BY id ASC"""
        prepared_statement = text(sql_stmt)
        results = self._session.execute(prepared_statement)
        for row in results:
            yield Event(
                id=row[0], name=row[1], data=json.loads(row[2]), created_at=row[3]
            )
