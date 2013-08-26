/*
 * Based on the configuration in ../../configure.zcml this JavaScript will only
 * be loaded when the user is looking at an ExampleDevice in the web interface.
 */

(function(){

    var DEVICE_OVERVIEW_ID = 'deviceoverviewpanel_summary';
    Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_ID, function(){
        var overview = Ext.getCmp(DEVICE_OVERVIEW_ID);
        overview.removeField('uptime');

        overview.addField({
            name: 'uptime',
 	    fieldLabel: _t('Uptime')
        });
    });

    var DEVICE_OVERVIEW_ID = 'deviceoverviewpanel_idsummary';
    Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_ID, function(){
        var overview_serial = Ext.getCmp(DEVICE_OVERVIEW_ID);
        overview_serial.removeField('serialNumber');

        overview_serial.addField({
            name: 'serialNumber',
            fieldLabel: _t('Serial Number')
        });
    });


});


})();
