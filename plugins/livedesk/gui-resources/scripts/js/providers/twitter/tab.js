define(['providers'], function(providers) {	providers.twitter = {		className: 'big-icon-twitter',			tooltip: _('Twitter'),		init: function() {		    $('.' + this.className).closest('a').find('.config-notif').hide();			require(['providers','providers/twitter'], function(providers) {				providers.twitter.init();			});		}	};	return providers;});