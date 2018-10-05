small_step = 500000

class brain():
    def __init__(self):
        self.recent_identifiers = []
        self.duplicate_count = 0
        self.current_step = small_step
        self.duplicates_this_step = 1

    def is_duplicate(self, comment: dict) -> bool:
        identifier = str(comment["timestamp"]) + comment["link"]
        if identifier in self.recent_identifiers:
            self.duplicate_count += 1
            self.duplicates_this_step += 1
            print(self.duplicate_count)
            return True
        
        self.update_duplicates(identifier)
        return False
    
    def update_duplicates(self, new_identifier: str):
        if len(self.recent_identifiers) > 100:
            self.recent_identifiers.pop(0)

        self.recent_identifiers.append(new_identifier)
    
    def calculate_next_step(self):
        if self.duplicates_this_step > 1:
            self.current_step += self.current_step / 5
        elif self.duplicates_this_step < 1:
            self.current_step -= self.current_step / 4
    
    def step(self) -> int:
        self.calculate_next_step()
        self.duplicates_this_step = 0
        print("Step: ---------------------------{}".format(self.current_step))
        return self.current_step