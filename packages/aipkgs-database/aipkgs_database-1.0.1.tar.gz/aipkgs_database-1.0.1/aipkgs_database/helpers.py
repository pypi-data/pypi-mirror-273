from aipkgs_core.logger.helpers import print_with_filename
from flask import Flask
from sqlalchemy import event

from aipkgs_database import core


class Database:
    class EventObserver:
        def update(self, table_name, mapper, connection, target):
            pass

    class EventSubject:
        def __init__(self):
            self.observers: [Database.EventObserver] = []

        def add_observer(self, observer):
            self.observers.append(observer)

        def remove_observer(self, observer):
            self.observers.remove(observer)

        def notify_observers(self, table_name, mapper, connection, target):
            for observer in self.observers:
                observer.update(table_name, mapper, connection, target)

        def remove_all_observers(self):
            self.observers.clear()

    event_subject = EventSubject()
    listeners = {}

    @staticmethod
    def listen_to_table_changes(table_model, observer: EventObserver):
        table_name = table_model.__tablename__
        if table_name not in Database.listeners:
            def table_modified(mapper, connection, target):
                table_name = table_model.__tablename__
                name = table_model.__name__
                print_with_filename(f'{name} {target.id} modified')
                Database.event_subject.notify_observers(table_name, mapper, connection, target)

            event.listen(target=table_model, identifier='after_update', fn=table_modified)

            Database.listeners[table_name] = table_modified

        Database.event_subject.add_observer(observer)

    @staticmethod
    def stop_listening_to_tables_changes(table_model):
        table_name = table_model.__tablename__
        if table_name in Database.listeners:
            function = Database.listeners[table_name]
            event.remove(target=table_model, identifier='after_update', fn=function)
