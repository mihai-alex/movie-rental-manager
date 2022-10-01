from src.iterable_data_structure import MyIterator


class UndoRedoRepository:
    def __init__(self):
        # self._undo_operations = []
        # self._undo_converses = []
        # self._redo_operations = []
        # self._redo_converses = []
        self._undo_operations = MyIterator()
        self._undo_converses = MyIterator()
        self._redo_operations = MyIterator()
        self._redo_converses = MyIterator()

    @property
    def undo_operations(self):
        return self._undo_operations[-1]

    @property
    def undo_converses(self):
        return self._undo_converses[-1]

    @property
    def redo_operations(self):
        return self._redo_operations[-1]

    @property
    def redo_converses(self):
        return self._redo_converses[-1]

    def is_undo_empty(self):
        if len(self._undo_operations) == 0:
            return True
        else:
            return False

    def is_redo_empty(self):
        if len(self._redo_operations) == 0:
            return True
        else:
            return False

    def add_undo_operation(self, objects):
        self._undo_operations.append(objects)

    def add_undo_converse(self, objects):
        self._undo_converses.append(objects)

    def remove_undo(self):
        return self._undo_operations.pop(), self._undo_converses.pop()

    def add_redo_operation(self, objects):
        self._redo_operations.append(objects)

    def add_redo_converse(self, objects):
        self._redo_converses.append(objects)

    def remove_redo(self):
        return self._redo_operations.pop(), self._redo_converses.pop()

    def clear_redo(self):
        self._redo_operations.clear()
        self._redo_converses.clear()
