'''
Created on May 4, 2012

@package: livedesk
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for blog API.
'''

from ..api.blog import IBlogService, QBlog, Blog
from ..meta.blog import BlogMapped
from ally.api.extension import IterPart
from ally.container.ioc import injected
from ally.container.support import setup
from ally.exception import InputError, Ref
from ally.internationalization import _
from ally.support.sqlalchemy.util_service import buildQuery, buildLimits
from livedesk.meta.blog_collaborator import BlogCollaboratorMapped
from sql_alchemy.impl.entity import EntityCRUDServiceAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import exists
from sqlalchemy.sql.functions import current_timestamp
from superdesk.collaborator.meta.collaborator import CollaboratorMapped

# --------------------------------------------------------------------

@injected
@setup(IBlogService)
class BlogServiceAlchemy(EntityCRUDServiceAlchemy, IBlogService):
    '''
    Implementation for @see: IBlogService
    '''

    def __init__(self):
        '''
        Construct the blog service.
        '''
        EntityCRUDServiceAlchemy.__init__(self, BlogMapped)

    def getBlog(self, blogId):
        '''
        @see: IBlogService.getBlog
        '''
        sql = self.session().query(BlogMapped)
        sql = sql.filter(BlogMapped.Id == blogId)

        try: return sql.one()
        except NoResultFound: raise InputError(Ref(_('Unknown id'), ref=Blog.Id))

    def getAll(self, languageId=None, userId=None, offset=None, limit=None, detailed=False, q=None):
        '''
        @see: IBlogService.getAll
        '''
        sql = self._buildQuery(languageId, userId, q)
        sqlLimit = buildLimits(sql, offset, limit)
        if detailed: return IterPart(sqlLimit.all(), sql.count(), offset, limit)
        return sqlLimit.all()

    def getLive(self, languageId=None, q=None):
        '''
        @see: IBlogService.getLive
        '''
        sql = self._buildQuery(languageId, None, q)
        sql = sql.filter((BlogMapped.ClosedOn == None) & (BlogMapped.LiveOn != None))
        return sql.all()

    def putLive(self, blogId):
        '''
        @see: IBlogService.putLive
        '''
        blog = self.session().query(BlogMapped).get(blogId)
        if not blog: raise InputError(_('Invalid blog or credentials')) 
        assert isinstance(blog, Blog), 'Invalid blog %s' % blog
        blog.LiveOn = current_timestamp() if blog.LiveOn is None else None
        self.session().merge(blog)


    def insert(self, blog):
        '''
        @see: IBlogService.insert
        '''
        assert isinstance(blog, Blog), 'Invalid blog %s' % blog
        if blog.CreatedOn is None: blog.CreatedOn = current_timestamp()
        return super().insert(blog)

    # ----------------------------------------------------------------

    def _buildQuery(self, languageId=None, userId=None, q=None):
        '''
        Builds the general query for blogs.
        '''
        sql = self.session().query(BlogMapped)
        if languageId: sql = sql.filter(BlogMapped.Language == languageId)
        if userId:
            userFilter = (BlogMapped.Creator == userId) | exists().where((CollaboratorMapped.User == userId) \
                                         & (BlogCollaboratorMapped.blogCollaboratorId == CollaboratorMapped.Id) \
                                         & (BlogCollaboratorMapped.Blog == BlogMapped.Id))
            sql = sql.filter(userFilter)
            
        if q:
            assert isinstance(q, QBlog), 'Invalid query %s' % q
            sql = buildQuery(sql, q, BlogMapped)
        return sql
