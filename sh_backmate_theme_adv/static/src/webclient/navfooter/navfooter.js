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

export class NavFooter extends Component {
    setup() {
        super.setup();
        }
        // get systrayItems() {
        //     return systrayRegistry
        //         .getEntries()
        //         .map(([key, value]) => ({ key, ...value }))
        //         .filter((item) => ("isDisplayed" in item ? item.isDisplayed(this.env) : true))
        //         .reverse();
        // }
    

    }
    

NavFooter.template = 'sh_backmate_theme_adv.NavFooter';
// NavFooter.components = { NotUpdatable, ErrorHandler };
