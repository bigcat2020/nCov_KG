import os
import time
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
#from pyltp import Parser
#from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
import sys
sys.path.append(r"..\Source\nlp")
import nlpltp