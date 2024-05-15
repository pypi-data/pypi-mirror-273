"""Klasse `DatabaseConnector`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("DatabaseConnector",)

import sqlite3
from typing import Final

from nrw.database._query_result import QueryResult


class DatabaseConnector:
    """Ein Objekt der Klasse `DatabaseConnector` ermöglicht die Abfrage und
    Manipulation einer `SQLite`-Datenbank.
    Beim Erzeugen des Objekts wird eine Datenbankverbindung aufgebaut, so dass
    anschließend SQL-Anweisungen an diese Datenbank gerichtet werden koennen.
    """

    # pylint: disable=W0613, W0718, R0913

    __slots__: Final[tuple[str, str, str]] = (
        "_connection",
        "_current_query_result",
        "_message",
    )

    def __init__(
        self,
        ip: None,
        port: None,
        database: str,
        username: None,
        password: None,
    ) -> None:
        """Ein Objekt vom Typ `DatabaseConnector` wird erstellt, und eine Verbindung zur
        Datenbank wird aufgebaut. Mit den Parametern `ip` und `port` werden die
        IP-Adresse und die Port-Nummer übergeben, unter denen die Datenbank mit Namen
        `database` zu erreichen ist.
        Mit den Parametern `username` und `password` werden Benutzername und Passwort
        für die Datenbank übergeben.

        Für `SQLite` wird nur `database` benötigt.
        """
        self._current_query_result: QueryResult | None = None
        self._message: str | None = None

        try:
            self._connection: sqlite3.Connection | None = sqlite3.connect(
                database,
                isolation_level=None,
            )
        except Exception as exception:
            self._connection = None
            self._message = str(exception)

    def execute_statement(self, sql_statement: str) -> None:
        """Der Auftrag schickt den im Parameter `sql_statement` enthaltenen SQL-Befehl
        an die Datenbank ab.
        Handelt es sich bei `sql_statement` um einen SQL-Befehl, der eine Ergebnismenge
        liefert, so kann dieses Ergebnis anschließend mit dem Property
        `current_query_result` abgerufen werden.
        """
        self._current_query_result = None
        self._message = None

        if self._connection is None:
            self._message = "No connection"
            return

        try:
            cursor: sqlite3.Cursor = self._connection.cursor()
        except Exception as exception:
            self._message = str(exception)
            return

        try:
            if cursor.execute(sql_statement) is not None and (
                data := cursor.fetchall()
            ):
                assert cursor.description is not None, "No description"
                column_names: tuple[str, ...] = tuple(
                    column[0] for column in cursor.description
                )
                colum_types: tuple[None, ...] = tuple(
                    column[1] for column in cursor.description
                )
                self._current_query_result = QueryResult(
                    data,
                    column_names,
                    colum_types,
                )
        except Exception as exception:
            self._message = str(exception)
        finally:
            cursor.close()

    @property
    def current_query_result(self) -> QueryResult | None:
        """Die Anfrage liefert das Ergebnis des letzten mit der Methode
        `execute_statement` an die Datenbank geschickten SQL-Befehls als Objekt vom Typ
        `QueryResult` zurück.
        Wurde bisher kein SQL-Befehl abgeschickt oder ergab der letzte Aufruf von
        `execute_statement` keine Ergebnismenge (z.B. bei einem INSERT-Befehl oder einem
        Syntaxfehler), so wird `None` geliefert.
        """
        return self._current_query_result

    @property
    def error_message(self) -> str | None:
        """Die Anfrage liefert `None` oder eine Fehlermeldung, die sich jeweils auf die
        letzte zuvor ausgefuehrte Datenbankoperation bezieht.
        """
        return self._message

    def close(self) -> None:
        """Die Datenbankverbindung wird geschlossen."""
        if self._connection is None:
            self._message = "No connection"
            return

        try:
            self._connection.close()
        except Exception as exception:
            self._message = str(exception)
