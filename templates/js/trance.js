hs.graphicsDir = 'highslide/graphics/';
hs.showCredits = false;
hs.outlineType = 'custom';
hs.dimmingOpacity = 0.85;
hs.fadeInOut = true;
hs.easing = 'linearTween';
hs.expandDuration = 100;
hs.restoreDuration = 100;
hs.align = 'center';
hs.allowMultipleInstances = false;
hs.enableKeyListener = false;
hs.registerOverlay({
	html: '<div class="close-simple-white" onclick="return hs.close(this)" title="Close"></div>',
	position: 'top right',
	useOnHtml: true,
	fade: 2 // fading the semi-transparent overlay looks bad in IE
});

