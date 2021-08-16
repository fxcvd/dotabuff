from .DotaBuff import DotaBuff


class DotaBuffPlayer(DotaBuff):
    def __init__(self, player_id):
        self.player = player_id

    async def get_matches(self, page=1, max_count=50):
        return await DotaBuff.get_matches(self, player=self.player, max_count=max_count, page=page)