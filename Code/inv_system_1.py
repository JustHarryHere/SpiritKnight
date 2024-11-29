# Quantity of an item
class item_slot:
    def _init_(self):
        self.type = None
        self.amount = 0
        
# Number of slots
class inventory:
    # Create inventory
    def _init_(self, capacity):
        self.capacity = capacity
        self.taken_slots = 0
        self.slots = []
        for _ in range(self.capacity):
            self.slots.append(item_slot())
    
    # Add an amount of item
    def add(self, item_type, amount=1):
        if item_type.stack_size > 1:
            for slot in self.slots:
                if slot.type == item_type:
                    add_amo = amount
                    if add_amo > item_type.stack_size - slot.amount:
                        add_amo = item_type.stack_size - slot.amount
                    slot.amount += add_amo
                    amount -= add_amo
                    if amount <= 0:
                        return
                    
    # Remove item
    def remove(self, item_type, amount=1):    
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount:
                    found += amount
                    slot.amount = 0
                    slot.type = None
                    continue
                elif slot.amount == amount:
                    found += amount
                    slot.amount = 0
                    return found
                else:
                    found += amount
                    slot.amount -= amount
        return found