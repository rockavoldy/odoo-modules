odoo.define('pos_payment_unique.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    
    const PaymentScreenHideMethods = PaymentScreen =>
        class extends PaymentScreen {
            hidePaymentMethods() {
                // Hide the payment methods if it already in paymentLines
                let hidePaymentMethods = [];
                let paymentlines = this.currentOrder.get_paymentlines();
                if (paymentlines.length > 0) {
                    paymentlines.forEach(element => {
                        hidePaymentMethods.push(element.payment_method.id);
                    });
                }
                
                this.payment_methods_from_config = this.env.pos.payment_methods.filter(method => !(hidePaymentMethods.includes(method.id)));

            }
            get paymentLines() {
                // When paymentLines already have 1 method, re-render payment methods
                const paymentlines = super.paymentLines;
                if (paymentlines.length > 0) {
                    this.hidePaymentMethods();
                }

                return paymentlines;
            }

            addNewPaymentLine({ detail: paymentMethod }) {
                // When add new paymentLine, hide the payment method from the list
                let successAddPayment = super.addNewPaymentLine(...arguments);
                if (successAddPayment) {
                    this.hidePaymentMethods();
                }

                return successAddPayment;
            }

            deletePaymentLine(event) {
                // When delete the paymentLine, repopulate the paymentMethods to the list
                const { cid } = event.detail;
                const line = this.paymentLines.find((line) => line.cid === cid);
                super.deletePaymentLine(...arguments);
                if (this.paymentLines.length === 0) {
                    this.hidePaymentMethods();
                }
            }
    }

    Registries.Component.extend(PaymentScreen, PaymentScreenHideMethods);

    return PaymentScreen;

});