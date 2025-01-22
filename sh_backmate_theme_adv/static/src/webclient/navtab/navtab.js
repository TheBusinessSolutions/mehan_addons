/** @odoo-module **/

const { Component, hooks } = owl;
// import { registry } from "@web/core/registry";
// import { ErrorHandler, NotUpdatable } from "@web/core/utils/components";
// import { getMessagingComponent } from '@mail/utils/messaging_component';

// const systrayRegistry = registry.category("systray");
// systrayRegistry.add('mail.MessagingMenu', {
//     Component: getMessagingComponent('MessagingMenu'),
// });
// systrayRegistry.add('mail.RtcActivityNotice', {
//     Component: getMessagingComponent('RtcActivityNotice'),
// });
import { useService } from "@web/core/utils/hooks";


export class NavTab extends Component {
    setup() {
        super.setup();
        this.actionService = useService("action");
        }
        // get systrayItems() {
        //     return systrayRegistry
        //         .getEntries()
        //         .map(([key, value]) => ({ key, ...value }))
        //         .filter((item) => ("isDisplayed" in item ? item.isDisplayed(this.env) : true))
        //         .reverse();
        // }
    
        // _onNavItemClick() {
        //     alert("e")
        //     this.actionService.restore('controller_2');
        // }
    }
   
    // $(document).ready(function () {

	// 	$('.o_web_client').on('click', '.sh_nav_item', function (event) {
    //         console.log(">>>>>>>>>>.",$(this).data('controller')) 
                
           
	// 	});
    // });

    

    NavTab.template = 'sh_backmate_theme_adv.NavTab';
// NavFooter.components = { NotUpdatable, ErrorHandler };
