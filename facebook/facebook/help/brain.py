small_step = 100000

class brain():
    def __init__(self):
        self.recent_identifiers = []
        self.current_step = small_step
        self.new_users = 0
        self.reached_start = False

    def is_duplicate(self, comment: dict) -> bool:
        identifier = str(comment["timestamp"]) + comment["name"]
        print(identifier)
        if identifier in self.recent_identifiers:
            return True
         
        self.new_users += 1
        self.update_duplicates(identifier)
        return False
    
    def update_duplicates(self, new_identifier: str):
        if len(self.recent_identifiers) > 100:
            self.recent_identifiers.pop(0)

        self.recent_identifiers.append(new_identifier)
    
    def calculate_next_step(self):
        if self.reached_start:
            if self.new_users < 2:
                self.current_step += int(self.current_step / 5)
            elif self.new_users > 2:
                self.current_step -= int(self.current_step / 3)
        else: 
            if self.new_users > 0:
                self.reached_start = True
                self.current_step = small_step

    def step(self) -> int:
        self.calculate_next_step()
        self.new_users = 0
        print("Step: ---------------------------{}".format(self.current_step))
        return self.current_step