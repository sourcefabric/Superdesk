'''
Created on Apr 19, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the decorator to be used by the models in the superdesk domain.
'''

from functools import partial
from ally.api.config import model

# --------------------------------------------------------------------

DOMAIN = 'Superdesk/'
modelSuperDesk = partial(model, domain=DOMAIN)
