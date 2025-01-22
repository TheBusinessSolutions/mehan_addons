/** @odoo-module **/

const { Component, hooks } = owl;
const rpc = require("web.rpc");
const session = require("web.session");

var show_zoom = false
rpc.query({
    model: 'res.users',
    method: 'search_read',
    fields: ['sh_enable_zoom'],
    domain: [['id', '=', session.uid]]
}, { async: false }).then(function (data) {
    if (data) {
        _.each(data, function (user) {
            if (user.sh_enable_zoom) {
               
                show_zoom = true
            }
        });

    }
});

export class ZoomWidget extends Component {
    setup() {
        super.setup();
        this.show_zoom = show_zoom;        
    }
    setResetZoom(){
        var zoom = $('.sh_full').text().split('%')
        $($('.o_content')[0].firstChild).removeClass("sh_zoom_"+zoom[0])
        zoom = 100
        $('.sh_full').text(zoom.toString()+'%');
        $($('.o_content')[0].firstChild).addClass("sh_zoom_"+zoom)
    }
    setDecZoom(){
        var zoom = $('.sh_full').text().split('%')
        if(parseInt(zoom[0])-10 >= 20 && parseInt(zoom[0])-10 <= 200){
            $($('.o_content')[0].firstChild).removeClass("sh_zoom_"+zoom[0])
            zoom = parseInt(zoom[0])-10
            $('.sh_full').text(zoom.toString()+'%');
            $($('.o_content')[0].firstChild).addClass("sh_zoom_"+zoom)
        }
        
    }
    setIncZoom(){
        var zoom = $('.sh_full').text().split('%')
        if(parseInt(zoom[0])+10 >= 20 && parseInt(zoom[0])+10 <= 200){

            $($('.o_content')[0].firstChild).removeClass("sh_zoom_"+zoom[0])
            zoom = parseInt(zoom[0])+10
            $('.sh_full').text(zoom.toString()+'%');
            $($('.o_content')[0].firstChild).addClass("sh_zoom_"+zoom)
        }
       
    }

}
    

ZoomWidget.template = 'sh_backmate_theme_adv.ZoomWidget';
// NavFooter.components = { NotUpdatable, ErrorHandler };
