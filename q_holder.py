import pickle

class QTable:
    table = {}

    def load_q_table(self):
        self.table = pickle.load(open('q.tictactoe', 'rb'))
        print("table len", len(self.table))

    def save_q_table(self):
        print(len(self.table))
        pickle.dump(self.table, open('q.tictactoe', 'wb'))