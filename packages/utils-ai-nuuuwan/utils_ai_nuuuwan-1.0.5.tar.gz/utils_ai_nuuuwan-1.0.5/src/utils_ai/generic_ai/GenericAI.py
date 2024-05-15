from utils_ai.generic_ai.GenericAIImage import GenericAIImage
from utils_ai.generic_ai.GenericAIText import GenericAIText


class GenericAI(
    GenericAIText,
    GenericAIImage,
):
    def __init__(self):
        GenericAIText.__init__(self)
        GenericAIImage.__init__(self)
