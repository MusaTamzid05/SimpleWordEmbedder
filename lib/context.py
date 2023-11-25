from collections import deque

class Context:
    def __init__(self):
        self.model_data = deque() # thread safe 
        self.last_model_name = ""
        self.last_word_generator = None


    def add(self, model_name, epochs, loss):
        found = False


        for i in range(len(self.model_data)):
            current_model_name = self.model_data[i]["name"]

            if current_model_name == model_name:
                self.model_data[i] = {
                    "name" : model_name,
                    "epochs" : epochs,
                    "loss" : loss
                    }
                found = True
                break

        if found:
            return


        self.model_data.append({
            "name" : model_name,
            "epochs" : epochs,
            "loss" : loss
            })



context = Context()
