'''
Created on Jan 25, 2012

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configurations for the encoder text.
'''

from ..test_support import EncoderGetObj
from .converter import contentNormalizer, converterPath
from .resource_manager import resourcesManager
from ally.container import ioc
from ally.core.impl.processor.encoder_text import EncodingTextHandler
from ally.core.impl.processor.meta_creator import MetaCreatorHandler
from ally.core.spec.server import Processor, Processors

# --------------------------------------------------------------------

@ioc.entity
def encoder(): return EncoderGetObj()

@ioc.entity
def encoderText() -> Processor:
    b = EncodingTextHandler()
    b.resourcesManager = resourcesManager()
    b.normalizer = contentNormalizer()
    b.converterId = converterPath()
    b.encoder = encoder()
    b.charSetDefault = 'UTF-8'
    b.contentTypes = {None:None}
    b.encodingError = 'backslashreplace'
    return b

@ioc.entity
def metaCreator() -> Processor:
    b = MetaCreatorHandler()
    b.resourcesManager = resourcesManager()
    return b

@ioc.entity
def encoderProcessors():
    return Processors(metaCreator(), encoderText())

@ioc.entity
def encoderTextProcessors():
    return Processors(encoderText())

@ioc.entity
def encoderCreateMetaProcessors():
    return Processors(metaCreator())