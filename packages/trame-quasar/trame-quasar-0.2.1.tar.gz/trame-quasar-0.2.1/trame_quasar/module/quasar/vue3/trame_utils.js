
                (function () {
                    function bindQuasar() {
                        if (window.Quasar) {
                            window.trame.utils.quasar = window.Quasar;
                        } else {
                            setTimeout(bindQuasar, 100);
                        }
                    }
                    bindQuasar();
                })();
            