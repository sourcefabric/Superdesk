define([
	'plugins/wrappup-toggle',
	'plugins/permanent-link',
	'plugins/twitter-widgets',
	'css!theme/liveblog',
	'tmpl!theme/container',
	'tmpl!theme/item/base',
	'tmpl!theme/item/source/youtube'
], function(){
	return {
		plugins: [ 'wrappup-toggle', 
					'permanent-link',
					'twitter-widgets'
					]
	}
});