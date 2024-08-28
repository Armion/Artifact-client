class Skills:
    def __init__(self, data: dict) -> None:
        self.data = data

    def get_skill(self, skill_name: str):
        return {
            'name': skill_name,
            'lvl': self.data.get(f'{skill_name}_level'),
            'required_xp': self.data.get(f'{skill_name}_max_xp')
        }