class Config:
    def __init__(self,
                 resolution_name: str,
                 screen_width: int,
                 screen_height: int):
        self.resolution_name = resolution_name.lower()
        self.screen_width = screen_width
        self.screen_height = screen_height
