'''
Created on Jan 9, 2012

@package Newscoop
@copyright 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services for newscoop.
'''

from ..plugin.registry import addService
from .db_superdesk import bindSuperdeskSession, bindSuperdeskValidations
from ally.container import support, aop

# --------------------------------------------------------------------

API, IMPL = 'superdesk.**.api.**.I*Service', 'superdesk.**.impl.**.*'

support.createEntitySetup(API, IMPL)
support.bindToEntities(IMPL, binders=bindSuperdeskSession)
support.listenToEntities(IMPL, listeners=addService(bindSuperdeskSession, bindSuperdeskValidations))
support.loadAllEntities(API)

# --------------------------------------------------------------------
