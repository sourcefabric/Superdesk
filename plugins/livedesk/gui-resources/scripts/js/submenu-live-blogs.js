requirejs.config({
	paths: { 
		'providers': config.gui('livedesk/scripts/js/providers'), 
		'livedesk/models': config.gui('lib/livedesk/scripts/js/models'), 
		'livedesk/collections': config.gui('lib/livedesk/scripts/js/collections/') 
} });
define
([
  'jquery', 'jquery/superdesk',
  'gizmo/superdesk',
  config.guiJs('livedesk', 'models/blog'),
  'jquery/tmpl', 'jquery/rest',
  'tmpl!livedesk>submenu'
], function($, superdesk, Gizmo, Blog)
{
    var Blogs = Gizmo.Collection.extend({model: Blog, href: new Gizmo.Url('LiveDesk/Blog') }), 
        b = Gizmo.Auth(new Blogs());
    
    var SubmenuView = Gizmo.View.extend
    ({
        init: function()
        {
            this.model.on('read update', this.render, this);
        },
        refresh: function()
        {
            this.model._list = [];
            this.model.xfilter('Title, Id').sync();
        },
        render: function()
        {
            $(this.menu).on('click', '#submenu-liveblogs-archive', function(event)
            {
                var self = this;
                superdesk.showLoader();
                superdesk.getAction('modules.livedesk.archive')
                .done(function(action)
                {
                    var callback = function()
                    { 
                        require([action.Script.href], function(app){ new app(); });
                    };
                    action.Script && superdesk.navigation.bind( $(self).attr('href'), callback, $(self).text() );
                }); 
                event.preventDefault();
            });
            
            $(this.menu).on('click', '#submenu-liveblogs-create', function(event)
            {
                superdesk.showLoader();
                superdesk.getAction('modules.livedesk.add')
                .done(function(action)
                {
                    action.Script &&
                        require([action.Script.href], function(AddApp){ addApp = new AddApp(); });
                }); 
                event.preventDefault();
            });
            $(this.menu).on('click', '.submenu-blog', function(event)
            {
                superdesk.showLoader();
                var theBlog = $(this).attr('data-blog-link'), self = this;
                superdesk.getAction('modules.livedesk.edit')
                .done(function(action)
                {
                    if(!action) return;
                    var callback = function()
                    { 
                        require([action.Script.href], function(EditApp){ EditApp(theBlog); }); 
                    };
                    action.Script && superdesk.navigation.bind( $(self).attr('href'), callback, $(self).text() );
                });
                event.preventDefault();
            });
            var self = this;
            /*!
             * apply template and go to selected blog if any
             */
            this.menu.tmpl('livedesk>submenu', {Blogs: this.model.feed()}, function()
            {
                if( superdesk.navigation.getStartPathname() == '') return false;
                self.menu.find('[href]').each(function()
                {
                    if( $(this).attr('href').replace(/^\/+|\/+$/g, '') == superdesk.navigation.getStartPathname())
                    {
                        superdesk.navigation.consumeStartPathname();
                        $(this).trigger('click');
                    }
                });
            }); 
        }
    });
    
    var subMenu = new SubmenuView({model: b});
    return {
        init: function(submenu, menu)
        { 
            subMenu.menu = $(submenu);
            subMenu.refresh();
            return subMenu; 
        }
    };
});