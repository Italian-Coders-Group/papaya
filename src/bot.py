import os
from pathlib import Path


os.chdir('src')

os.environ['TOKEN'] = Path('../.env').read_text().split('\n')[0].split('=')[1]

import PapayaBot