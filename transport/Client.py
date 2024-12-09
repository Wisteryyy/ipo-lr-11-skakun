class Client:
    def __init__(self, name, cargo_weight, is_vip):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

    def to_dict(self):
        return {
            'name': self.name,
            'cargo_weight': self.cargo_weight,
            'is_vip': self.is_vip
        }
