define([ 'jquery','jquery/superdesk', 'gizmo/superdesk/action' ],
function($, superdesk, Action)
{
    return { init: function() 
    {
        Action.get('modules.article.list')
        .done(function(action)
        {
            if(action.get('Path') == 'modules.article.list' && action.get('Script'))
                require([action.get('Script').href], function(app){ app(); });
        });
    }};
});