 $('.txtfld').bind({
            keyup:function(){ 
         //total calculation
                    $(".printer-type tr:not(:first, last) td:last-child").text(function () {
                        var totalVal = 0;
                        $(this).prevAll().each(function () {
                            totalVal += parseInt($(this).children('.txtfld').val()) || 0;
                            //totalVal += parseInt( );
                        });
                        return totalVal;
                    });

                    $(".printer-type tr:last td").text(function (i) {
                        var totalVal = 0;
                        $(this).parent().prevAll().find("td:nth-child(" + (++i) + ")").each(function () {
                            totalVal += parseInt($(this).children('.txtfld').val()) || 0;
                            $(".printer-type tr:last td:first").text('Total sheets/year');
                        });
                        return totalVal;

                    });
                    //Total calculation
            }
        });